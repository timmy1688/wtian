#!/bin/bash

# 问天易经AI - 前端静态文件构建脚本

echo "🔨 构建问天易经AI前端静态文件..."

# 检查是否安装了依赖
if [ ! -d "ui/node_modules" ]; then
    echo "📦 安装前端依赖..."
    cd ui && npm install
    cd ..
fi

# 执行构建
cd ui && npm run build

if [ $? -eq 0 ]; then
    echo "✅ 前端构建成功"
    echo "📁 静态文件位置: ui/dist/"
    ls -la ui/dist/
else
    echo "❌ 前端构建失败"
    exit 1
fi
