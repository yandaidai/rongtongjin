#!/usr/bin/env python3
"""初始化种子数据：贵金属品种 + 默认点差配置

用法:
    python seed.py            # 写入 MySQL 数据库
    python seed.py --sqlite   # 写入 SQLite 测试数据库
"""

import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base
from app.models.metal_global_config import MetalGlobalConfig
from app.models.metal_product import MetalProduct

# 国内 SGE 品种
DOMESTIC_PRODUCTS = [
    {"code": "Au99.99", "name": "黄金99.99", "unit": "元/克"},
    {"code": "Au99.95", "name": "黄金99.95", "unit": "元/克"},
    {"code": "Au100g",  "name": "黄金100克", "unit": "元/克"},
    {"code": "Pt99.95", "name": "铂金99.95", "unit": "元/克"},
    {"code": "Ag(T+D)", "name": "白银延期",  "unit": "元/千克"},
    {"code": "Au(T+D)", "name": "黄金延期",  "unit": "元/克"},
    {"code": "mAu(T+D)","name": "迷你黄金延期", "unit": "元/克"},
    {"code": "Ag99.99", "name": "白银99.99", "unit": "元/千克"},
]

# 国际品种
INTERNATIONAL_PRODUCTS = [
    {"code": "XAU", "name": "国际现货黄金", "unit": "美元/盎司"},
    {"code": "XAG", "name": "国际现货白银", "unit": "美元/盎司"},
    {"code": "XPT", "name": "国际现货铂金", "unit": "美元/盎司"},
]

ALL_PRODUCTS = DOMESTIC_PRODUCTS + INTERNATIONAL_PRODUCTS


def seed(db: Session):
    """写入种子数据"""
    existing = {p.code for p in db.query(MetalProduct).all()}

    for item in ALL_PRODUCTS:
        if item["code"] in existing:
            continue
        product = MetalProduct(**item)
        db.add(product)
        db.flush()  # 获取 product.id

        # 创建默认点差配置
        config = MetalGlobalConfig(
            product_id=product.id,
            sell_add_price=3.0,
            buy_back_sub_price=2.0,
        )
        db.add(config)

    db.commit()
    print(f"种子数据写入完成：{len(ALL_PRODUCTS)} 个品种 + 对应默认点差")


def main():
    use_sqlite = "--sqlite" in sys.argv

    if use_sqlite:
        db_url = "sqlite:///./test.db"
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
    else:
        from app.config import settings
        db_url = settings.db_url
        engine = create_engine(db_url)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
