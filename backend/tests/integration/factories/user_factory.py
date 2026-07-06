"""
用户数据工厂

用于在测试中快速创建用户对象。
"""

from typing import Any, ClassVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.utils.password_security import password_security

from tests.integration.factories.base import BaseFactory


class UserFactory(BaseFactory):
    """用户数据工厂"""

    _model = User
    _defaults: ClassVar[dict[str, Any]] = {}

    @classmethod
    def build(cls, **overrides: Any) -> dict[str, Any]:
        """
        构建用户数据字典。

        默认值:
            - phone: 1380013xxxx（随机）
            - nickname: 同 phone
            - hashed_password: bcrypt 加密的 "testpass123"
            - status: True
        """
        from tests.integration.utils.helpers import random_string

        phone = overrides.get('phone', f'1380013{random_string(4)}')

        data = {
            'phone': phone,
            'nickname': overrides.get('nickname', f'用户{phone[-4:]}'),
            'email': overrides.get('email'),
            'avatar': overrides.get('avatar'),
            'hashed_password': overrides.get('password')
                and password_security.hash(overrides['password'])
                or None,
            'status': overrides.get('status', True),
        }
        # 清理无效字段
        return {k: v for k, v in data.items() if v is not None or k in ('email', 'avatar', 'hashed_password')}

    @classmethod
    async def create(cls, db: AsyncSession, **overrides: Any) -> User:
        """创建用户并持久化"""
        return await super().create(db, **overrides)
