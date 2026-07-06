"""认证相关 API 路由 - 符合需求文档"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from database.db import get_db
from app.models.user import User
from app.schemas.user import (
    TokenResponse, UserAvatarUpdate, UserLogin, UserNicknameUpdate,
    UserPasswordUpdate, UserRegister, UserResponse, UserLoginPassword
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    """手机验证码登录"""
    return await AuthService.login(db, data)


@router.post("/login/password", response_model=TokenResponse)
async def login_via_password(data: UserLoginPassword, db: AsyncSession = Depends(get_db)):
    """密码登录"""
    return await AuthService.login_via_password(db, data)


@router.post("/register", response_model=TokenResponse)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    """手机验证码注册（注册即登录）"""
    return await AuthService.register(db, data)


@router.get("/user/info", response_model=UserResponse)
async def get_user_info(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取当前用户信息"""
    return await AuthService.get_user_by_id(db, current_user.id)


@router.patch("/user/avatar", response_model=UserResponse)
async def update_avatar(
    data: UserAvatarUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """设置用户头像"""
    return await AuthService.update_avatar(db, current_user.id, data)


@router.patch("/user/nickname", response_model=UserResponse)
async def update_nickname(
    data: UserNicknameUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """设置用户昵称"""
    return await AuthService.update_nickname(db, current_user.id, data)


@router.post("/user/password")
async def set_password(
    data: UserPasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """设置密码"""
    return await AuthService.set_password(db, current_user.id, data)


@router.delete("/user/account")
async def deactivate_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """注销账号"""
    return await AuthService.deactivate_account(db, current_user.id)
