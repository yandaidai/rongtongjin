"""实时行情 Pydantic 数据模型"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MetalQuoteResponse(BaseModel):
    """实时行情响应"""
    id: int
    product_id: int
    price: float
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    rise: float
    rise_rate: float
    quote_time: datetime

    model_config = {"from_attributes": True}


class MetalProductQuoteResponse(BaseModel):
    """带点差计算的产品报价响应"""
    product_id: int
    product_code: str
    product_name: str
    market_price: float  # 大盘价
    sell_price: float    # 销售价 = 大盘价 + 销售价点差
    buy_back_price: float  # 回购价 = 大盘价 - 回购价点差
    sell_add_price: float  # 销售价点差
    buy_back_sub_price: float  # 回购价点差
    rise: float
    rise_rate: float
    quote_time: datetime
