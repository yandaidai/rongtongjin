from datetime import datetime
from typing import Annotated

from sqlalchemy import BigInteger, DateTime, Text, TypeDecorator
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, declared_attr, mapped_column

from backend.common.enums import DataBaseType
from backend.core.conf import settings
from backend.utils.timezone import timezone

# 通用主键类型
id_key = Annotated[
    int,
    mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        index=True,
        autoincrement=True,
        sort_order=-999,
        comment='主键 ID',
    ),
]


class UniversalText(TypeDecorator[str]):
    """MySQL 长文本类型"""

    impl = LONGTEXT
    cache_ok = True

    def process_bind_param(self, value: str | None, dialect) -> str | None:  # noqa: ANN001
        return value

    def process_result_value(self, value: str | None, dialect) -> str | None:  # noqa: ANN001
        return value


class TimeZone(TypeDecorator[datetime]):
    """MySQL 时区感知类型"""

    impl = DateTime(timezone=True)
    cache_ok = True

    @property
    def python_type(self) -> type[datetime]:
        return datetime

    def process_bind_param(self, value: datetime | None, dialect) -> datetime | None:  # noqa: ANN001
        if value is not None and value.utcoffset() != timezone.now().utcoffset():
            value = timezone.from_datetime(value)
        return value

    def process_result_value(self, value: datetime | None, dialect) -> datetime | None:  # noqa: ANN001
        if value is not None and value.tzinfo is None:
            value = value.replace(tzinfo=timezone.tz_info)
        return value


class DateTimeMixin(MappedAsDataclass):
    """日期时间 Mixin"""

    created_time: Mapped[datetime] = mapped_column(
        TimeZone,
        init=False,
        default_factory=timezone.now,
        sort_order=999,
        comment='创建时间',
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        TimeZone,
        init=False,
        onupdate=timezone.now,
        sort_order=999,
        comment='更新时间',
    )


class MappedBase(AsyncAttrs, DeclarativeBase):
    """
    声明式基类，自动生成 __tablename__

    SQLAlchemy 2.0 Async + DeclarativeBase 模式
    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower()

    @declared_attr.directive
    def __table_args__(self) -> dict:
        return {'comment': self.__doc__ or ''}


class Base(MappedBase):
    """标准表基类"""

    __abstract__ = True
