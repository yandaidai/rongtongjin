"""实时行情服务 - 从 akshare 获取贵金属大盘价，计算销售价/回购价"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models.metal_global_config import MetalGlobalConfig
from app.models.metal_product import MetalProduct
from app.models.metal_quote import MetalQuote
from app.models.metal_user_config import MetalUserConfig
from app.schemas.metal_quote import MetalProductQuoteResponse, MetalQuoteResponse
from app.services.akshare_service import AkshareQuote, AkshareService


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

    def _get_akshare_quote(self, product_code: str) -> Optional[AkshareQuote]:
        """从 akshare 获取品种的实时行情"""
        # 先尝试 SGE 行情
        quote = AkshareService.get_sge_quote(product_code)
        if quote:
            return quote

        # 如果 SGE 没有，尝试国际行情
        # 根据品种代码映射到国际行情名称
        international_map = {
            "XAU": "COMEX黄金",       # 国际现货黄金 -> COMEX黄金当月连续
            "XAG": "COMEX白银",       # 国际现货白银 -> COMEX白银当月连续
            "XPT": "NYMEX铂金",       # 国际现货铂金 -> NYMEX铂金当月连续
        }
        if product_code in international_map:
            return AkshareService.get_international_quote(international_map[product_code])

        return None

    # 国内品种代码集（对应上海黄金交易所品种）
    DOMESTIC_CODES = {"Au99.99", "Au99.95", "Au100g", "Pt99.95", "Ag(T+D)", "Au(T+D)", "mAu(T+D)", "Ag99.99"}

    # 国际品种代码映射
    INTERNATIONAL_CODE_MAP = {
        "XAU": "COMEX黄金",
        "XAG": "COMEX白银",
        "XPT": "NYMEX铂金",
    }

    def get_quotes_by_category(
        self, category: str, user_id: Optional[int] = None
    ) -> list[MetalProductQuoteResponse]:
        """按类别获取行情报价"""
        products = self.db.query(MetalProduct).filter(
            MetalProduct.status == True,
        ).all()

        if category == "domestic":
            products = [p for p in products if p.code in self.DOMESTIC_CODES]
        elif category == "international":
            products = [p for p in products if p.code in self.INTERNATIONAL_CODE_MAP]
        # else "all" — return everything

        result = []
        for product in products:
            akshare_quote = self._get_akshare_quote(product.code)
            if not akshare_quote:
                continue

            sell_add, buy_back_sub = self._get_spread(product.id, user_id)
            sell_price = round(akshare_quote.price + sell_add, 2)
            buy_back_price = round(akshare_quote.price - buy_back_sub, 2)

            result.append(MetalProductQuoteResponse(
                product_id=product.id,
                product_code=product.code,
                product_name=product.name,
                market_price=akshare_quote.price,
                sell_price=sell_price,
                buy_back_price=buy_back_price,
                sell_add_price=sell_add,
                buy_back_sub_price=buy_back_sub,
                rise=akshare_quote.rise or 0.0,
                rise_rate=akshare_quote.rise_rate or 0.0,
                quote_time=akshare_quote.quote_time or datetime.now(timezone.utc),
            ))

        return result

    def get_product_quotes(self, user_id: Optional[int] = None) -> list[MetalProductQuoteResponse]:
        """获取所有产品的报价（含销售价、回购价计算）"""
        return self.get_quotes_by_category("all", user_id)

    def get_quote_history(self, product_id: int, limit: int = 10) -> list[MetalQuoteResponse]:
        """获取指定品种的历史行情"""
        quotes = self.db.query(MetalQuote).filter(
            MetalQuote.product_id == product_id
        ).order_by(MetalQuote.quote_time.desc()).limit(limit).all()

        return [MetalQuoteResponse.model_validate(q) for q in reversed(quotes)]
