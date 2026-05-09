"""贵金属品种服务"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.metal_product import MetalProduct
from app.schemas.metal_product import MetalProductResponse


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_products(self) -> list[MetalProductResponse]:
        """获取所有启用的贵金属品种"""
        products = self.db.query(MetalProduct).filter(
            MetalProduct.status == True
        ).all()
        return [MetalProductResponse.model_validate(p) for p in products]

    def get_product_by_id(self, product_id: int) -> Optional[MetalProduct]:
        """根据ID获取品种"""
        return self.db.query(MetalProduct).filter(
            MetalProduct.id == product_id,
            MetalProduct.status == True,
        ).first()

    def get_product_by_code(self, code: str) -> Optional[MetalProduct]:
        """根据代码获取品种"""
        return self.db.query(MetalProduct).filter(
            MetalProduct.code == code,
            MetalProduct.status == True,
        ).first()
