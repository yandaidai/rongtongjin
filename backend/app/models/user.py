"""用户模型 - 符合需求文档"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, comment="手机号")
    nickname: Mapped[str] = mapped_column(String(50), nullable=True, comment="用户昵称")
    avatar: Mapped[str] = mapped_column(String(255), nullable=True, comment="用户头像URL")
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=True, comment="密码哈希（可为空，验证码注册用户可后续设置）")
    status: Mapped[bool] = mapped_column(Boolean, default=True, comment="状态：1-正常 0-禁用")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, phone={self.phone})>"
