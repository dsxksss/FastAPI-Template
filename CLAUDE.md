# CLAUDE.md - 企业级FastAPI后端模板开发指南

这是一个专为团队开发设计的企业级FastAPI后端模板项目的Claude Code开发指南。

## 📋 项目概述

本项目是一个功能完整的企业级FastAPI后端模板，采用现代化的三层架构设计，内置完整的RBAC权限管理、用户管理、文件管理等核心企业功能。项目已完全移除AI相关业务逻辑，专注于提供干净、可扩展的后端框架。

## 🛠️ 开发环境命令

### 环境管理

```bash
# 安装UV包管理器
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆项目后，安装依赖
uv sync

# 安装开发依赖
uv sync --dev

# 创建虚拟环境（如果需要独立环境）
uv venv
source .venv/bin/activate  # Linux/macOS
# 或 .venv\Scripts\activate  # Windows
```

### 应用运行

```bash
# 开发服务器
uv run uvicorn src:app --reload --host 0.0.0.0 --port 8000

# 生产服务器
uv run uvicorn src:app --host 0.0.0.0 --port 8000 --workers 4
```

### 数据库操作

```bash
# 初始化数据库（首次运行）
uv run aerich init-db

# 生成迁移文件（模型变更后）
uv run aerich migrate --name "describe_your_changes"

# 应用迁移到数据库
uv run aerich upgrade

# 查看迁移历史
uv run aerich history

# 回滚迁移（谨慎使用）
uv run aerich downgrade
```

### 测试和质量控制

```bash
# 运行所有测试
uv run pytest

# 运行特定测试文件
uv run pytest tests/test_users.py

# 生成测试覆盖率报告
uv run pytest --cov=src --cov-report=html

# 代码格式化
uv run black src/
uv run isort src/

# 代码质量检查
uv run pylint src/
uv run flake8 src/
```

### Docker操作

```bash
# 构建镜像
docker build -t backend-template .

# 运行容器
docker run -p 8000:8000 backend-template

# 使用docker-compose
docker-compose up -d

# 查看日志
docker-compose logs -f app
```

## 🏗️ 项目架构详解

### 三层架构模式

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ FastAPI Routes (src/api/v1/)                        │    │
│  │ • 参数验证和类型转换                                    │    │
│  │ • 路由分发和响应格式化                                  │    │
│  │ • 依赖注入 (认证、权限)                                │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Service Layer                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Business Logic (src/services/)                      │    │
│  │ • 业务规则验证和处理                                    │    │
│  │ • 权限检查和业务安全                                    │    │
│  │ • 跨Repository的复杂操作                               │    │
│  │ • 统一异常处理和日志记录                                │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Repository Layer                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Data Access (src/repositories/)                     │    │
│  │ • CRUD操作和数据库查询                                  │    │
│  │ • 简单的查询条件构建                                    │    │
│  │ • 数据模型转换                                         │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Model Layer                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Tortoise ORM Models (src/models/)                   │    │
│  │ • 数据模型定义和关系                                    │    │
│  │ • 数据库表结构                                         │    │
│  │ • 模型验证和约束                                       │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 核心设计原则

1. **单一职责原则** - 每个层次只处理自己的逻辑
2. **依赖注入** - 通过FastAPI的依赖系统管理组件
3. **类型安全** - 全面使用Python类型注解
4. **异步优先** - 所有I/O操作都是异步的
5. **安全第一** - 内置多重安全防护机制

### 目录结构详解

