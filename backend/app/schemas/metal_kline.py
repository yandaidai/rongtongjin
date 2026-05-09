"""K线数据 Pydantic 数据模型"""

from datetime import datetime

from pydantic import BaseModel


class MetalKlineResponse(BaseModel):
    """K线数据响应"""
    id: int
    product_id: int
    k_type: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    k_time: datetime

    model_config = {"from_attributes": True}


class MetalKlineListResponse(BaseModel):
    """K线数据列表响应"""
    items: list[MetalKlineResponse]
    total: int
