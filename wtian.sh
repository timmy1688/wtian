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
  dianji [--huancun DIR]  从维基文库重新生成《滴天髓》《穷通宝鉴》数据（需 opencc-python-reimplemented）
构建与部署
  build-api [TAG]    构建并推送后端镜像，TAG 默认当天日期（镜像名可用 IMAGE 覆盖）
  build-ui           构建前端静态文件到 ui/dist
  deploy-ui          上传 ui/dist 并重启 nginx 容器（需 DEPLOY_HOST，可选 DEPLOY_PORT、DEPLOY_PATH）
  restart            在 docker/ 下重启全部容器
EOF
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
    exec "$PYTHON" -m dianji.goujian "$@"
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
  deploy-ui)
    : "${DEPLOY_HOST:?set DEPLOY_HOST, e.g. user@1.2.3.4}"
    [ -d "$ROOT/ui/dist" ] || { echo "ui/dist not found, run ./wtian.sh build-ui first" >&2; exit 1; }
    port="${DEPLOY_PORT:-22}"
    rsync -a -e "ssh -p $port" "$ROOT/ui/dist" "$DEPLOY_HOST:${DEPLOY_PATH:-~/nginx/}"
    ssh -p "$port" "$DEPLOY_HOST" "sudo docker restart wtian-nginx"
    ;;
  restart)
    cd "$ROOT/docker"
    docker-compose down
    docker-compose up -d
    docker-compose ps
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
