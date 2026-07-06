import hashlib

from cryptography.fernet import Fernet


class AESCipher:
    """AES 加解密工具"""

    def __init__(self, key: str):
        self.fernet = Fernet(self._get_fernet_key(key))

    @staticmethod
    def _get_fernet_key(key: str) -> bytes:
        """将任意长度密钥转换为 32 字节的 Fernet 密钥"""
        return hashlib.sha256(key.encode()).digest()

    def encrypt(self, data: str) -> str:
        """加密"""
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """解密"""
        return self.fernet.decrypt(encrypted_data.encode()).decode()
