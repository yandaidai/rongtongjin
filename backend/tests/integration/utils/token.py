"""
测试用 JWT Token 生成工具

提供在测试中直接生成 Token 的辅助函数，无需走完整的登录流程。
主要用于需要认证的接口测试。
"""

from datetime import timedelta

from jose import jwt as jose_jwt

from backend.utils.timezone import timezone
from backend.core.conf import settings


def create_test_access_token(
    user_id: int = 1,
    username: str = 'testuser',
    nickname: str = 'Test User',
    is_superuser: bool = False,
    **extra_claims,
) -> str:
    """
    生成测试用 access_token。

    可用于跳过登录流程，直接测试需要认证的接口。

    Args:
        user_id: 用户 ID
        username: 用户名
        nickname: 昵称
        is_superuser: 是否为超级管理员
        **extra_claims: 额外的 JWT claims

    Returns:
        JWT access_token 字符串
    """
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
    to_encode = {
        'sub': user_id,
        'username': username,
        'nickname': nickname,
        'is_superuser': is_superuser,
        'type': 'access',
        'exp': expire,
        **extra_claims,
    }
    return jose_jwt.encode(
        to_encode,
        settings.TOKEN_SECRET_KEY,
        algorithm=settings.TOKEN_ALGORITHM,
    )


def create_test_refresh_token(user_id: int = 1) -> str:
    """
    生成测试用 refresh_token。

    Args:
        user_id: 用户 ID

    Returns:
        JWT refresh_token 字符串
    """
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)
    to_encode = {
        'sub': user_id,
        'type': 'refresh',
        'exp': expire,
    }
    return jose_jwt.encode(
        to_encode,
        settings.TOKEN_SECRET_KEY,
        algorithm=settings.TOKEN_ALGORITHM,
    )


def create_expired_access_token(user_id: int = 1) -> str:
    """
    生成已过期的 access_token，用于测试 Token 过期场景。

    Args:
        user_id: 用户 ID

    Returns:
        已过期的 JWT access_token 字符串
    """
    expire = timezone.now() - timedelta(seconds=10)
    to_encode = {
        'sub': user_id,
        'type': 'access',
        'exp': expire,
    }
    return jose_jwt.encode(
        to_encode,
        settings.TOKEN_SECRET_KEY,
        algorithm=settings.TOKEN_ALGORITHM,
    )


def create_malformed_token() -> str:
    """生成格式错误的 Token，用于测试异常场景"""
    return 'this.is.not.a.valid.jwt'
