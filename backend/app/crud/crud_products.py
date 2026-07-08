"""
贵金属品种CRUD
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.metal_product import MetalProduct


class CRUDProducts:
    """贵金属品种数据库操作"""

    async def get_all(self, db: AsyncSession) -> list[MetalProduct]:
        """获取所有启用的贵金属品种"""
        result = await db.execute(select(MetalProduct).where(MetalProduct.status == True))
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, product_id: int) -> MetalProduct | None:
        """根据 ID 获取贵金属品种"""
        result = await db.execute(select(MetalProduct).where(MetalProduct.id == product_id))
        return result.scalar_one_or_none()

    async def get_by_code(self, db: AsyncSession, code: str) -> MetalProduct | None:
        """根据代码获取贵金属品种"""
        result = await db.execute(select(MetalProduct).where(MetalProduct.code == code))
        return result.scalar_one_or_none()