"""实时行情 API 路由 - 包含销售价、回购价、点差"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_optional
from app.database import get_db
from app.models.user import User
from app.schemas.metal_quote import MetalProductQuoteResponse, MetalQuoteResponse
from app.services.quote_service import QuoteService

router = APIRouter(prefix="/quotes", tags=["实时行情"])


@router.get("/", response_model=list[MetalProductQuoteResponse])
def get_quotes(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """获取所有产品的实时行情（含销售价、回购价、点差）
    如果用户已登录，会优先使用用户自定义点差配置
    """
    service = QuoteService(db)
    user_id = current_user.id if current_user else None
    return service.get_product_quotes(user_id=user_id)


@router.get("/history", response_model=list[MetalQuoteResponse])
def get_quote_history(
    product_id: int = Query(..., description="贵金属品种ID"),
    limit: int = Query(10, description="返回条数"),
    db: Session = Depends(get_db),
):
    """获取指定品种的历史行情"""
    service = QuoteService(db)
    return service.get_quote_history(product_id, limit)
