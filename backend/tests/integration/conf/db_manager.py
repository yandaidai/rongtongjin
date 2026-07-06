"""
测试数据库生命周期管理器

管理测试数据库的创建和清理：
1. 连接 MySQL（不指定数据库）创建测试库
2. 在测试数据库中创建所有表
3. 测试结束后清理测试库

安全保护：如果 ENVIRONMENT != 'test' 则拒绝执行任何 DDL 操作。

使用方式（通常在 conftest.py 的 session-scoped fixture 中调用）:
    await create_test_database()
    await create_test_tables()
    ...
    await drop_test_database()
"""

from sqlalchemy import URL, create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from backend.common.log import log
from backend.common.model import MappedBase
from backend.core.conf import settings

# ============================================================
# 安全防护：确认当前处于测试模式
# ============================================================
_TEST_ENV_GUARD = settings.ENVIRONMENT == 'test'
if not _TEST_ENV_GUARD:
    raise RuntimeError(
        '致命错误：测试数据库管理器只能在 ENVIRONMENT=test 模式下运行！\n'
        f'当前环境: {settings.ENVIRONMENT}'
    )


def _get_test_db_name() -> str:
    """获取测试数据库名称（生产库名 + _test 后缀）"""
    return f'{settings.DATABASE_SCHEMA}_test'


def _get_admin_db_url() -> str:
    """
    获取管理数据库连接的 URL（不指定具体数据库，用于 CREATE/DROP DATABASE）。
    """
    url = URL.create(
        drivername='mysql+pymysql',
        username=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=None,  # 不指定数据库，只连接 MySQL 实例
    )
    return url.render_as_string(hide_password=False)


async def create_test_database() -> None:
    """
    创建测试数据库（如果不存在）。

    使用同步连接执行 DDL，兼容异步框架的 pytest session 生命周期。
    """
    test_db_name = _get_test_db_name()
    admin_url = _get_admin_db_url()

    try:
        sync_engine = create_engine(admin_url, isolation_level='AUTOCOMMIT')
        with sync_engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
                    f"WHERE SCHEMA_NAME = '{test_db_name}'"
                )
            )
            exist = result.fetchone() is not None

            if not exist:
                conn.execute(
                    text(
                        f'CREATE DATABASE `{test_db_name}` '
                        'CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'
                    )
                )
                log.info('[TestDB] 测试数据库已创建: {db}', db=test_db_name)
            else:
                log.info('[TestDB] 测试数据库已存在: {db}', db=test_db_name)
    except Exception as e:
        log.error('[TestDB] 创建测试数据库失败: {error}', e)
        raise
    finally:
        sync_engine.dispose()   # 引擎释放连接池全部资源


async def drop_test_database() -> None:
    """
    删除测试数据库。

    注意：仅当显式调用时执行。默认 conftest 不会自动删除（保留现场便于排查）。
    """
    test_db_name = _get_test_db_name()
    admin_url = _get_admin_db_url()

    try:
        sync_engine = create_engine(admin_url, isolation_level='AUTOCOMMIT')
        with sync_engine.connect() as conn:
            conn.execute(text(f'DROP DATABASE IF EXISTS `{test_db_name}`'))
            log.info('[TestDB] 测试数据库已删除: {db}', db=test_db_name)
    except Exception as e:
        log.error('[TestDB] 删除测试数据库失败: {error}', error=e)
        raise
    finally:
        sync_engine.dispose()


async def reset_test_database() -> None:
    """
    重置测试数据库（先删除再创建）。

    适用于每个测试类/模块之间需要完全隔离的场景。
    """
    await drop_test_database()
    await create_test_database()


async def create_test_tables() -> None:
    """
    在测试数据库中创建所有表。

    使用 MappedBase.metadata.create_all 确保与生产表结构一致（幂等操作）。
    """
    test_db_name = _get_test_db_name()
    test_async_url = URL.create(
        drivername='mysql+asyncmy',
        username=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=test_db_name,
    )

    test_engine: AsyncEngine | None = None
    try:
        test_engine = create_async_engine(
            test_async_url,
            echo=False,
            future=True,
        )
        async with test_engine.begin() as conn:
            await conn.run_sync(MappedBase.metadata.create_all)
        log.info('[TestDB] 测试数据库表创建完成')
    except Exception as e:
        log.error('[TestDB] 创建测试表失败: {error}', error=e)
        raise
    finally:
        if test_engine is not None:
            await test_engine.dispose()


async def drop_test_tables() -> None:
    """
    删除测试数据库中的所有表。
    """
    test_db_name = _get_test_db_name()
    test_async_url = URL.create(
        drivername='mysql+asyncmy',
        username=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=test_db_name,
    )

    test_engine: AsyncEngine | None = None
    try:
        test_engine = create_async_engine(test_async_url, echo=False, future=True)
        async with test_engine.begin() as conn:
            await conn.run_sync(MappedBase.metadata.drop_all)
        log.info('[TestDB] 测试数据库表已全部删除')
    except Exception as e:
        log.error('[TestDB] 删除测试表失败: {error}', error=e)
        raise
    finally:
        if test_engine is not None:
            await test_engine.dispose()
