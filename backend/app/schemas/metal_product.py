"""贵金属品种 Pydantic 数据模型"""

from datetime import datetime

from pydantic import BaseModel


class MetalProductResponse(BaseModel):
    """贵金属品种响应"""
    id: int
    code: str
    name: str
    unit: str
    status: bool
    created_at: datetime

    model_config = {"from_attributes": True}
