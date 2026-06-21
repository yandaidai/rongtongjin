"""用户相关 Pydantic 数据模型 - 符合需求文档"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserRegister(BaseModel):
    """用户注册请求（手机验证码方式）"""
    phone: str
    code: str  # 验证码
    agree_protocol: bool = False  # 是否同意用户使用协议和隐私政策


class UserLogin(BaseModel):
    """用户登录请求（手机验证码方式）"""
    phone: str
    code: str  # 验证码


class UserLoginPassword(BaseModel):
    """用户登录请求（密码方式）"""
    phone: str
    password: str
    agree_protocol: bool = False  # 是否同意用户使用协议和隐私政策


class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    phone: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    status: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Token 响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserAvatarUpdate(BaseModel):
    """更新用户头像"""
    avatar: str


class UserNicknameUpdate(BaseModel):
    """更新用户昵称"""
    nickname: str


class UserPasswordUpdate(BaseModel):
    """设置/更新密码"""
    password: str