```
src/
├── api/v1/              # 🌐 API路由层 (轻量级)
│   ├── __init__.py     # 路由注册
│   ├── base/           # 基础接口 (健康检查、登录等)
│   ├── users/          # 用户管理接口
│   ├── roles/          # 角色管理接口
│   ├── menus/          # 菜单管理接口
│   ├── files/          # 文件管理接口
│   ├── depts/          # 部门管理接口
│   ├── apis/           # API权限管理接口
│   └── auditlog/       # 审计日志接口
│
├── services/            # 🔧 业务逻辑层 (核心)
│   ├── __init__.py
│   ├── base_service.py # 基础服务类和权限服务
│   ├── user_service.py # 用户业务逻辑
│   └── file_service.py # 文件业务逻辑
│
├── repositories/        # 🗄️ 数据访问层 (Repository模式)
│   ├── __init__.py
│   ├── user.py         # 用户数据操作
│   ├── role.py         # 角色数据操作
│   ├── menu.py         # 菜单数据操作
│   ├── api.py          # API数据操作
│   ├── dept.py         # 部门数据操作
│   └── file_mapping.py # 文件映射数据操作
│
├── models/              # 📊 数据模型层
│   ├── __init__.py
│   ├── base.py         # 基础模型类
│   ├── admin.py        # 用户、角色、权限模型
│   └── enums.py        # 枚举定义
│
├── schemas/             # ✅ 数据验证层
│   ├── __init__.py
│   ├── base.py         # 基础响应模式
│   ├── users.py        # 用户相关Schema
│   ├── roles.py        # 角色相关Schema
│   ├── menus.py        # 菜单相关Schema
│   ├── apis.py         # API相关Schema
│   ├── depts.py        # 部门相关Schema
│   └── login.py        # 登录相关Schema
│
├── core/                # ⚙️ 核心功能
│   ├── dependency.py   # 依赖注入 (认证、权限)
│   ├── middlewares.py  # 中间件 (CORS、安全头、日志)
│   ├── exceptions.py   # 异常处理
│   ├── crud.py         # CRUD基类
│   ├── ctx.py          # 上下文管理
│   ├── init_app.py     # 应用初始化
│   └── bgtask.py       # 后台任务
│
├── utils/               # 🔧 工具函数
│   ├── jwt.py          # JWT令牌处理
│   ├── password.py     # 密码加密验证
│   └── sensitive_word_filter.py # 敏感词过滤
│
├── settings/            # ⚙️ 配置管理
│   ├── __init__.py
│   └── config.py       # 配置类定义
│
├── log/                 # 📋 日志模块
│   ├── __init__.py
│   ├── log.py          # 日志配置
│   └── context.py      # 日志上下文
│
└── handlers/            # 🔄 处理器
    ├── __init__.py
    ├── data_processor.py    # 数据处理器
    └── sensitive_filter.py  # 敏感词过滤处理器
```

## 🚀 添加新功能指南

### 标准开发流程

1. **定义数据模型** (`src/models/`)
2. **创建Pydantic Schema** (`src/schemas/`)
3. **实现Repository数据层** (`src/repositories/`)
4. **编写Service业务层** (`src/services/`)
5. **添加API路由** (`src/api/v1/`)
6. **生成数据库迁移**
7. **编写测试**

### 示例：添加"产品管理"功能

#### 1. 定义数据模型 (`src/models/admin.py`)

```python
class Product(BaseModel, TimestampMixin):
    """产品模型"""
    name = fields.CharField(max_length=200, description="产品名称", index=True)
    description = fields.TextField(description="产品描述", null=True)
    price = fields.DecimalField(max_digits=10, decimal_places=2, description="价格")
    category_id = fields.IntField(description="分类ID", index=True)
    is_active = fields.BooleanField(default=True, description="是否激活")
    
    class Meta:
        table = "product"
```

#### 2. 创建Schema (`src/schemas/products.py`)

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str = Field(..., description="产品名称", max_length=200)
    description: Optional[str] = Field(None, description="产品描述")
    price: float = Field(..., description="价格", gt=0)
    category_id: int = Field(..., description="分类ID")
    is_active: bool = Field(True, description="是否激活")

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, description="产品名称", max_length=200)
    description: Optional[str] = Field(None, description="产品描述")
    price: Optional[float] = Field(None, description="价格", gt=0)
    category_id: Optional[int] = Field(None, description="分类ID")
    is_active: Optional[bool] = Field(None, description="是否激活")

class ProductOut(ProductCreate):
    id: int
    created_at: datetime
    updated_at: datetime
```

#### 3. 实现Repository (`src/repositories/product.py`)

```python
from core.crud import CRUDBase
from models.admin import Product
from schemas.products import ProductCreate, ProductUpdate

class ProductRepository(CRUDBase[Product, ProductCreate, ProductUpdate]):
    """产品数据访问层 (Repository模式)"""
    
    async def get_products_by_category(self, category_id: int):
        """根据分类获取产品"""
        return await self.model.filter(category_id=category_id, is_active=True).all()
    
    async def search_products(self, keyword: str):
        """搜索产品"""
        return await self.model.filter(
            name__icontains=keyword, 
            is_active=True
        ).all()

# 全局实例
product_repository = ProductRepository(Product)
```

#### 4. 编写Service (`src/services/product_service.py`)

```python
from services.base_service import BaseService, permission_service
from repositories.product import product_repository
from schemas.products import ProductCreate, ProductUpdate
from schemas.base import Success, Fail
from models.admin import User

