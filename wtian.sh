#!/usr/bin/env bash
# 问天 AI 统一脚本入口：./wtian.sh <命令> [参数]
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python}"
IMAGE="${IMAGE:-crpi-73k11wlq0reghi4z.cn-shenzhen.personal.cr.aliyuncs.com/litm/wtian-api}"
NPM_REGISTRY="${NPM_REGISTRY:-https://registry.npmmirror.com}"

usage() {
  cat <<'EOF'
用法：./wtian.sh <命令> [参数]

开发
  dev-api            启动后端（热重载，读取 api/.env），端口 PORT 默认 8000
  dev-ui             启动前端开发服务器（/api 代理到 API_PROXY_TARGET，默认 http://127.0.0.1:8000）
测试
  check              离线检查：排盘算法对照、经文与典籍数据、取用规则、提示词组装
  eval [--judge]     在线评测：固定案例调用真实模型（需 api/.env 中的 DEEPSEEK_API_KEY）
数据
  dianji [--huancun DIR]  重新生成《滴天髓》《穷通宝鉴》（维基文库）与《鬼谷子两头钳》数据（需 opencc-python-reimplemented）
构建
  build-api [TAG]    构建并推送后端镜像，TAG 默认当天日期（镜像名可用 IMAGE 覆盖）
  build-ui           构建前端静态文件到 ui/dist
部署（服务器信息读取 .deploy.env，参考 .deploy.env.example）
  deploy [TAG]       一键发布：build-api → build-ui → deploy-api → deploy-ui
                     DEPLOY_VIA=ssh 时不经镜像仓库，本地构建后用 ship-api 直传服务器
  ship-api TAG       把本地镜像经 SSH 直接导入服务器（镜像仓库推送不稳定时使用）
  deploy-api TAG     上传 compose 与 nginx 配置，切换后端镜像版本并重启，安装证书续期钩子
  deploy-ui          备份线上前端后同步 ui/dist（无需重启 nginx）
  status             查看线上容器、证书有效期与接口状态
EOF
}

load_deploy_env() {
  if [ -f "$ROOT/.deploy.env" ]; then
    set -a
    . "$ROOT/.deploy.env"
    set +a
  fi
  : "${DEPLOY_HOST:?set DEPLOY_HOST in .deploy.env, e.g. user@1.2.3.4}"
  DEPLOY_PORT="${DEPLOY_PORT:-22}"
  # Keep a literal ~ so it expands to the remote user's home, not the local one
  [ -n "${DEPLOY_DIR:-}" ] || DEPLOY_DIR='~'
  SITE_URL="${SITE_URL:-https://wtian.cloud}"
}

remote() {
  ssh -p "$DEPLOY_PORT" "$DEPLOY_HOST" "$@"
}

ship_api() {
  local tag="$1"
  echo "==> ship $IMAGE:$tag over ssh"
  docker save "$IMAGE:$tag" | gzip -1 | remote "gunzip | sudo docker load"
}

deploy_api() {
  local tag="$1" stamp
  stamp="$(date +%Y%m%d%H%M)"
  remote "cd $DEPLOY_DIR && test -f .env" || { echo "$DEPLOY_DIR/.env missing on server, see docker/.env.example" >&2; exit 1; }

  echo "==> upload compose and nginx config (previous copies kept as *.bak$stamp)"
  # Existing files on the server may be root-owned, hence sudo
  remote "cd $DEPLOY_DIR && sudo mkdir -p nginx/conf nginx/dist nginx/logs \
    && { [ ! -f docker-compose.yml ] || sudo cp -p docker-compose.yml docker-compose.yml.bak$stamp; } \
    && { [ ! -f nginx/conf/nginx.conf ] || sudo cp -p nginx/conf/nginx.conf nginx/conf/nginx.conf.bak$stamp; }"
  remote "sudo tee $DEPLOY_DIR/docker-compose.yml >/dev/null" < "$ROOT/docker/docker-compose.yml"
  remote "sudo tee $DEPLOY_DIR/nginx/conf/nginx.conf >/dev/null" < "$ROOT/docker/nginx/conf/nginx.conf"

  echo "==> install certbot deploy hook"
  remote "sudo tee /etc/letsencrypt/renewal-hooks/deploy/reload-wtian-nginx.sh >/dev/null \
    && sudo chmod 755 /etc/letsencrypt/renewal-hooks/deploy/reload-wtian-nginx.sh" < "$ROOT/docker/certbot-deploy-hook.sh"

  echo "==> switch API_TAG to $tag and restart"
  remote "cd $DEPLOY_DIR && if grep -q '^API_TAG=' .env; then sed -i 's/^API_TAG=.*/API_TAG=$tag/' .env; else echo 'API_TAG=$tag' >> .env; fi \
    && sudo docker compose up -d --pull missing --remove-orphans \
    && sudo docker exec wtian-nginx nginx -t -q \
    && sudo docker exec wtian-nginx nginx -s reload"

  echo "==> wait for API health"
  local i
  for i in $(seq 1 20); do
    if [ "$(remote "sudo docker inspect -f '{{.State.Health.Status}}' wtian-api")" = "healthy" ]; then
      echo "wtian-api healthy ($tag)"
      return 0
    fi
    sleep 3
  done
  echo "wtian-api not healthy, check: sudo docker logs wtian-api" >&2
  exit 1
}

