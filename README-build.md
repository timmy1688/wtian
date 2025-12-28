# 问天易经AI - 构建指南

## 📦 构建脚本

### 后端镜像构建
```bash
./build.sh
```
- 构建Docker镜像并推送到阿里云容器镜像服务
- Tag格式：当前日期（YYYYMMDD）
- 镜像名称：`crpi-73k11wlq0reghi4z.cn-shenzhen.personal.cr.aliyuncs.com/litm/wtian-api:YYYYMMDD`

### 前端静态文件构建
```bash
./build-ui.sh
```
- 构建Vue.js前端项目
- 生成静态文件到 `ui/dist/` 目录
- 可用于Nginx等Web服务器部署

## 🚀 部署流程

1. **构建后端**：`./build.sh`
2. **构建前端**：`./build-ui.sh`
3. **部署服务**：
   ```bash
   cd docker
   docker-compose up -d
   ```

## 📋 文件说明

- `build.sh` - 后端Docker镜像构建脚本
- `build-ui.sh` - 前端静态文件构建脚本
- `docker/docker-compose.yml` - 容器编排配置
- `api/Dockerfile` - 后端镜像构建配置

## 🔧 环境要求

- Docker & Docker Compose
- Node.js & npm (前端构建)
- 阿里云容器镜像服务访问权限
