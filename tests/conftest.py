"""测试配置和固件"""

import asyncio
import os
import tempfile
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from tortoise import Tortoise

from src import app


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """设置测试数据库"""
    # 使用临时SQLite数据库
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db.close()
    
    db_url = f"sqlite://{temp_db.name}"
    
    # 初始化Tortoise ORM
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["src.models"]},
    )
    
    # 生成数据库架构
    await Tortoise.generate_schemas()
    
    yield
    
    # 清理
    await Tortoise.close_connections()
    os.unlink(temp_db.name)


@pytest.fixture
def client():
    """同步测试客户端"""
    with TestClient(app) as c:
        yield c


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """异步测试客户端"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def admin_token(async_client: AsyncClient) -> str:
    """获取管理员Token"""
    # 创建管理员用户
    from src.controllers.user import user_controller
    from src.schemas.users import UserCreate
    
    admin_user = UserCreate(
        username="test_admin",
        email="test_admin@test.com",
        password="Test123456",
        is_superuser=True,
        is_active=True
    )
    
    await user_controller.create_user(obj_in=admin_user)
    
    # 登录获取token
    response = await async_client.post(
        "/api/v1/base/access_token",
        json={
            "username": "test_admin",
            "password": "Test123456"
        }
    )
    
    data = response.json()
    return data["data"]["access_token"]


@pytest.fixture
async def normal_user_token(async_client: AsyncClient) -> str:
    """获取普通用户Token"""
    from src.controllers.user import user_controller
    from src.schemas.users import UserCreate
    
    normal_user = UserCreate(
        username="test_user",
        email="test_user@test.com", 
        password="Test123456",
        is_superuser=False,
        is_active=True
    )
    
    await user_controller.create_user(obj_in=normal_user)
    
    # 登录获取token
    response = await async_client.post(
        "/api/v1/base/access_token",
        json={
            "username": "test_user",
            "password": "Test123456"
        }
    )
    
    data = response.json()
    return data["data"]["access_token"]


@pytest.fixture
def auth_headers(admin_token: str) -> dict:
    """认证头"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def normal_auth_headers(normal_user_token: str) -> dict:
    """普通用户认证头"""
    return {"Authorization": f"Bearer {normal_user_token}"}