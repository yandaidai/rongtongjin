"""贵金属品种接口测试"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database import Base
from app.models.metal_product import MetalProduct


def _seed_products(db_session: Session):
    """插入测试数据"""
    products = [
        MetalProduct(code="Au99.99", name="黄金99.99", unit="元/克"),
        MetalProduct(code="Ag99.99", name="白银99.99", unit="元/克"),
        MetalProduct(code="Pt99.95", name="铂金99.95", unit="元/克"),
    ]
    for p in products:
        db_session.add(p)
    db_session.commit()


def test_get_products_empty(client: TestClient):
    """测试获取品种列表（空数据）"""
    response = client.get("/api/products/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_products(client: TestClient, db_session: Session):
    """测试获取品种列表"""
    _seed_products(db_session)

    response = client.get("/api/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["code"] == "Au99.99"
