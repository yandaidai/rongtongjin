"""
密码安全工具

使用 bcrypt 算法进行密码哈希和验证
"""

from pwdlib import PasswordHash

from pwdlib.hashers.bcrypt import BcryptHasher


class PasswordSecurity:
    """密码安全工具类"""

    def __init__(self):
        self._password_hash = PasswordHash([BcryptHasher()])

    def hash(self, password: str) -> str:
        """哈希密码"""
        return self._password_hash.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return self._password_hash.verify(plain_password, hashed_password)

    def needs_update(self, hashed_password: str) -> bool:
        """检查密码是否需要更新哈希算法"""
        return self._password_hash.needs_update(hashed_password)


# 全局密码安全实例
password_security = PasswordSecurity()
