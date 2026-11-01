# FROM python:3.10
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.10.4

RUN mkdir -p /wtian/api

WORKDIR /wtian/api


COPY . /wtian/api

RUN pip install  -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

#清理垃圾
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

# 启动命令（docker-compose.yml 中的 command 会覆盖它）
CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]