"""用户认证服务 - 手机验证码方式"""

from datetime import timedelta

from jose import jwt as jose_jwt
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.utils.password_security import password_security
from app.models.user import User
from app.schemas.user import (
    TokenResponse, UserLogin, UserRegister, UserResponse,
    UserAvatarUpdate, UserNicknameUpdate, UserPasswordUpdate,
    UserLoginPassword
)
from app.crud.crud_user import crud_user
from backend.core.conf import settings
from backend.utils.timezone import timezone


class AuthService:
    """认证服务"""

    @staticmethod
    def _create_access_token(user_id: int, is_superuser: bool = False) -> str:
        """生成访问令牌"""
        expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
        to_encode = {
            "sub": str(user_id),
            "exp": expire,
            "is_superuser": is_superuser,
            "type": "access",
        }
        return jose_jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)

    @staticmethod
    def _create_refresh_token(user_id: int) -> str:
        """创建刷新令牌"""
        expire = timezone.now() + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)
        to_encode = {
            'sub': user_id,
            'type': 'refresh',
            'exp': expire,
        }
        return jose_jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)

    @staticmethod
    async def register(db: AsyncSession, data: UserRegister) -> TokenResponse:
        """用户注册（手机验证码方式）"""
        if not data.agree_protocol:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="请先同意用户使用协议和隐私政策",
            )

        # 验证验证码（开发环境固定为 123456）
        if data.code != "123456":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码错误",
            )

        # 验证手机号格式
        import re
        if not re.match(r"^\d{10,15}$", data.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="手机号格式错误",
            )

        # 检查手机号是否已注册
        existing = await db.execute(select(User).where(User.phone == data.phone))
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该手机号已注册",
            )

        # 创建用户
        user = User(
            phone=data.phone,
            nickname=f"用户{data.phone[-4:]}",
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        # 生成 token
        token = AuthService._create_access_token(user.id)
        return TokenResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )

    @staticmethod
    async def login(db: AsyncSession, data: UserLogin) -> TokenResponse:
        """用户登录（手机验证码方式）"""
        # 验证验证码
        if data.code != "123456":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码错误",
            )

        # 查找用户
        result = await db.execute(select(User).where(User.phone == data.phone))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在，请先注册",
            )

        if not user.status:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="账户已被禁用",
            )

        # 生成 token
        token = AuthService._create_access_token(user.id)
        return TokenResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )

    @staticmethod
    async def login_via_password(db: AsyncSession, data: UserLoginPassword) -> TokenResponse:
        """用户登录（密码方式）"""
        # 查找用户
        result = await db.execute(select(User).where(User.phone == data.phone))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="该手机号未注册",
            )

        if not user.status:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="账户已被禁用",
            )

        if not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该账号未设置密码，请使用验证码登录",
            )

        # 验证密码
        if not password_security.verify(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="密码错误",
            )

        # 生成 token
        token = AuthService._create_access_token(user.id)
        return TokenResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> UserResponse:
        """获取用户信息"""
        user = await crud_user.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在",
            )
        return UserResponse.model_validate(user)

    @staticmethod
    async def update_avatar(db: AsyncSession, user_id: int, data: UserAvatarUpdate) -> UserResponse:
        """更新用户头像"""
        user = await crud_user.update_avatar(db, user_id=user_id, avatar_url=data.avatar)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在",
            )
        return UserResponse.model_validate(user)

    @staticmethod
    async def update_nickname(db: AsyncSession, user_id: int, data: UserNicknameUpdate) -> UserResponse:
        """更新用户昵称"""
        user = await crud_user.update_nickname(db, user_id=user_id, nickname=data.nickname)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在",
            )
        return UserResponse.model_validate(user)

    @staticmethod
    async def set_password(db: AsyncSession, user_id: int, data: UserPasswordUpdate) -> dict:
        """设置/更新密码"""
        user = await crud_user.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在",
            )
        user.hashed_password = password_security.hash(data.password)
        await db.commit()
        return {"message": "密码设置成功"}

    @staticmethod
    async def deactivate_account(db: AsyncSession, user_id: int) -> dict:
        """注销账号"""
        await crud_user.deactivate_account(db, user_id=user_id)
        return {"message": "账号已注销"}
