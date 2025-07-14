import json
import os
import secrets
import typing

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    VERSION: str = "0.1.0"
    APP_TITLE: str = "Vue FastAPI Admin"
    PROJECT_NAME: str = "Vue FastAPI Admin"
    APP_DESCRIPTION: str = "Description"

    CORS_ORIGINS: str = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:8080"
    )

    @property
    def CORS_ORIGINS_LIST(self) -> typing.List[str]:
        """将CORS_ORIGINS字符串转换为列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: typing.List = [
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
    ]
    CORS_ALLOW_HEADERS: typing.List = [
        "Content-Type",
        "Authorization",
        "X-Requested-With",
    ]

    DEBUG: bool = True
    APP_ENV: str = "development"

    PROJECT_ROOT: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT: str = os.path.join(BASE_DIR, "app/logs")
    SECRET_KEY: str = os.getenv("SECRET_KEY") or secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 4  # 4 hours
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 7 days for refresh token
    # 数据库配置
    DB_ENGINE: str = "postgres"  # 默认使用PostgreSQL
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = "fastapi_backend"

    @property
    def TORTOISE_ORM(self) -> dict:
        """动态生成Tortoise ORM配置"""
        if self.DB_ENGINE == "postgres":
            return {
                "connections": {
                    "default": {
                        "engine": "tortoise.backends.asyncpg",
                        "credentials": {
                            "host": self.DB_HOST,
                            "port": self.DB_PORT,
                            "user": self.DB_USER,
                            "password": self.DB_PASSWORD,
                            "database": self.DB_NAME,
                        },
                    }
                },
                "apps": {
                    "models": {
                        "models": ["models", "aerich.models"],
                        "default_connection": "default",
                    },
                },
                "use_tz": False,
                "timezone": "Asia/Shanghai",
            }
        else:
            # SQLite fallback configuration
            return {
                "connections": {
                    "default": {
                        "engine": "tortoise.backends.sqlite",
                        "credentials": {
                            "file_path": f"{self.BASE_DIR}/db.sqlite3"
                        },
                    }
                },
                "apps": {
                    "models": {
                        "models": ["models", "aerich.models"],
                        "default_connection": "default",
                    },
                },
                "use_tz": False,
                "timezone": "Asia/Shanghai",
            }

    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    # Swagger
    SWAGGER_UI_USERNAME: str = os.getenv("SWAGGER_UI_USERNAME", "admin")
    SWAGGER_UI_PASSWORD: str = os.getenv("SWAGGER_UI_PASSWORD", "")
    COMPANY_ROLE_MAPPING: typing.Dict[str, typing.List[int]] = {"default": []}

    @field_validator("COMPANY_ROLE_MAPPING", mode="before")
    @classmethod
    def parse_company_role_mapping(cls, v):
        """解析 COMPANY_ROLE_MAPPING 环境变量"""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return {"default": []}
        return v

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 配置验证
        if not self.SECRET_KEY:
            raise ValueError(
                "SECRET_KEY 环境变量必须设置，请在.env文件中配置或使用: openssl rand -hex 32 生成"
            )
        if not self.SWAGGER_UI_PASSWORD:
            raise ValueError(
                "SWAGGER_UI_PASSWORD 环境变量必须设置，请在.env文件中配置Swagger访问密码"
            )


settings = Settings()
