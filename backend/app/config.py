"""应用配置管理"""

import logging

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "融通金 API"
    DEBUG: bool = True

    # 数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "root"
    DB_NAME: str = "rongtongjin"
    DATABASE_URL: str = ""

    @property
    def db_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"

    # JWT 配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 小时

    @property
    def effective_secret_key(self) -> str:
        """返回有效密钥，并在使用默认值时发出警告"""
        if self.SECRET_KEY in ("", "your-secret-key-change-in-production"):
            logger.warning(
                "SECRET_KEY 使用默认值，生产环境请在 .env 或环境变量中设置 SECRET_KEY"
            )
        return self.SECRET_KEY

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
