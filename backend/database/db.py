"""数据库连接配置 — 异步，支持 SQLite（测试）+ asyncmy（生产）"""

import sys

from collections.abc import AsyncGenerator
from typing import Annotated, Any, Optional, TypeAlias
from uuid import uuid4

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.common.log import log
from backend.common.model import MappedBase
from backend.core.conf import settings

# 延迟初始化（模块加载时不创建连接，允许测试时通过 init_db() 覆盖）
async_engine: Optional[AsyncEngine] = None
async_db_session: Optional[async_sessionmaker[AsyncSession]] = None


# ---------------------------------------------------------------------------
# URL 构建
# ---------------------------------------------------------------------------

def get_database_url(*, unittest: bool = False, with_database: bool = True) -> URL:
    """
    从 settings 构建 MySQL 异步连接 URL。

    :param unittest: 是否指向测试库（自动追加 _test 后缀）
    :param with_database: 是否包含数据库名（建库时传 False）
    """
    database = settings.DATABASE_SCHEMA if not unittest else f'{settings.DATABASE_SCHEMA}_test'
    if not with_database:
        database = None

    return URL.create(
        drivername='mysql+asyncmy',
        username=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=database,
    )


def get_sync_database_url(*, unittest: bool = False, with_database: bool = True) -> str:
    """
    同步数据库连接 URL（用于 Alembic 迁移）。

    返回字符串形式而非 URL 对象，兼容 Alembic 的 env.py。
    """
    database = settings.DATABASE_SCHEMA if not unittest else f'{settings.DATABASE_SCHEMA}_test'
    if not with_database:
        database = None

    url = URL.create(
        drivername='mysql+pymysql',
        username=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=database,
    )
    return url.render_as_string(hide_password=False)


# ---------------------------------------------------------------------------
# 引擎 / 会话工厂
# ---------------------------------------------------------------------------

def _is_sqlite_url(url: str | URL) -> bool:
    """检测 URL 是否指向 SQLite"""
    return 'sqlite' in str(url)


def create_database_async_engine(url: str | URL, echo: bool | None = None) -> AsyncEngine:
    """
    创建异步数据库引擎。

    自动检测 SQLite URL 并切换为 ``aiosqlite`` 驱动（用于测试），
    MySQL 则使用 ``asyncmy`` 驱动并配置完整连接池。

    :param url: 数据库连接 URL
    :param echo: 覆盖 ``settings.DATABASE_ECHO``，测试时可传入 True
    """
    _echo = settings.DATABASE_ECHO if echo is None else echo
    try:
        url_str = str(url)

        if _is_sqlite_url(url_str):
            # SQLite — 测试用，无连接池
            if url_str.startswith('sqlite://'):
                url_str = url_str.replace('sqlite://', 'sqlite+aiosqlite://', 1)
            return create_async_engine(url_str, echo=_echo, future=True)

        # MySQL（asyncmy）— 生产配置
        return create_async_engine(
            url,
            echo=_echo,
            echo_pool=settings.DATABASE_POOL_ECHO,
            future=True,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=3600,
            pool_pre_ping=True,
            pool_use_lifo=False,
        )
    except Exception as e:
        log.error('数据库连接失败 {error}', error=e)
        sys.exit()


def create_database_async_session(engine: AsyncEngine) -> async_sessionmaker[AsyncSession | Any]:
    """
    创建数据库异步会话工厂。
    """
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )


def init_db(db_url: Optional[str] = None, echo: Optional[bool] = None) -> None:
    """
    初始化数据库连接。

    - 不传 ``db_url`` → 从 ``settings`` 构建 MySQL URL
    - 传 ``db_url``（如 ``sqlite+aiosqlite:///./test.db``）→ 测试用 SQLite
    - ``echo`` 默认为 None（使用 ``settings.DATABASE_ECHO``），传 True/False 则覆盖
    """
    global async_engine, async_db_session

    url: str | URL = db_url or get_database_url()
    async_engine = create_database_async_engine(url, echo=echo)
    async_db_session = create_database_async_session(async_engine)


# ---------------------------------------------------------------------------
# 依赖注入
# ---------------------------------------------------------------------------

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话（FastAPI 依赖注入）"""
    if async_db_session is None:
        init_db()
    async with async_db_session() as session:
        yield session


async def get_db_transaction() -> AsyncGenerator[AsyncSession, None]:
    """获取带事务的数据库会话"""
    if async_db_session is None:
        init_db()
    async with async_db_session.begin() as session:
        yield session


# ---------------------------------------------------------------------------
# 表管理
# ---------------------------------------------------------------------------

async def create_tables() -> None:
    """创建所有表"""
    if async_engine is None:
        init_db()
    async with async_engine.begin() as conn:
        await conn.run_sync(MappedBase.metadata.create_all)


async def drop_tables() -> None:
    """删除所有表"""
    if async_engine is None:
        init_db()
    async with async_engine.begin() as conn:
        await conn.run_sync(MappedBase.metadata.drop_all)


# ---------------------------------------------------------------------------
# 工具
# ---------------------------------------------------------------------------

def uuid4_str() -> str:
    return str(uuid4())


# ---------------------------------------------------------------------------
# 类型别名（路由注入时直接用）
# ---------------------------------------------------------------------------
CurrentSession: TypeAlias = Annotated[AsyncSession, Depends(get_db)]
CurrentSessionTransaction: TypeAlias = Annotated[AsyncSession, Depends(get_db_transaction)]
