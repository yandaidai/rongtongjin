"""通用工具函数"""

import random
from datetime import datetime


def generate_order_no(prefix: str = "RTJ") -> str:
    """生成订单号：前缀 + 日期时间 + 随机数"""
    now = datetime.now()
    date_str = now.strftime("%Y%m%d%H%M%S")
    rand_str = str(random.randint(1000, 9999))
    return f"{prefix}{date_str}{rand_str}"


def hash_password(password: str) -> str:
    """简单的密码哈希函数（生产环境请使用更安全的算法，如 bcrypt）"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

