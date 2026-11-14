# 页面先在仓库根目录构建到 ui/dist，再打进这个镜像。一次发布同时更新页面和接口。
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.10.4

RUN mkdir -p /wtian/api

WORKDIR /wtian/api

COPY api/requirements.txt /wtian/api/requirements.txt

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 基础镜像已带 tzdata，上海时区可直接用，不再单独 apt 安装
COPY api/ /wtian/api
COPY ui/dist /wtian/api/ui_dist

EXPOSE 8000

# 启动命令（docker-compose.yml 中的 command 会覆盖它）
CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000", "--graceful-timeout", "30"]
