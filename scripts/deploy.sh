#!/bin/bash

# 设置变量
IMAGE_NAME="crpi-nessk20nyrqkpfxu.cn-shenzhen.personal.cr.aliyuncs.com/giihg/nexus-backend"
CONTAINER_NAME="nexus-backend-container"

# 自动获取最新的语义化版本标签
# 注意：这需要您已登录到 Docker 仓库
echo "Fetching latest tag from repository..."
LATEST_TAG=$(docker search --limit 100 ${IMAGE_NAME} --format "{{.Tag}}" | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | tail -n 1)

if [ -z "${LATEST_TAG}" ]; then
    echo "Could not find a valid semantic version tag. Using 'latest' instead."
    LATEST_TAG="latest"
fi

IMAGE_WITH_TAG="${IMAGE_NAME}:${LATEST_TAG}"
echo "Using image: ${IMAGE_WITH_TAG}"

# 停止并删除旧的容器（如果存在）
if [ $(docker ps -a -f name=^/${CONTAINER_NAME}$ --format '{{.Names}}') ]; then
    echo "Stopping and removing existing container: ${CONTAINER_NAME}"
    docker stop ${CONTAINER_NAME}
    docker rm ${CONTAINER_NAME}
fi

# 拉取最新的镜像
echo "Pulling latest image: ${IMAGE_WITH_TAG}"
docker pull ${IMAGE_WITH_TAG}

# 创建logs和uploads目录（如果不存在）
echo "Creating logs and uploads directories if they don't exist..."
mkdir -p ./logs
mkdir -p ./uploads

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "❌ 错误：.env 文件不存在，请确保配置文件已准备好"
    exit 1
fi

# 检查是否设置了环境类型
if grep -q "ENVIRONMENT=" .env; then
    DEPLOY_ENV=$(grep "ENVIRONMENT=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    echo "📊 检测到环境配置: ${DEPLOY_ENV}"
else
    echo "⚠️ 未检测到 ENVIRONMENT 配置，默认为开发环境"
    DEPLOY_ENV="development"
fi

# 根据环境提供不同的部署策略
case ${DEPLOY_ENV} in
    "production")
        echo "🏭 生产环境部署 - 仅应用现有迁移"
        MIGRATION_STRATEGY="production"
        ;;
    "staging"|"test")
        echo "🧪 测试环境部署 - 允许自动迁移"
        MIGRATION_STRATEGY="test"
        ;;
    *)
        echo "🔧 开发环境部署 - 完整迁移处理"
        MIGRATION_STRATEGY="development"
        ;;
esac

echo "Database migrations will be handled during container startup with strategy: ${MIGRATION_STRATEGY}"

# 启动新容器
echo "Starting new container: ${CONTAINER_NAME}"
# 获取当前用户的UID和GID
USER_ID=$(id -u)
GROUP_ID=$(id -g)

# 创建容器时传递环境信息
# 注意：为了避免权限问题，暂时移除 --user 参数
docker run -d -p 8000:8000 \
  --env-file .env \
  -e DEPLOYMENT_STRATEGY="${MIGRATION_STRATEGY}" \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/uploads:/app/uploads \
  --name ${CONTAINER_NAME} \
  ${IMAGE_WITH_TAG}

echo "Deployment complete."