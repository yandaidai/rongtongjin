"""贵金属品种 API 路由"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.metal_product import MetalProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["贵金属品种"])


@router.get("/", response_model=list[MetalProductResponse])
def get_products(db: Session = Depends(get_db)):
    """获取所有启用的贵金属品种"""
    service = ProductService(db)
    return service.get_all_products()
