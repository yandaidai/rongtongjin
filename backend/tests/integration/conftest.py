"""pytest 测试配置"""

import pytest
import os
import logging
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db, init_db
from app.main import app


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "pytest_run.log"


# 设置环境变量，确保测试环境配置正确
os.environ["ENVIRONMENT"] = "testing"  # 设置环境变量，供 app.config 使用
os.environ["DEBUG"] = "False"  # 测试环境关闭 DEBUG 模式
os.environ["DATABASE_URL"] = "sqlite:///./test.db"  # 测试用数据库 URL
os.environ["SECRET_KEY"] = "test-secret-key-change-in-production"  # 测试用密钥


def pytest_configure(config):
    """在 pytest 启动时配置日志，全局基础设施信息

    注意：不要在 conftest 中手动添加控制台 Handler。
    控制台日志由 pyproject.toml 的 log_cli 系列配置控制，
    pytest 会在 configure 之后自动注册自己的 log_cli handler。
    手动添加会干扰 pytest 的日志捕获机制。
    """
    root_logger = logging.getLogger()

    # ❌ 不要 clear() root_logger.handlers — 会删掉 pytest 自己的 log_cli handler
    # ❌ 不要手动加 StreamHandler — 用 pyproject.toml 的 log_cli 配置即可

    # ✅ 只加文件 Handler (详细日志)
    if not any(isinstance(h, logging.FileHandler) for h in root_logger.handlers):
        file_handler = logging.FileHandler(
            LOG_FILE,
            mode="w",       # 每次测试运行覆盖旧日志
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_format)
        root_logger.addHandler(file_handler)

    # 降低第三方库的日志级别，避免过多无关日志干扰测试输出
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def pytest_sessionstart(session):
    """测试会话开始前执行，此时日志系统已就绪"""
    start_msg = "=" * 30 + "测试会话开始" + "=" * 30
    
    # ✅ 控制台输出（强制刷新）
    print(f"\n{start_msg}", flush=True)
    
    # ✅ 文件输出（通过 logging）
    logging.info(start_msg)


@pytest.fixture(autouse=True)
def per_test_logger(request):
    """每个测试用例独立的日志上下文"""
    test_name = request.node.name

    # # 创建测试专用日志文件
    # test_log_file = LOG_DIR / f"{test_name}.log"
    # test_logger = logging.getLogger(test_name)
    # test_logger.setLevel(logging.DEBUG)
    # test_logger.propagate = False  # 不向 root logger 传播，避免重复日志输出

    # # 防止重复添加 handler
    # test_logger.handlers.clear()

    # file_handler = logging.FileHandler(test_log_file, encoding="utf-8")
    # file_handler.setLevel(logging.DEBUG)
    # file_format = logging.Formatter(
    #     "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    #     datefmt="%Y-%m-%d %H:%M:%S",
    # )
    # file_handler.setFormatter(file_format)
    # test_logger.addHandler(file_handler)

    # 记录测试开始
    logging.info(f"▶▶▶ 开始测试: {test_name} ")

    yield

    # 记录测试结束
    logging.info(f"◀◀◀ 结束测试: {test_name}")



@pytest.fixture(scope="session")
def db_url():
    """测试用数据库连接 URL"""
    # 可以在 Fixture 中添加日志、校验、默认值处理等逻辑
    # 默认使用 SQLite 内存数据库进行测试
    url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # 可选：校验 URL 格式是否合法
    if not url.startswith(("sqlite", "mysql", "postgresql")):
        raise ValueError(f"不支持的数据库 URL: {url}")
    
    return url


@pytest.fixture(scope="session")
def test_engine(db_url):
    """测试用数据库引擎"""
    engine = create_engine(db_url, connect_args={"check_same_thread": False} if "sqlite" in db_url else {})
    return engine


@pytest.fixture(autouse=True)
def setup_database(db_url, test_engine):
    """每个测试前创建表，测试后删除表"""
    # 重新初始化数据库连接为 SQLite
    init_db(db_url=db_url, echo=False)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="session")
def TestingSessionLocal(test_engine):
    """共享的 Session 工厂（整个测试 Session 复用）"""
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture
def test_session(TestingSessionLocal):
    """
    每个测试用例的独立 Session，自动回滚事务
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()  # 回滚所有未提交的更改
        db.close()


@pytest.fixture
def db_session(test_session):
    """兼容旧测试代码（test_configs.py 等），等价于 test_session"""
    return test_session


@pytest.fixture
def client(test_session):
    """
    测试客户端：使用共享的 Session 工厂，确保与 test_session 使用相同的数据库连接
    """
    def _get_test_db():
        # ✅ 复用共享的 Session 工厂，而不是重新创建
        yield test_session

    app.dependency_overrides[get_db] = _get_test_db # 覆盖 get_db 依赖，确保 FastAPI 路由使用测试数据库连接

    with TestClient(app) as c:
        yield c

    """TearDown: 清除依赖覆盖"""
    app.dependency_overrides.clear()