class ProductService(BaseService):
    """产品业务逻辑层"""
    
    def __init__(self):
        super().__init__(product_repository)
    
    async def create_product(self, data: ProductCreate, current_user: User) -> Success:
        """创建产品 - 需要管理员权限"""
        try:
            # 权限检查
            permission_error = await permission_service.check_superuser(current_user)
            if permission_error:
                return permission_error
            
            # 业务逻辑验证
            if await product_repository.model.filter(name=data.name).exists():
                return Fail(msg="产品名称已存在")
            
            # 创建产品
            return await self.create_item(
                item_data=data.dict(),
                success_msg="产品创建成功"
            )
            
        except Exception as e:
            self.logger.error(f"创建产品失败: {str(e)}")
            return Fail(msg="创建产品失败")
    
    async def search_products(self, keyword: str) -> Success:
        """搜索产品"""
        try:
            products = await product_repository.search_products(keyword)
            return Success(data=products, msg="搜索成功")
        except Exception as e:
            self.logger.error(f"搜索产品失败: {str(e)}")
            return Fail(msg="搜索失败")

# 全局实例
product_service = ProductService()
```

#### 5. 添加API路由 (`src/api/v1/products/`)

```python
# src/api/v1/products/__init__.py
from fastapi import APIRouter
from .products import router

product_router = APIRouter()
product_router.include_router(router, tags=["产品管理"])
```

```python
# src/api/v1/products/products.py
from fastapi import APIRouter, Query
from core.dependency import DependAuth
from models.admin import User
from schemas.products import ProductCreate, ProductUpdate
from services.product_service import product_service

router = APIRouter()

@router.get("/list", summary="获取产品列表")
async def get_products(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    current_user: User = DependAuth,
):
    """获取产品列表"""
    return await product_service.get_paginated_list(page=page, page_size=page_size)

@router.post("/create", summary="创建产品")
async def create_product(
    data: ProductCreate,
    current_user: User = DependAuth,
):
    """创建产品"""
    return await product_service.create_product(data, current_user)

@router.get("/search", summary="搜索产品")
async def search_products(
    keyword: str = Query(..., description="搜索关键词"),
    current_user: User = DependAuth,
):
    """搜索产品"""
    return await product_service.search_products(keyword)
```

#### 6. 注册路由 (`src/api/v1/__init__.py`)

```python
from api.v1.products import product_router

# 添加到router注册中
api_router.include_router(product_router, prefix="/products")
```

#### 7. 生成数据库迁移

```bash
uv run aerich migrate --name "add_product_model"
uv run aerich upgrade
```

#### 8. 编写测试 (`tests/test_products.py`)

```python
import pytest
from httpx import AsyncClient
from src import app

