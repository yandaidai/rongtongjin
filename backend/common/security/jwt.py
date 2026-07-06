"""
JWT 工具函数

创建和验证 JWT Token
"""

from datetime import timedelta

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt as jose_jwt

from backend.common.exception import errors
from backend.core.conf import settings
from backend.utils.timezone import timezone

# Bearer Token 提取器
bearer_scheme = HTTPBearer(auto_error=False)


async def create_access_token(
    user_id: int,
    username: str,
    nickname: str = '',
    is_superuser: bool = False,
) -> str:
    """创建访问令牌"""
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
    to_encode = {
        'sub': user_id,
        'username': username,
        'nickname': nickname,
        'is_superuser': is_superuser,
        'type': 'access',
        'exp': expire,
    }
    return jose_jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)


async def create_refresh_token(user_id: int) -> str:
    """创建刷新令牌"""
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)
    to_encode = {
        'sub': user_id,
        'type': 'refresh',
        'exp': expire,
    }
    return jose_jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)


async def jwt_authentication(request: Request, token: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> str:
    """
    JWT 认证依赖注入

    从 Header 或 Cookie 中提取 Token 并验证
    """
    # 从 Header 获取
    token_str = token.credentials if token else None

    # 从 Cookie 获取
    if not token_str:
        token_str = request.cookies.get(settings.COOKIE_REFRESH_TOKEN_KEY)

    if not token_str:
        raise errors.TokenError(msg='未提供认证令牌')

    return token_str


DependsJwtAuth = Depends(jwt_authentication)
