"""数据库连接配置"""

from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

# 延迟创建 engine，允许测试时覆盖
engine = None
SessionLocal = None


def init_db(db_url: Optional[str] = None, echo: bool = False):
    """初始化数据库连接（测试可以传入 db_url 覆盖）"""
    global engine, SessionLocal
    url = db_url or settings.db_url
    engine = create_engine(url, echo=echo, pool_size=5, max_overflow=10)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """获取数据库会话（FastAPI 依赖注入，请求结束时自动关闭）"""
    global engine, SessionLocal
    if SessionLocal is None:
        init_db(echo=settings.DEBUG)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
