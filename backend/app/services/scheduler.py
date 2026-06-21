"""定时任务：每分钟刷新贵金属行情到 metal_quote 表"""

import logging
from datetime import datetime, timezone

from apscheduler.schedulers.background import BackgroundScheduler

from app.constants import INTERNATIONAL_CODE_MAP, SGE_SYMBOLS
from app.database import get_db
from app.models.metal_kline import MetalKline
from app.models.metal_product import MetalProduct
from app.models.metal_quote import MetalQuote
from app.services.akshare_service import AkshareService

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def refresh_quotes():
    """定时刷新所有品种的大盘行情并保存到数据库"""
    db = get_db()
    try:
        products = db.query(MetalProduct).filter(MetalProduct.status == True).all()
        now = datetime.now(timezone.utc)

        for product in products:
            quote = None
            if product.code in SGE_SYMBOLS:
                quote = AkshareService.get_sge_quote(product.code)
            elif product.code in INTERNATIONAL_CODE_MAP:
                name_keyword = INTERNATIONAL_CODE_MAP[product.code]
                quote = AkshareService.get_international_quote(name_keyword)

            if quote is None:
                continue

            # 写入 metal_quote 表
            db.add(MetalQuote(
                product_id=product.id,
                price=quote.price,
                open=quote.open,
                high=quote.high,
                low=quote.low,
                rise=quote.rise,
                rise_rate=quote.rise_rate,
                quote_time=quote.quote_time or now,
            ))

            # 计算真实的 K 线 OHLC（基于上一分钟收盘价）
            prev_kline = db.query(MetalKline).filter(
                MetalKline.product_id == product.id,
                MetalKline.k_type == "minute",
            ).order_by(MetalKline.k_time.desc()).first()

            prev_close = prev_kline.close_price if prev_kline else quote.price
            open_price = prev_close
            high_price = max(prev_close, quote.price)
            low_price = min(prev_close, quote.price)
            close_price = quote.price

            db.add(MetalKline(
                product_id=product.id,
                k_type="minute",
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                close_price=close_price,
                volume=0.0,
                k_time=quote.quote_time or now,
            ))

        db.commit()
        logger.info("行情刷新完成，共处理 %d 个品种", len(products))
    except Exception:
        logger.exception("行情刷新失败")
    finally:
        db.close()


def start_scheduler():
    """启动定时任务"""
    scheduler.add_job(
        refresh_quotes,
        "interval",
        minutes=1,
        id="refresh_quotes",
        name="每分钟刷新贵金属行情",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("行情定时任务已启动（间隔 1 分钟）")


def stop_scheduler():
    """停止定时任务"""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("行情定时任务已停止")
