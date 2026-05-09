"""实时行情服务 - 包含销售价/回购价计算"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models.metal_global_config import MetalGlobalConfig
from app.models.metal_product import MetalProduct
from app.models.metal_quote import MetalQuote
from app.models.metal_user_config import MetalUserConfig
from app.schemas.metal_quote import MetalProductQuoteResponse, MetalQuoteResponse


class QuoteService:
    def __init__(self, db: Session):
        self.db = db

    def _get_spread(self, product_id: int, user_id: Optional[int] = None) -> tuple[float, float]:
        """获取点差：优先使用用户自定义配置，否则使用全局默认配置
        返回: (sell_add_price, buy_back_sub_price)
        """
        # 优先使用用户自定义配置
        if user_id:
            user_config = self.db.query(MetalUserConfig).filter(
                MetalUserConfig.user_id == user_id,
                MetalUserConfig.product_id == product_id,
                MetalUserConfig.status == True,
            ).first()
            if user_config:
                return user_config.sell_add_price, user_config.buy_back_sub_price

        # 使用全局默认配置
        global_config = self.db.query(MetalGlobalConfig).filter(
            MetalGlobalConfig.product_id == product_id,
            MetalGlobalConfig.status == True,
        ).first()
        if global_config:
            return global_config.sell_add_price, global_config.buy_back_sub_price

        # 默认值
        return 3.0, 2.0

    def get_latest_quotes(self) -> list[MetalQuoteResponse]:
        """获取所有品种的最新行情"""
        # 获取每个品种的最新行情
        from sqlalchemy import func as sqlfunc

        subquery = self.db.query(
            MetalQuote.product_id,
            sqlfunc.max(MetalQuote.quote_time).label("max_time")
        ).group_by(MetalQuote.product_id).subquery()

        quotes = self.db.query(MetalQuote).join(
            subquery,
            (MetalQuote.product_id == subquery.c.product_id) &
            (MetalQuote.quote_time == subquery.c.max_time)
        ).all()

        return [MetalQuoteResponse.model_validate(q) for q in quotes]

    def get_product_quotes(self, user_id: Optional[int] = None) -> list[MetalProductQuoteResponse]:
        """获取所有产品的报价（含销售价、回购价计算）"""
        products = self.db.query(MetalProduct).filter(
            MetalProduct.status == True
        ).all()

        result = []
        for product in products:
            # 获取该品种最新行情
            latest_quote = self.db.query(MetalQuote).filter(
                MetalQuote.product_id == product.id
            ).order_by(MetalQuote.quote_time.desc()).first()

            if not latest_quote:
                continue

            # 获取点差
            sell_add, buy_back_sub = self._get_spread(product.id, user_id)

            # 计算销售价和回购价
            sell_price = round(latest_quote.price + sell_add, 2)
            buy_back_price = round(latest_quote.price - buy_back_sub, 2)

            result.append(MetalProductQuoteResponse(
                product_id=product.id,
                product_code=product.code,
                product_name=product.name,
                market_price=latest_quote.price,
                sell_price=sell_price,
                buy_back_price=buy_back_price,
                sell_add_price=sell_add,
                buy_back_sub_price=buy_back_sub,
                rise=latest_quote.rise,
                rise_rate=latest_quote.rise_rate,
                quote_time=latest_quote.quote_time,
            ))

        return result

    def get_quote_history(self, product_id: int, limit: int = 10) -> list[MetalQuoteResponse]:
        """获取指定品种的历史行情"""
        quotes = self.db.query(MetalQuote).filter(
            MetalQuote.product_id == product_id
        ).order_by(MetalQuote.quote_time.desc()).limit(limit).all()

        return [MetalQuoteResponse.model_validate(q) for q in quotes]
