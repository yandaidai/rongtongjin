"""贵金属品种模型"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base


class MetalProduct(Base):
    """贵金属品种表"""
    __tablename__ = "metal_product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="品种代码，如 Au99.99")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="品种名称，如黄金99.99")
    unit: Mapped[str] = mapped_column(String(20), default="元/克", comment="计价单位")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )
    status: Mapped[bool] = mapped_column(Boolean, default=True, comment="状态：1-启用 0-禁用")

    def __repr__(self) -> str:
        return f"<MetalProduct(id={self.id}, code={self.code}, name={self.name})>"
