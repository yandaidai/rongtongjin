"""默认贵金属点差配置 Pydantic 数据模型"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MetalGlobalConfigResponse(BaseModel):
    """默认点差配置响应"""
    id: int
    product_id: int
    sell_add_price: float
    buy_back_sub_price: float
    status: bool
    create_time: datetime

    model_config = {"from_attributes": True}


class MetalGlobalConfigUpdate(BaseModel):
    """更新默认点差配置"""
    sell_add_price: Optional[float] = None
    buy_back_sub_price: Optional[float] = None
