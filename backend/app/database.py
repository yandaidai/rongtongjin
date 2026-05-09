"""数据库连接配置"""

from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# 延迟创建 engine，允许测试时覆盖
engine = None
SessionLocal = None


def init_db(db_url: Optional[str] = None, echo: bool = False):
    """初始化数据库连接"""
    global engine, SessionLocal
    url = db_url or settings.db_url
    engine = create_engine(url, echo=echo)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """获取数据库会话的依赖注入"""
    global engine, SessionLocal
    if SessionLocal is None:
        init_db(echo=settings.DEBUG)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
