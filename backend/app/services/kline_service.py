"""K线数据服务"""

from sqlalchemy.orm import Session

from app.models.metal_kline import MetalKline
from app.schemas.metal_kline import MetalKlineResponse


class KlineService:
    def __init__(self, db: Session):
        self.db = db

    def get_klines(
        self,
        product_id: int,
        k_type: str,
        limit: int = 100,
    ) -> list[MetalKlineResponse]:
        """获取K线数据"""
        klines = self.db.query(MetalKline).filter(
            MetalKline.product_id == product_id,
            MetalKline.k_type == k_type,
        ).order_by(MetalKline.k_time.desc()).limit(limit).all()

        # 按时间正序返回
        klines.reverse()
        return [MetalKlineResponse.model_validate(k) for k in klines]

    def get_latest_klines(
        self,
        product_id: int,
        k_type: str,
        limit: int = 10,
    ) -> list[MetalKlineResponse]:
        """获取最新的N条K线记录（用于价格记录列表展示）"""
        klines = self.db.query(MetalKline).filter(
            MetalKline.product_id == product_id,
            MetalKline.k_type == k_type,
        ).order_by(MetalKline.k_time.desc()).limit(limit).all()

        # 按时间正序返回
        klines.reverse()
        return [MetalKlineResponse.model_validate(k) for k in klines]
