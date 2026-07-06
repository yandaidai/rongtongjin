"""
认证 Fixtures

提供测试用户、Token 等认证相关的异步 fixture。
"""

from typing import Any

import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


@pytest_asyncio.fixture(scope="function")
async def auth_empty_db() -> dict[str, Any]:
    """空数据库环境"""
    return {
        "unregistered_phone": "13800138000",
    }


@pytest_asyncio.fixture(scope="function")
async def auth_user_without_password(db: AsyncSession) -> dict[str, Any]:
    """已注册但未设置密码的用户"""
    await db.execute(delete(User))
    user = User(phone="13800138001", nickname="无密码用户")
    db.add(user)
    await db.flush()
    return {
        "phone": user.phone,
        "nickname": user.nickname,
    }
