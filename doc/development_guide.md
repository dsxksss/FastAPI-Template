# Nexus 后端开发指南

## 目录
1. [开发环境配置](#开发环境配置)
2. [添加新的数据模型](#添加新的数据模型)
3. [添加新的 API](#添加新的-api)
4. [权限控制](#权限控制)
5. [最佳实践](#最佳实践)

## 开发环境配置

### 1. 环境要求
- Python 3.11
- SQLite/PostgreSQL
- VSCode (推荐)

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置开发环境
1. 复制 `.env.example` 到 `.env`
2. 修改数据库配置
3. 配置 VSCode 开发环境（已包含在 `.vscode/launch.json`）

## 添加新的数据模型

### 1. 创建模型文件
在 `src/models` 目录下创建新的模型文件，例如 `article.py`：

```python
from tortoise import fields
from .base import BaseModel, TimestampMixin

class Article(BaseModel, TimestampMixin):
    """文章模型"""
    title = fields.CharField(
        max_length=200, 
        description="文章标题", 
        index=True
    )
    content = fields.TextField(
        description="文章内容"
    )
    author_id = fields.IntField(
        description="作者ID", 
        index=True
    )
    status = fields.BooleanField(
        default=True, 
        description="是否发布"
    )
    
    class Meta:
        table = "article"
        table_description = "文章表"
```

### 2. 注册模型
在 `src/models/__init__.py` 中导入新模型：

```python
from .article import Article

__all__ = [
    # ... 其他模型
    "Article",
]
```

### 3. 创建数据库迁移
```bash
# 生成迁移文件
aerich migrate

# 应用迁移
aerich upgrade
```

## 添加新的 API

### 1. 创建 Schema
在 `src/schemas` 目录下创建新的 schema 文件，例如 `articles.py`：

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ArticleBase(BaseModel):
    """文章基础模型"""
    title: str = Field(..., description="文章标题", example="示例文章")
    content: str = Field(..., description="文章内容", example="这是文章内容")
    status: bool = Field(True, description="是否发布", example=True)

class ArticleCreate(ArticleBase):
    """创建文章请求模型"""
    pass

class ArticleUpdate(ArticleBase):
    """更新文章请求模型"""
    title: Optional[str] = Field(None, description="文章标题")
    content: Optional[str] = Field(None, description="文章内容")
    status: Optional[bool] = Field(None, description="是否发布")

class ArticleOut(ArticleBase):
    """文章响应模型"""
    id: int = Field(..., description="文章ID")
    author_id: int = Field(..., description="作者ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True
```

### 2. 创建 Controller
在 `src/controllers` 目录下创建新的控制器文件，例如 `article.py`：

```python
from core.crud import CRUDBase
from models.article import Article
from schemas.articles import ArticleCreate, ArticleUpdate

class ArticleController(CRUDBase[Article, ArticleCreate, ArticleUpdate]):
    """文章控制器"""
    def __init__(self):
        super().__init__(model=Article)

article_controller = ArticleController()
```

### 3. 创建 API 路由
在 `src/api/v1` 目录下创建新的路由文件，例如 `articles.py`：

```python
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from controllers.article import article_controller
from schemas.base import Success, SuccessExtra
from schemas.articles import *

router = APIRouter()

@router.get("/list", summary="获取文章列表")
async def list_articles(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    title: str = Query(None, description="文章标题"),
):
    """获取文章列表"""
    q = Q()
    if title:
        q &= Q(title__contains=title)
    total, articles = await article_controller.list(
        page=page, 
        page_size=page_size, 
        search=q
    )
    data = [await obj.to_dict() for obj in articles]
    return SuccessExtra(
        data=data, 
        total=total, 
        page=page, 
        page_size=page_size
    )

@router.post("/create", summary="创建文章")
async def create_article(article_in: ArticleCreate):
    """创建文章"""
    article = await article_controller.create(obj_in=article_in)
    return Success(data=await article.to_dict())

@router.get("/get/{id}", summary="获取文章详情")
async def get_article(id: int):
    """获取文章详情"""
    article = await article_controller.get(id=id)
    return Success(data=await article.to_dict())

@router.post("/update/{id}", summary="更新文章")
async def update_article(id: int, article_in: ArticleUpdate):
    """更新文章"""
    article = await article_controller.update(id=id, obj_in=article_in)
    return Success(data=await article.to_dict())

@router.delete("/delete/{id}", summary="删除文章")
async def delete_article(id: int):
    """删除文章"""
    await article_controller.delete(id=id)
    return Success(msg="删除成功")
```

### 4. 注册路由
在 `src/api/v1/__init__.py` 中注册新路由：

```python
from .articles import router as articles_router

v1_router.include_router(
    articles_router,
    prefix="/article",
    dependencies=[DependPermisson],
    tags=["文章模块"]
)
```

### 5. 更新 API 权限
```bash
# 访问 API 管理页面
http://localhost:8000/api/v1/api/list

# 或通过 API 刷新
curl -X POST http://localhost:8000/api/v1/api/refresh
```

## 权限控制

### 1. 添加菜单
在 `src/core/init_app.py` 的 `init_menus` 函数中添加新菜单：

```python
async def init_menus():
    # ... 现有代码 ...
    children_menu.append(
        Menu(
            menu_type=MenuType.MENU,
            name="文章管理",
            path="article",
            order=7,
            parent_id=parent_menu.id,
            icon="material-symbols:article-outline",
            is_hidden=False,
            component="/system/article",
            keepalive=False,
        )
    )
```

### 2. 分配权限
1. 登录管理后台
2. 进入角色管理
3. 为相应角色分配新 API 的权限

## 最佳实践

### 1. 代码规范
- 遵循 PEP 8 编码规范
- 使用 Google 风格的文档字符串
- 所有接口必须有完整的类型注解
- 关键功能需要编写单元测试

### 2. 命名规范
- 模型名：使用单数形式，首字母大写（如 `Article`）
- 表名：使用小写，复数形式（如 `articles`）
- API 路径：使用小写，复数形式（如 `/articles`）
- 变量名：使用小写，下划线分隔（如 `article_list`）

### 3. 错误处理
- 使用自定义异常类
- 统一错误响应格式
- 记录关键错误日志

### 4. 性能优化
- 合理使用索引
- 避免 N+1 查询问题
- 使用异步操作处理耗时任务

### 5. 安全建议
- 所有用户输入必须验证
- 敏感数据必须加密
- 使用参数化查询防止 SQL 注入
- 实现适当的访问控制

## 常见问题

### 1. 数据库迁移失败
```bash
# 删除迁移文件
rm -rf migrations/

# 重新初始化
aerich init-db
aerich migrate
aerich upgrade
```

### 2. API 权限不生效
1. 检查路由是否正确添加了 `DependPermisson`
2. 运行 `refresh_api` 更新 API 列表
3. 检查角色权限配置

### 3. 模型关系问题
- 使用 `fields.ForeignKeyField` 定义外键关系
- 使用 `fields.ManyToManyField` 定义多对多关系
- 注意设置 `related_name` 避免命名冲突

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交变更
4. 推送到分支
5. 创建 Pull Request

