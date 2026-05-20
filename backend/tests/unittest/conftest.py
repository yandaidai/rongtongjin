import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture()
def client():
    """提供 FastAPI 测试客户端"""
    with TestClient(app) as c:
        yield c
