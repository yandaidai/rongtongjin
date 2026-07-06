"""
测试助手工具

提供断言封装、响应解析、随机数据生成等工具函数。
遵循 Arrange-Act-Assert 模式的 Assert 部分复用。
"""

from typing import Any


# ============================================================
# 测试数据生成
# ============================================================

import random
import string


def random_string(length: int = 10) -> str:
    """生成指定长度的随机字母数字字符串"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def random_email() -> str:
    """生成随机邮箱地址"""
    return f'{random_string(8)}@test.com'


def random_username() -> str:
    """生成随机用户名"""
    return f'test_user_{random_string(6)}'
