"""K线数据 API 路由"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.metal_kline import MetalKlineResponse
from app.services.kline_service import KlineService

router = APIRouter(prefix="/klines", tags=["K线数据"])


@router.get("/", response_model=list[MetalKlineResponse])
def get_klines(
    product_id: int = Query(..., description="贵金属品种ID"),
    k_type: str = Query("day", description="K线类型：minute-分钟, two_day-两日, day-日K, week-周K, month-月K"),
    limit: int = Query(100, description="返回条数"),
    db: Session = Depends(get_db),
):
    """获取K线数据"""
    service = KlineService(db)
    return service.get_klines(product_id, k_type, limit)


@router.get("/latest", response_model=list[MetalKlineResponse])
def get_latest_klines(
    product_id: int = Query(..., description="贵金属品种ID"),
    k_type: str = Query("minute", description="K线类型"),
    limit: int = Query(10, description="返回条数"),
    db: Session = Depends(get_db),
):
    """获取最新的N条K线记录（用于价格记录列表展示）"""
    service = KlineService(db)
    return service.get_latest_klines(product_id, k_type, limit)
