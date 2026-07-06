"""akshare 贵金属行情服务 - 从 akshare 获取实时贵金属价格"""

import logging
from datetime import datetime, timezone
from typing import Optional

import akshare as ak  # type: ignore[import-untyped]
import pandas as pd

from app.constants import SGE_SYMBOLS

logger = logging.getLogger(__name__)


class AkshareQuote:
    """单个品种的实时行情数据"""
    def __init__(
        self,
        product_code: str,
        price: float,
        open: Optional[float] = None,
        high: Optional[float] = None,
        low: Optional[float] = None,
        rise: Optional[float] = None,
        rise_rate: Optional[float] = None,
        quote_time: Optional[datetime] = None,
    ):
        self.product_code = product_code
        self.price = price
        self.open = open
        self.high = high
        self.low = low
        self.rise = rise
        self.rise_rate = rise_rate
        self.quote_time = quote_time or datetime.now(timezone.utc)


class AkshareService:
    """akshare 贵金属行情服务"""

    # 符号映射从 constants.py 统一管理
    SGE_SYMBOLS = SGE_SYMBOLS

    @staticmethod
    def get_sge_quote(product_code: str) -> Optional[AkshareQuote]:
        """获取上海黄金交易所指定品种的实时行情"""
        symbol = SGE_SYMBOLS.get(product_code)
        if not symbol:
            return None

        try:
            df = ak.spot_quotations_sge(symbol=symbol)
            if df.empty:
                logger.warning("akshare SGE 返回空数据: %s", product_code)
                return None

            # 取最新一条数据
            latest = df.iloc[-1]
            price = float(latest["现价"])

            # 解析更新时间
            update_time_str = latest.get("更新时间", "")
            quote_time = None
            if update_time_str:
                try:
                    quote_time = datetime.strptime(
                        update_time_str, "%Y年%m月%d日 %H:%M:%S"
                    )
                except ValueError:
                    quote_time = datetime.now(timezone.utc)

            return AkshareQuote(
                product_code=product_code,
                price=price,
                quote_time=quote_time,
            )
        except Exception:
            logger.exception("akshare SGE 查询失败: %s", product_code)
            return None

    @staticmethod
    def get_all_sge_quotes() -> dict[str, AkshareQuote]:
        """获取所有 SGE 品种的实时行情"""
        result = {}
        for code in SGE_SYMBOLS:
            quote = AkshareService.get_sge_quote(code)
            if quote:
                result[code] = quote
        return result

    @staticmethod
    def get_international_quote(name_keyword: str) -> Optional[AkshareQuote]:
        """获取国际贵金属行情（从 futures_global_spot_em）

        Args:
            name_keyword: 品种名称关键词，如 'COMEX黄金', 'COMEX白银', 'NYMEX铂金'
        """
        try:
            df = ak.futures_global_spot_em()
            if df.empty:
                logger.warning("akshare 国际行情返回空数据: %s", name_keyword)
                return None

            # 查找当月连续合约（名称完全匹配）
            mask = df["名称"] == name_keyword
            if not mask.any():
                logger.warning("akshare 未找到国际行情品种: %s", name_keyword)
                return None

            row = df[mask].iloc[0]
            price = float(row["最新价"])
            open_price = float(row["今开"]) if pd.notna(row.get("今开")) else None
            high = float(row["最高"]) if pd.notna(row.get("最高")) else None
            low = float(row["最低"]) if pd.notna(row.get("最低")) else None
            rise = float(row["涨跌额"]) if pd.notna(row.get("涨跌额")) else None
            rise_rate = float(row["涨跌幅"]) if pd.notna(row.get("涨跌幅")) else None

            return AkshareQuote(
                product_code=name_keyword,
                price=price,
                open=open_price,
                high=high,
                low=low,
                rise=rise,
                rise_rate=rise_rate,
                quote_time=datetime.now(timezone.utc),
            )
        except Exception:
            logger.exception("akshare 国际行情查询失败: %s", name_keyword)
            return None


akshare_service = AkshareService()
