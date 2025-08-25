import json
import os
from datetime import UTC, datetime

from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from core.ctx import CTX_USER_ID
from core.dependency import DependAuth
from models.admin import User
from repositories.user import user_repository
from schemas.base import Fail, Success
from schemas.login import (
    CredentialsSchema,
    JWTOut,
    RefreshTokenRequest,
    TokenRefreshOut,
)
from schemas.response import (
    CurrentUserResponse,
    HealthInfo,
    HealthResponse,
    TokenResponse,
    VersionInfo,
    VersionResponse,
)
from settings import settings
from utils.jwt import create_token_pair, verify_token

# 创建限流器实例
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


def apply_rate_limit(rate="5/minute"):
    """根据环境应用限流装饰器"""

    def decorator(func):

        if os.getenv("TESTING", "false").lower() == "true":
            return func  # 测试环境不应用限流
        return limiter.limit(rate)(func)

    return decorator


@router.post("/access_token", summary="获取token", response_model=TokenResponse)
@apply_rate_limit()
async def login_access_token(request: Request, credentials: CredentialsSchema):
    user: User = await user_repository.authenticate(credentials)
    await user_repository.update_last_login(user.id)

    # 创建访问令牌和刷新令牌
    access_token, refresh_token = create_token_pair(
        user_id=user.id, username=user.username, is_superuser=user.is_superuser
    )

    data = JWTOut(
        access_token=access_token,
        refresh_token=refresh_token,
        username=user.username,
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    result = Success(data=data.model_dump())
    return json.loads(result.body)


@router.post("/refresh_token", summary="刷新token", response_model=TokenResponse)
@apply_rate_limit("10/minute")
async def refresh_access_token(request: Request, refresh_request: RefreshTokenRequest):
    """
    使用刷新令牌获取新的访问令牌和刷新令牌
    """
    try:
        # 验证刷新令牌
        payload = verify_token(refresh_request.refresh_token, token_type="refresh")

        # 验证用户是否仍然存在且有效
        user = await user_repository.get(id=payload.user_id)
        if not user or not user.is_active:
            return Fail(code=401, msg="用户不存在或已被禁用")

        # 创建新的令牌对
        access_token, refresh_token = create_token_pair(
            user_id=user.id, username=user.username, is_superuser=user.is_superuser
        )

        data = TokenRefreshOut(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

        result = Success(data=data.model_dump())
        return json.loads(result.body)

    except Exception:
        result = Fail(code=401, msg="令牌无效或已过期")
        return json.loads(result.body)


@router.get("/userinfo", summary="查看用户信息", response_model=CurrentUserResponse)
async def get_userinfo(current_user: User = DependAuth):
    user_id = CTX_USER_ID.get()
    user_obj = await user_repository.get(id=user_id)
    user_dict = await user_obj.to_dict()
    result = Success(data=user_dict)
    return json.loads(result.body)


@router.get("/health", summary="健康检查", response_model=HealthResponse)
async def health_check():
    """系统健康检查"""
    health_data = HealthInfo(
        status="healthy",
        timestamp=datetime.now(UTC),
        environment=settings.APP_ENV,
        database="connected"
    )
    return HealthResponse(code=200, msg="OK", data=health_data)


@router.get("/version", summary="版本信息", response_model=VersionResponse)
async def get_version():
    """获取API版本信息"""
    version_data = VersionInfo(
        app_name=settings.APP_TITLE,
        version=settings.VERSION,
        api_version="v1",
        environment=settings.APP_ENV
    )
    return VersionResponse(code=200, msg="OK", data=version_data)


# @router.get("/usermenu", summary="查看用户菜单", dependencies=[DependAuth])
# async def get_user_menu():
#     user_id = CTX_USER_ID.get()
#     user_obj = await User.filter(id=user_id).first()
#     menus: list[Menu] = []
#     if user_obj.is_superuser:
#         menus = await Menu.all()
#     else:
#         role_objs: list[Role] = await user_obj.roles
#         for role_obj in role_objs:
#             menu = await role_obj.menus
#             menus.extend(menu)
#         menus = list(set(menus))
#     parent_menus: list[Menu] = []
#     for menu in menus:
#         if menu.parent_id == 0:
#             parent_menus.append(menu)
#     res = []
#     for parent_menu in parent_menus:
#         parent_menu_dict = await parent_menu.to_dict()
#         parent_menu_dict["children"] = []
#         for menu in menus:
#             if menu.parent_id == parent_menu.id:
#                 parent_menu_dict["children"].append(await menu.to_dict())
#         res.append(parent_menu_dict)
#     return Success(data=res)


# @router.get("/userapi", summary="查看用户API", dependencies=[DependAuth])
# async def get_user_api():
#     user_id = CTX_USER_ID.get()
#     user_obj = await User.filter(id=user_id).first()
#     if user_obj.is_superuser:
#         api_objs: list[Api] = await Api.all()
#         apis = [api.method.lower() + api.path for api in api_objs]
#         return Success(data=apis)
#     role_objs: list[Role] = await user_obj.roles
#     apis = []
#     for role_obj in role_objs:
#         api_objs: list[Api] = await role_obj.apis
#         apis.extend([api.method.lower() + api.path for api in api_objs])
#     apis = list(set(apis))
#     return Success(data=apis)


# @router.post("/update_password", summary="修改密码", dependencies=[DependAuth])
# async def update_user_password(req_in: UpdatePassword):
#     user_id = CTX_USER_ID.get()
#     user = await user_controller.get(user_id)
#     verified = verify_password(req_in.old_password, user.password)
#     if not verified:
#         return Fail(msg="旧密码验证错误！")
#     user.password = get_password_hash(req_in.new_password)
#     await user.save()
#     return Success(msg="修改成功")