@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 登录获取token
        login_response = await ac.post("/api/v1/base/access_token", data={
            "username": "admin",
            "password": "abcd1234"
        })
        token = login_response.json()["access_token"]
        
        # 创建产品
        response = await ac.post(
            "/api/v1/products/create",
            json={
                "name": "测试产品",
                "description": "这是一个测试产品",
                "price": 99.99,
                "category_id": 1
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["msg"] == "产品创建成功"
```

## 🔐 安全最佳实践

### JWT认证流程

1. **用户登录** → 验证用户名密码
2. **生成Token** → 包含用户ID、角色等信息
3. **Token验证** → 每个请求验证Token有效性
4. **权限检查** → 根据用户角色检查API访问权限

### 权限控制设计

```python
# 使用依赖注入进行权限检查
from core.dependency import DependAuth, SuperUserRequired

@router.post("/admin-only")
async def admin_only_endpoint(current_user: User = SuperUserRequired):
    """只有超级管理员可以访问"""
    pass

@router.get("/authenticated")  
async def authenticated_endpoint(current_user: User = DependAuth):
    """需要认证的接口"""
    pass
```

### 文件上传安全

- **文件类型验证** - 白名单机制
- **文件大小限制** - 防止大文件攻击
- **危险文件检测** - 黑名单过滤
- **安全文件名** - 防止路径遍历攻击
- **病毒扫描** - 可扩展集成杀毒引擎

## 📊 数据库最佳实践

### 模型设计原则

```python
# 继承基础模型类
class YourModel(BaseModel, TimestampMixin):
    # 字段定义
    name = fields.CharField(max_length=200, description="名称", index=True)
    
    # 关联关系
    user = fields.ForeignKeyField("models.User", related_name="your_models")
    
    # 元数据
    class Meta:
        table = "your_table"
        # 索引定义
        indexes = [
            ("name", "created_at"),  # 复合索引
        ]
```

### 查询优化

```python
# 使用select_related预加载关联数据
users = await User.all().select_related("roles")

# 使用prefetch_related优化多对多查询
roles = await Role.all().prefetch_related("menus", "apis")

# 使用索引字段进行查询
products = await Product.filter(is_active=True).all()
```

## 🧪 测试指南

### 测试结构

```
tests/
├── conftest.py              # 测试配置和固件
├── test_auth.py            # 认证测试
├── test_users.py           # 用户管理测试
├── test_roles.py           # 角色管理测试
├── test_files.py           # 文件管理测试
└── integration/            # 集成测试
    ├── test_workflows.py   # 工作流测试
    └── test_permissions.py # 权限测试
```

### 测试工具配置

```python
# conftest.py
import pytest
from tortoise.contrib.test import initializer, finalizer
from src.settings.config import settings

@pytest.fixture(scope="session", autouse=True)
def initialize_tests():
    # 初始化测试数据库
    initializer(["src.models"], db_url="sqlite://:memory:")
    yield
    finalizer()

@pytest.fixture
async def test_client():
    from httpx import AsyncClient
    from src import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
```

## 🚀 部署指南

### 环境变量配置

**开发环境 (.env.development)**
```bash
DEBUG=True
APP_ENV=development
DB_ENGINE=sqlite
LOG_LEVEL=DEBUG
```

**生产环境 (.env.production)**
```bash
DEBUG=False
APP_ENV=production
DB_ENGINE=postgres
DB_HOST=your_postgres_host
DB_PASSWORD=your_strong_password
SECRET_KEY=your_64_char_secret_key
CORS_ORIGINS=https://your-domain.com
LOG_LEVEL=INFO
```

### Docker部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 安装依赖
RUN uv sync --frozen --no-dev

# 复制源代码
COPY . .

# 运行应用
CMD ["uv", "run", "uvicorn", "src:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Nginx配置

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🛠️ 故障排除

### 常见问题

1. **Tortoise ORM导入错误**
```python
# ❌ 错误：相对导入
from .models import User

# ✅ 正确：使用字符串引用
user = fields.ForeignKeyField("models.User")
```

2. **异步上下文错误**
```python
# ❌ 错误：直接访问关系
roles = user.roles

# ✅ 正确：使用异步方法
roles = await user.roles.all()
```

3. **路径导入问题**
```bash
# 设置PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# 或在pyproject.toml中配置
[tool.hatch.envs.default.env-vars]
PYTHONPATH = "src"
```

### 性能优化

- **数据库连接池配置**
- **异步任务队列**
- **缓存策略实施**
- **静态资源CDN**

## 📝 代码规范

### Python代码风格

```python
# 使用类型注解
async def create_user(data: UserCreate, current_user: User) -> Success:
    """创建用户
    
    Args:
        data: 用户创建数据
        current_user: 当前操作用户
        
    Returns:
        Success: 创建结果
    """
    pass

# 异常处理
try:
    result = await some_operation()
    return Success(data=result)
except SpecificException as e:
    logger.error(f"操作失败: {str(e)}")
    return Fail(msg="操作失败")
```

### 文档字符串规范

```python
def complex_function(param1: str, param2: int = 10) -> Dict[str, Any]:
    """执行复杂操作的函数
    
    这个函数执行一些复杂的业务逻辑处理。
    
    Args:
        param1: 字符串参数，用于xxx
        param2: 整数参数，默认为10，用于yyy
        
    Returns:
        包含处理结果的字典
        
    Raises:
        ValueError: 当param1为空时抛出
        
    Example:
        >>> result = complex_function("test", 5)
        >>> print(result["status"])
        success
    """
    pass
```

## 🔄 持续集成

### GitHub Actions示例

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Install uv
      uses: astral-sh/setup-uv@v2
      
    - name: Set up Python
      run: uv python install 3.11
      
    - name: Install dependencies
      run: uv sync
      
    - name: Run tests
      run: uv run pytest --cov=src
      
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## 🔗 相关资源

### 官方文档
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tortoise ORM Documentation](https://tortoise.github.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [UV Documentation](https://docs.astral.sh/uv/)

### 开发工具
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) - AI编程助手
- [Postman](https://www.postman.com/) - API测试工具
- [DBeaver](https://dbeaver.io/) - 数据库管理工具

---

**这是一个企业级的FastAPI后端模板项目，专为团队开发设计。遵循最佳实践，提供完整的功能和安全保障。** 🚀