"""贵金属品种 API 路由"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from app.schemas.metal_product import MetalProductResponse
from app.services.product_service import ProductService
from common.response.response_schema import ResponseModel


router = APIRouter(prefix="/products", tags=["贵金属品种"])


@router.get(
    "/",
    response_model=ResponseModel[List[MetalProductResponse]],
    summary="获取所有启用的贵金属品种",)
async def get_products(db: Session = Depends(get_db)):
    """获取所有启用的贵金属品种"""
    service = ProductService(db)
    products = await service.get_all_products()
    return ResponseModel.success(
        data=products,
        msg="获取品种成功" if products else "暂无启用的品种"
    )