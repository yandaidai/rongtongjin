"""贵金属品种 API 路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.db import get_db
from app.schemas.metal_product import MetalProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["贵金属品种"])


@router.get("/", response_model=list[MetalProductResponse])
async def get_products(db: Session = Depends(get_db)):
    """获取所有启用的贵金属品种"""
    service = ProductService(db)
    try:
        return service.get_all_products()
    except Exception as e:
        print(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch products")