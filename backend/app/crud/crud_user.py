"""
用户CRUD
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.utils.password_security import password_security


class CRUDUser:
    """用户数据库操作"""

    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        """根据 ID 获取用户"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_by_phone(self, db: AsyncSession, phone: str) -> User | None:
        """根据手机号获取用户"""
        result = await db.execute(select(User).where(User.phone == phone))
        return result.scalar_one_or_none()
    
    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        """根据用户名获取用户"""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        """根据邮箱获取用户"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, phone_number: str) -> User:
        """创建用户"""
        user = User(
            phone_number=phone_number,
            nickname=f"用户{phone_number[-4:]}",  # 默认昵称为用户+手机号后4位
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    async def update_profile(self, db: AsyncSession, user_id: int, **kwargs) -> User | None:
        """更新用户资料"""
        user = await self.get_by_id(db, user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)

        await db.flush()
        await db.refresh(user)
        return user
    
    async def update_avatar(self, db: AsyncSession, user_id: int, avatar_url: str) -> User | None:
        """更新用户头像"""
        user = await self.get_by_id(db, user_id)
        if not user:
            return None
        
        user.avatar = avatar_url

        await db.flush()
        await db.refresh(user)
        return user
    
    async def update_nickname(self, db: AsyncSession, user_id: int, nickname: str) -> User | None:
        """更新用户昵称"""
        user = await self.get_by_id(db, user_id)
        if not user:
            return None
        
        user.nickname = nickname

        await db.flush()
        await db.refresh(user)
        return user

    async def update_password(self, db: AsyncSession, user_id: int, new_password: str) -> bool:
        """更新用户密码"""
        user = await self.get_by_id(db, user_id)
        if not user:
            return None
        
        hashed_password = password_security.hash(new_password)
        user.password = hashed_password

        await db.flush()
        await db.refresh(user)
        return True

    async def authenticate(self, db: AsyncSession, username: str, password: str) -> User | None:
        """验证用户凭据"""
        user = await self.get_by_username(db, username)
        if not user:
            return None
        if not password_security.verify(password, user.password):
            return None
        return user
    
    async def deactivate_account(self, db: AsyncSession, user_id: int) -> bool:
        """注销用户账号"""
        user = await self.get_by_id(db, user_id)
        if not user:
            return None
        
        user.status = False  # 设置用户状态为禁用

        await db.flush()
        await db.refresh(user)
        return True


# CRUD 单例
crud_user = CRUDUser()
