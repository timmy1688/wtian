#!/bin/bash

# 问天易经AI - 服务重启脚本

echo "🔄 重启问天易经AI服务..."

cd docker

# 停止所有服务
echo "🛑 停止服务..."
docker-compose down

# 启动所有服务
echo "🚀 启动服务..."
docker-compose up -d

# 检查服务状态
echo "📊 服务状态:"
docker-compose ps

echo "✅ 重启完成"