deploy_ui() {
  [ -f "$ROOT/ui/dist/index.html" ] || { echo "ui/dist not found, run ./wtian.sh build-ui first" >&2; exit 1; }
  local stamp
  stamp="$(date +%Y%m%d%H%M)"
  echo "==> back up live frontend as nginx/dist-bak$stamp (keep latest 3)"
  remote "cd $DEPLOY_DIR/nginx && sudo cp -a dist dist-bak$stamp \
    && ls -d dist-bak* | sort | head -n -3 | xargs -r sudo rm -rf"
  # Sync in place: nginx bind-mounts this directory, so it must not be replaced
  echo "==> sync ui/dist"
  rsync -a --delete-after --delay-updates --exclude '.well-known/' \
    -e "ssh -p $DEPLOY_PORT" "$ROOT/ui/dist/" "$DEPLOY_HOST:$DEPLOY_DIR/nginx/dist/"
}

show_status() {
  remote "sudo docker ps --filter name=wtian --format '{{.Names}}\t{{.Image}}\t{{.Status}}'"
  echo "--- certificate"
  echo | openssl s_client -connect "${SITE_URL#https://}:443" -servername "${SITE_URL#https://}" 2>/dev/null \
    | openssl x509 -noout -enddate
  echo "--- endpoints"
  curl -s -o /dev/null -w "home  %{http_code}\n" "$SITE_URL/"
  curl -s -o /dev/null -w "api   %{http_code}\n" -X POST -H 'Content-Type: application/json' \
    -d '{"birth":"19900115 10","gender":"boy","is_lunar":false}' "$SITE_URL/api/bazi/paipan"
}

load_api_env() {
  cd "$ROOT/api"
  if [ -f .env ]; then
    set -a
    . ./.env
    set +a
  fi
}

ensure_ui_deps() {
  cd "$ROOT/ui"
  [ -d node_modules ] || npm install --registry="$NPM_REGISTRY"
}

cmd="${1:-}"
[ $# -gt 0 ] && shift

case "$cmd" in
  dev-api)
    load_api_env
    export APP_NAME="${APP_NAME:-wtian}" RD_HOST="${RD_HOST:-127.0.0.1}" RD_PORT="${RD_PORT:-16666}"
    export RD_DB="${RD_DB:-0}" RD_PASSWORD="${RD_PASSWORD:-123456}"
    export WHITELIST_IPS="${WHITELIST_IPS:-127.0.0.1}" ACCESS_LIMIT_PER_DAY="${ACCESS_LIMIT_PER_DAY:-10}"
    exec "$PYTHON" -m uvicorn main:app --reload --host 0.0.0.0 --port "${PORT:-8000}"
    ;;
  dev-ui)
    ensure_ui_deps
    exec npm run serve
    ;;
  check)
    cd "$ROOT/api"
    exec "$PYTHON" -m evals.check_engine
    ;;
  eval)
    load_api_env
    exec "$PYTHON" -m evals.run_llm_eval "$@"
    ;;
  dianji)
    cd "$ROOT/api"
    "$PYTHON" -m dianji.goujian "$@"
    exec "$PYTHON" -m dianji.goujian_liangtouqian "$@"
    ;;
  build-api)
    tag="${1:-$(date +%Y%m%d)}"
    docker build -t "$IMAGE:$tag" "$ROOT/api"
    docker push "$IMAGE:$tag"
    echo "pushed $IMAGE:$tag"
    ;;
  build-ui)
    ensure_ui_deps
    npm run build
    ;;
  deploy)
    tag="${1:-$(date +%Y%m%d)}"
    load_deploy_env
    if [ "${DEPLOY_VIA:-registry}" = "ssh" ]; then
      docker build -t "$IMAGE:$tag" "$ROOT/api"
      ship_api "$tag"
    else
      "$0" build-api "$tag"
    fi
    "$0" build-ui
    deploy_api "$tag"
    deploy_ui
    show_status
    ;;
  ship-api)
    tag="${1:?usage: ./wtian.sh ship-api TAG}"
    load_deploy_env
    ship_api "$tag"
    ;;
  deploy-api)
    tag="${1:?usage: ./wtian.sh deploy-api TAG (an image pushed by build-api or shipped by ship-api)}"
    load_deploy_env
    deploy_api "$tag"
    ;;
  deploy-ui)
    load_deploy_env
    deploy_ui
    ;;
  status)
    load_deploy_env
    show_status
    ;;
  ""|-h|--help|help)
    usage
    ;;
  *)
    echo "unknown command: $cmd" >&2
    usage
    exit 1
    ;;
esac
