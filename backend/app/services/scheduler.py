"""定时任务：每分钟刷新贵金属行情到 metal_quote 表"""

import logging
from datetime import datetime, timezone

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings
from app.models.metal_kline import MetalKline
from app.models.metal_product import MetalProduct
from app.models.metal_quote import MetalQuote
from app.services.akshare_service import AkshareService
from app.services.quote_service import QuoteService

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def _get_session() -> Session:
    """创建独立数据库会话（不依赖 FastAPI 注入）"""
    engine = create_engine(settings.db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def refresh_quotes():
    """定时刷新所有品种的大盘行情并保存到数据库"""
    db = _get_session()
    try:
        products = db.query(MetalProduct).filter(MetalProduct.status == True).all()
        now = datetime.now(timezone.utc)

        for product in products:
            quote = None
            if product.code in AkshareService.SGE_SYMBOLS:
                quote = AkshareService.get_sge_quote(product.code)
            elif product.code in QuoteService.INTERNATIONAL_CODE_MAP:
                name_keyword = QuoteService.INTERNATIONAL_CODE_MAP[product.code]
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

            # 写入 K 线数据（以分钟 K 线维度存储）
            db.add(MetalKline(
                product_id=product.id,
                k_type="minute",
                open_price=quote.price,
                high_price=quote.price,
                low_price=quote.price,
                close_price=quote.price,
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
