from enum import Enum
from enum import IntEnum as SourceIntEnum
from typing import Any


class _EnumBase:
    """枚举基类，提供通用方法"""

    @classmethod
    def get_member_keys(cls) -> list[str]:
        return list(cls.__members__.keys())

    @classmethod
    def get_member_values(cls) -> list:
        return [item.value for item in cls.__members__.values()]


class IntEnum(_EnumBase, SourceIntEnum):
    """整型枚举基类"""


class StrEnum(_EnumBase, str, Enum):
    """字符串枚举基类"""


class StatusType(IntEnum):
    """状态类型"""
    disable = 0
    enable = 1


class MethodType(StrEnum):
    """HTTP 请求方法"""
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    OPTIONS = 'OPTIONS'


class LoginLogStatusType(IntEnum):
    """登录日志状态"""
    fail = 0
    success = 1


class DataBaseType(StrEnum):
    """数据库类型"""
    mysql = 'mysql'
