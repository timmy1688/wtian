#!/bin/bash

# 问天易经AI - 后端镜像构建脚本

# 获取当前日期作为tag (格式: YYYYMMDD)
TAG=$(date +%Y%m%d)
image=crpi-73k11wlq0reghi4z.cn-shenzhen.personal.cr.aliyuncs.com/litm/wtian-api

echo "🔨 构建问天易经AI后端镜像... (Tag: $TAG)"
cd api && docker build -t $image:$TAG .

if [ $? -eq 0 ]; then
    echo "✅ 镜像构建成功: $image:$TAG"
    docker images $image:$TAG
else
    echo "❌ 镜像构建失败"
    exit 1
fi
docker push $image:$TAG