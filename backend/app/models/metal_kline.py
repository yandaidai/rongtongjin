"""K线数据模型"""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MetalKline(Base):
    """K线数据表"""
    __tablename__ = "metal_kline"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("metal_product.id"), nullable=False, comment="贵金属品种ID"
    )
    k_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="K线类型：minute-分钟, two_day-两日, day-日K, week-周K, month-月K")
    open_price: Mapped[float] = mapped_column(Float, nullable=False, comment="开盘价")
    high_price: Mapped[float] = mapped_column(Float, nullable=False, comment="最高价")
    low_price: Mapped[float] = mapped_column(Float, nullable=False, comment="最低价")
    close_price: Mapped[float] = mapped_column(Float, nullable=False, comment="收盘价")
    volume: Mapped[float] = mapped_column(Float, default=0.0, comment="成交量")
    k_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, comment="K线时间"
    )
    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="创建时间"
    )

    def __repr__(self) -> str:
        return f"<MetalKline(product_id={self.product_id}, k_type={self.k_type}, k_time={self.k_time})>"
