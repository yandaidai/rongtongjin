"""实时行情模型"""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MetalQuote(Base):
    """实时行情表"""
    __tablename__ = "metal_quote"

    __table_args__ = (
        Index("ix_metal_quote_product_time", "product_id", "quote_time"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("metal_product.id"), nullable=False, comment="贵金属品种ID"
    )
    price: Mapped[float] = mapped_column(Float, nullable=False, comment="大盘价（元/克）")
    open: Mapped[float] = mapped_column(Float, nullable=True, comment="开盘价")
    high: Mapped[float] = mapped_column(Float, nullable=True, comment="最高价")
    low: Mapped[float] = mapped_column(Float, nullable=True, comment="最低价")
    rise: Mapped[float] = mapped_column(Float, default=0.0, comment="涨跌额")
    rise_rate: Mapped[float] = mapped_column(Float, default=0.0, comment="涨跌幅%")
    quote_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, comment="行情时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    def __repr__(self) -> str:
        return f"<MetalQuote(product_id={self.product_id}, price={self.price})>"
