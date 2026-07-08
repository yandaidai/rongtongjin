"""贵金属品种服务"""

from typing import Optional

from sqlalchemy.orm import Session

from app.crud.crud_products import CRUDProducts
from app.models.metal_product import MetalProduct


class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.crud = CRUDProducts()

    async def get_all_products(self) -> list[MetalProduct]:
        """获取所有启用的贵金属品种"""
        products = await self.crud.get_all(self.db)
        return products

    async def get_product_by_id(self, product_id: int) -> Optional[MetalProduct]:
        """根据ID获取品种"""
        return await self.crud.get_by_id(self.db, product_id)

    async def get_product_by_code(self, code: str) -> Optional[MetalProduct]:
        """根据代码获取品种"""
        return await self.crud.get_by_code(self.db, code)
