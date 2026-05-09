"""认证相关 API 路由 - 符合需求文档"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.user import (
    TokenResponse, UserAvatarUpdate, UserLogin, UserNicknameUpdate,
    UserPasswordUpdate, UserRegister, UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """手机验证码登录"""
    service = AuthService(db)
    return service.login(data)


@router.post("/register", response_model=TokenResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """手机验证码注册（注册即登录）"""
    service = AuthService(db)
    return service.register(data)


@router.get("/user/info", response_model=UserResponse)
def get_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserResponse.model_validate(current_user)


@router.patch("/user/avatar", response_model=UserResponse)
def update_avatar(
    data: UserAvatarUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """设置用户头像"""
    service = AuthService(db)
    return service.update_avatar(current_user.id, data)


@router.patch("/user/nickname", response_model=UserResponse)
def update_nickname(
    data: UserNicknameUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """设置用户昵称"""
    service = AuthService(db)
    return service.update_nickname(current_user.id, data)


@router.post("/user/password")
def set_password(
    data: UserPasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """设置密码"""
    service = AuthService(db)
    return service.set_password(current_user.id, data)


@router.delete("/user/account")
def deactivate_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """注销账号"""
    service = AuthService(db)
    return service.deactivate_account(current_user.id)
