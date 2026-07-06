"""
工厂基类

提供通用的数据构建方法，子类只需实现 _defaults 和 _create 即可。
"""

import copy
from typing import Any, ClassVar

from sqlalchemy.ext.asyncio import AsyncSession


class BaseFactory:
    """
    数据工厂基类

    使用方式:
        # 构建但不持久化
        user_data = UserFactory.build(**overrides)

        # 构建并持久化到数据库
        user = await UserFactory.create(db_session, **overrides)

    子类需定义:
        - _model: SQLAlchemy 模型类
        - _defaults: ClassVar[dict] 默认属性
    """

    _model: Any = None  # 子类需指定 SQLAlchemy 模型类
    _defaults: ClassVar[dict[str, Any]] = {}  # 子类需指定默认属性

    @classmethod
    def build(cls, **overrides: Any) -> dict[str, Any]:
        """
        构建字典格式的数据（不持久化）。

        参数合并规则: overrides > _defaults
        """
        data = copy.deepcopy(cls._defaults)
        data.update(overrides)
        return data

    @classmethod
    async def create(cls, db: AsyncSession, **overrides: Any) -> Any:
        """
        构建并持久化到数据库。

        Args:
            db: 数据库 AsyncSession
            **overrides: 覆盖默认值的字段

        Returns:
            持久化后的模型实例
        """
        data = cls.build(**overrides)
        instance = cls._model(**data)
        db.add(instance)
        await db.flush()
        await db.refresh(instance)
        return instance

    @classmethod
    async def create_batch(cls, db: AsyncSession, count: int = 3, **overrides: Any) -> list[Any]:
        """
        批量创建多条数据。

        Args:
            db: 数据库 AsyncSession
            count: 创建数量
            **overrides: 所有实例共享的覆盖字段

        Returns:
            持久化后的模型实例列表
        """
        instances = []
        for _ in range(count):
            instance_overrides = {k: v(_) if callable(v) else v for k, v in overrides.items()}
            instance = await cls.create(db, **instance_overrides)
            instances.append(instance)
        return instances
