"""用户认证服务 - 手机验证码方式"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import (
    TokenResponse, UserLogin, UserRegister, UserResponse,
    UserAvatarUpdate, UserNicknameUpdate, UserPasswordUpdate,
)


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def _generate_code(self) -> str:
        """模拟生成验证码（生产环境接入真实短信服务）"""
        return "123456"  # 开发环境固定验证码

    def _verify_code(self, code: str) -> bool:
        """验证验证码（生产环境接入真实短信服务）"""
        # 开发环境：固定验证码 123456
        return code == "123456"
    
    def _verify_phone_format(self, phone: str) -> bool:
        """验证手机号格式"""
        import re
        pattern = re.compile(r"^\d{10,15}$")  # 简单的手机号格式验证
        return bool(pattern.match(phone))

    def register(self, data: UserRegister) -> TokenResponse:
        """用户注册（手机验证码方式）"""
        if not data.agree_protocol:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="请先同意用户使用协议和隐私政策",
            )

        # 验证验证码
        if not self._verify_code(data.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码错误",
            )
    
        # 验证手机号格式
        if not self._verify_phone_format(data.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="手机号格式错误",
            )

        # 检查手机号是否已注册
        existing_user = self.db.query(User).filter(User.phone == data.phone).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该手机号已注册",
            )

        # 创建用户
        user = User(
            phone=data.phone,
            nickname=f"用户{data.phone[-4:]}",  # 默认昵称：用户+手机号后4位
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        # 生成 token
        token = create_access_token(data={"sub": user.id})
        return TokenResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )

    def login(self, data: UserLogin) -> TokenResponse:
        """用户登录（手机验证码方式）"""
        # 验证验证码
        if not self._verify_code(data.phone, data.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码错误",
            )

        # 查找用户
        user = self.db.query(User).filter(User.phone == data.phone).first()
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
        token = create_access_token(data={"sub": user.id})
        return TokenResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )

    def get_user_by_id(self, user_id: int) -> UserResponse:
        """获取用户信息"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在",
            )
        return UserResponse.model_validate(user)

    def update_avatar(self, user_id: int, data: UserAvatarUpdate) -> UserResponse:
        """更新用户头像"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在",
            )
        user.avatar = data.avatar
        self.db.commit()
        self.db.refresh(user)
        return UserResponse.model_validate(user)

    def update_nickname(self, user_id: int, data: UserNicknameUpdate) -> UserResponse:
        """更新用户昵称"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在",
            )
        user.nickname = data.nickname
        self.db.commit()
        self.db.refresh(user)
        return UserResponse.model_validate(user)

    def set_password(self, user_id: int, data: UserPasswordUpdate) -> dict:
        """设置/更新密码"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在",
            )
        user.hashed_password = hash_password(data.password)
        self.db.commit()
        return {"message": "密码设置成功"}

    def deactivate_account(self, user_id: int) -> dict:
        """注销账号"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在",
            )
        user.status = False
        self.db.commit()
        return {"message": "账号已注销"}
