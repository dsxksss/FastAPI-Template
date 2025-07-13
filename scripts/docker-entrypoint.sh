#!/bin/bash
set -e

echo "🚀 正在启动 Nexus Backend..."

# 设置工作目录和 Python 路径
cd /app
export PYTHONPATH=/app:/app/src

# 获取环境变量，判断是否为生产环境
ENVIRONMENT=${ENVIRONMENT:-"development"}
SKIP_MIGRATIONS=${SKIP_MIGRATIONS:-"false"}

echo "📊 当前环境: $ENVIRONMENT"
echo "📁 当前工作目录: $(pwd)"
echo "🐍 Python 路径: $PYTHONPATH"

# 检查关键文件是否存在
if [ ! -f "aerich_config.py" ]; then
    echo "❌ 错误：aerich_config.py 文件不存在"
    exit 1
fi

# 数据库迁移处理
if [ "$SKIP_MIGRATIONS" = "true" ]; then
    echo "⚠️ 跳过数据库迁移（SKIP_MIGRATIONS=true）"
elif [ "$ENVIRONMENT" = "production" ]; then
    echo "🏭 生产环境 - 仅应用现有迁移..."
    
    # 生产环境只应用迁移，不生成新的
    echo "🔧 应用数据库迁移..."
    if aerich upgrade; then
        echo "✅ 迁移应用成功"
    else
        echo "❌ 迁移失败！请检查迁移文件是否兼容"
        echo "💡 尝试设置 SKIP_MIGRATIONS=true 跳过迁移"
        exit 1
    fi
else
    echo "🧪 开发/测试环境 - 完整迁移处理..."
    
    # 检查是否已经初始化过 aerich
    if [ ! -f "pyproject.toml" ]; then
        echo "🔧 首次初始化 aerich..."
        if aerich init --tortoise-orm aerich_config.TORTOISE_ORM; then
            echo "✅ aerich 初始化成功"
        else
            echo "❌ aerich 初始化失败"
            exit 1
        fi
    else
        echo "ℹ️ aerich 配置文件已存在"
    fi

    # 检查并创建迁移目录
    if [ ! -d "migrations" ]; then
        echo "🔧 创建迁移目录..."
        mkdir -p migrations/models || {
            echo "❌ 无法创建迁移目录，可能是权限问题"
            echo "💡 尝试使用 root 用户或调整目录权限"
            exit 1
        }
        
        echo "🔧 首次初始化数据库..."
        if aerich init-db; then
            echo "✅ 数据库初始化成功"
        else
            echo "❌ 数据库初始化失败"
            exit 1
        fi
    else
        echo "ℹ️ 迁移目录已存在"
        
        # 生成新的迁移（如果有变更）
        echo "🔧 检查并生成迁移文件..."
        if aerich migrate --name "auto_migration_$(date +%Y%m%d_%H%M%S)"; then
            echo "✅ 新迁移文件已生成"
        else
            echo "ℹ️ 无需生成新的迁移文件"
        fi

        # 应用迁移
        echo "🔧 应用数据库迁移..."
        if aerich upgrade; then
            echo "✅ 迁移应用成功"
        else
            echo "⚠️ 迁移应用可能已是最新版本"
        fi
    fi
fi

echo "✅ 数据库迁移处理完成"

# 检查应用文件是否存在
if [ ! -f "src/__init__.py" ]; then
    echo "❌ 错误：src/__init__.py 文件不存在"
    exit 1
fi

# 启动应用
echo "🌟 启动 FastAPI 应用..."
exec uvicorn src:app --host 0.0.0.0 --port 8000