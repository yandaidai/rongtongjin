"""用户价格预警模型"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MetalWarn(Base):
    """用户价格预警表"""
    __tablename__ = "metal_warn"

    __table_args__ = (
        Index("ix_metal_warn_user_product", "user_id", "product_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, comment="用户ID"
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("metal_product.id"), nullable=False, comment="贵金属品种ID"
    )
    upper_limit: Mapped[float] = mapped_column(Float, nullable=True, comment="最高阀值")
    lower_limit: Mapped[float] = mapped_column(Float, nullable=True, comment="最低阀值")
    warn_enable: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否启用预警")
    upper_trigger: Mapped[bool] = mapped_column(Boolean, default=False, comment="最高阀值是否已触发")
    lower_trigger: Mapped[bool] = mapped_column(Boolean, default=False, comment="最低阀值是否已触发")
    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    def __repr__(self) -> str:
        return f"<MetalWarn(user_id={self.user_id}, product_id={self.product_id})>"
