"""用户自定义贵金属销售价&回购价点差模型"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base


class MetalUserConfig(Base):
    """用户自定义贵金属销售价&回购价点差"""
    __tablename__ = "metal_user_config"

    __table_args__ = (
        Index("ix_metal_user_config_user_product", "user_id", "product_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, comment="用户ID"
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("metal_product.id"), nullable=False, comment="贵金属品种ID"
    )
    sell_add_price: Mapped[float] = mapped_column(Float, default=3.0, comment="用户自定义销售价加点（元/克）")
    buy_back_sub_price: Mapped[float] = mapped_column(Float, default=2.0, comment="用户自定义回购价减点（元/克）")
    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )
    status: Mapped[bool] = mapped_column(Boolean, default=True, comment="状态：1-启用 0-禁用")

    def __repr__(self) -> str:
        return f"<MetalUserConfig(user_id={self.user_id}, product_id={self.product_id})>"
