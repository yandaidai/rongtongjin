"""
pytest 测试配置 — 全异步架构

使用 register_app() 创建独立测试实例，httpx.AsyncClient 发送请求，
savepoint 事务隔离实现测试间数据隔离。
"""

import os
import logging
from pathlib import Path
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from backend.common.model import Base
from backend.core.registrar import register_app
from database.db import get_db, get_db_transaction


# ── 环境变量（在模块导入前设置） ──

os.environ.setdefault("ENVIRONMENT", "testing")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test.db?timeout=30")
os.environ.setdefault("SECRET_KEY", "test-secret-key-change-in-production")


# ── 日志 ──

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "pytest_run.log"


def pytest_configure(config):
    root_logger = logging.getLogger()
    if not any(isinstance(h, logging.FileHandler) for h in root_logger.handlers):
        handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))
        root_logger.addHandler(handler)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def pytest_sessionstart(session):
    print("\n" + "=" * 30 + " 测试会话开始 " + "=" * 30, flush=True)
    logging.info("测试会话开始")


@pytest.fixture(autouse=True)
def per_test_logger(request):
    test_name = request.node.name
    logging.info("▶▶▶ 开始测试: %s", test_name)
    yield
    logging.info("◀◀◀ 结束测试: %s", test_name)


# ── 数据库引擎 ──

@pytest_asyncio.fixture(scope="session")
async def db_url() -> str:
    return os.environ["DATABASE_URL"]


@pytest_asyncio.fixture(scope="session")
async def test_engine(db_url: str) -> AsyncGenerator[AsyncEngine, None]:
    """异步数据库引擎（session 级，所有测试复用）"""
    engine = create_async_engine(db_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def test_session_factory(
    test_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """AsyncSession 工厂"""
    return async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


# ── FastAPI 应用 ──

@asynccontextmanager
async def _noop_lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    yield


@pytest_asyncio.fixture(scope="session")
async def app() -> FastAPI:
    """测试用 FastAPI 应用实例（独立创建，不影响生产 app）"""
    application = register_app()
    application.router.lifespan_context = _noop_lifespan
    return application


# ── 数据库会话（savepoint 隔离） ──

@pytest_asyncio.fixture(scope="function")
async def db(
    app: FastAPI,
    test_engine: AsyncEngine,
    test_session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """提供隔离的数据库会话（function 级，savepoint 回滚）"""
    conn = await test_engine.connect()
    trans = await conn.begin()

    session = AsyncSession(
        bind=conn,
        join_transaction_mode="create_savepoint",
        expire_on_commit=False,
    )

    async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield session

    async def _override_get_db_transaction() -> AsyncGenerator[AsyncSession, None]:
        yield session

    orig_overrides = dict(app.dependency_overrides)
    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_db_transaction] = _override_get_db_transaction

    try:
        yield session
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(orig_overrides)
        await trans.rollback()
        await session.close()
        await conn.close()


# ── 测试用 DB Session（直接查询） ──

@pytest_asyncio.fixture(scope="function")
async def test_db_session(test_session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    """提供独立的 AsyncSession，用于测试中的直接 DB 查询"""
    async with test_session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()


# ── HTTP 客户端 ──

@pytest_asyncio.fixture(scope="function")
async def async_client(app: FastAPI, db: Any) -> AsyncGenerator[AsyncClient, None]:
    """异步 HTTP 客户端（function 级）"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
