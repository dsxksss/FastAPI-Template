#!/bin/bash

# 设置镜像名称和标签
IMAGE_NAME="crpi-nessk20nyrqkpfxu.cn-shenzhen.personal.cr.aliyuncs.com/giihg/nexus-backend"
# 生成基于时间的标签
TAG=$(date +%Y%m%d%H%M%S)

# 构建并标记镜像
echo "Building and tagging image: ${IMAGE_NAME}:${TAG} and ${IMAGE_NAME}:latest"
docker build -t "${IMAGE_NAME}:${TAG}" -t "${IMAGE_NAME}:latest" .

echo "Build complete."

# 推送镜像到仓库
echo "Pushing image to repository: ${IMAGE_NAME}:${TAG}"
docker push "${IMAGE_NAME}:${TAG}"
echo "Pushing image to repository: ${IMAGE_NAME}:latest"
docker push "${IMAGE_NAME}:latest"

echo "Push complete."