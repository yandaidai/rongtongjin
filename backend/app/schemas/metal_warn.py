"""用户价格预警 Pydantic 数据模型"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MetalWarnResponse(BaseModel):
    """用户价格预警响应"""
    id: int
    user_id: int
    product_id: int
    upper_limit: Optional[float] = None
    lower_limit: Optional[float] = None
    warn_enable: bool
    upper_trigger: bool
    lower_trigger: bool
    create_time: datetime

    model_config = {"from_attributes": True}


class MetalWarnCreate(BaseModel):
    """创建价格预警"""
    product_id: int
    upper_limit: Optional[float] = None
    lower_limit: Optional[float] = None
    warn_enable: bool = True


class MetalWarnUpdate(BaseModel):
    """更新价格预警"""
    upper_limit: Optional[float] = None
    lower_limit: Optional[float] = None
    warn_enable: Optional[bool] = None
