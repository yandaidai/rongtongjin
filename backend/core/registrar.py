import asyncio
import os

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette_context.middleware import ContextMiddleware
from starlette_context.plugins import RequestIdPlugin

from backend.common.exception.exception_handlers import register_exception
from backend.common.log import log, setup_logging
from backend.common.response.response_schema import ResponseModel
from backend.core.conf import settings
from backend.core.path_conf import STATIC_DIR, UPLOAD_DIR
from backend.database.db import async_db_session, create_tables
from backend.database.redis import redis_client
from backend.middleware.jwt_auth_middleware import JwtAuthMiddleware
from backend.utils.serializers import MsgSpecJSONResponse


async def periodic_news_fetch() -> None:
    """
    定时抓取新闻

    使用纯 asyncio 实现，每小时抓取一次
    """
    while True:
        try:
            from backend.app.services.akshare_service import akshare_service

            async with async_db_session.begin() as db:
                result = await akshare_service.get_all_sge_quotes()
                if len(result) > 0:
                    log.info('定时抓取完成，获取 {count} 条贵金属价格', count=len(result))
        except Exception as e:
            log.error('定时抓取失败: {error}', error=e)
        await asyncio.sleep(settings.NEWS_FETCH_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    应用生命周期

    启动时：
    1. 创建数据库表
    2. 初始化 Redis
    3. 启动定时抓取任务

    关闭时：
    1. 取消定时任务
    2. 关闭 Redis 连接
    """
    # 启动
    await create_tables()
    log.info('数据库表初始化完成')

    try:
        await redis_client.init()
        log.info('Redis 连接初始化完成')
    except Exception as e:
        log.warning('Redis 连接失败，将使用无缓存模式: {error}', error=e)
    
    # 启动定时抓取
    fetch_task = asyncio.create_task(periodic_news_fetch())
    log.info('金价抓取任务已启动')

    yield

    # 关闭
    fetch_task.cancel()
    try:
        await fetch_task
    except asyncio.CancelledError:
        log.info('金价抓取任务已取消')
        pass

    await redis_client.aclose()
    log.info('Redis 连接已关闭')


def register_app() -> FastAPI:
    """注册 FastAPI 应用"""

    app = FastAPI(
        title=settings.FASTAPI_TITLE,
        description=settings.FASTAPI_DESCRIPTION,
        docs_url=settings.FASTAPI_DOCS_URL,
        redoc_url=settings.FASTAPI_REDOC_URL,
        openapi_url=settings.FASTAPI_OPENAPI_URL,
        default_response_class=MsgSpecJSONResponse,
        lifespan=lifespan,
    )

    # 注册组件
    register_logger()
    register_middleware(app)
    register_router(app)
    register_exception(app)
    register_health_check(app)

    return app


def register_logger() -> None:
    """注册日志"""
    setup_logging()


def register_middleware(app: FastAPI) -> None:
    """注册中间件（执行顺序从下往上）"""
    # ContextVar - 请求上下文
    app.add_middleware(
        ContextMiddleware,
        plugins=[RequestIdPlugin(validate=True)],
    )

    # JWT 认证
    app.add_middleware(
        AuthenticationMiddleware,
        backend=JwtAuthMiddleware(),
        on_error=JwtAuthMiddleware.auth_exception_handler,
    )

    # CORS
    if settings.MIDDLEWARE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
            expose_headers=settings.CORS_EXPOSE_HEADERS,
        )


def register_router(app: FastAPI) -> None:
    """注册路由"""
    from backend.app.router import router as main_router

    app.include_router(main_router)

    @app.get('/')
    async def root():
        """根路径，重定向到新闻页面"""
        return ResponseModel.success(msg='News Aggregator API', data={
            'version': '0.1.0',
            'docs': '/docs',
        })


def register_health_check(app: FastAPI) -> None:
    """注册健康检查"""
    @app.get('/health')
    async def health():
        return ResponseModel.success(data={'status': 'ok'})
