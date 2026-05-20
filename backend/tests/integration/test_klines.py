"""K线数据接口测试"""

from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.metal_kline import MetalKline
from app.models.metal_product import MetalProduct


def _seed_data(db_session: Session):
    """插入测试数据"""
    product = MetalProduct(code="Au99.99", name="黄金99.99", unit="元/克")
    db_session.add(product)
    db_session.commit()

    klines = [
        MetalKline(
            product_id=product.id, k_type="day",
            open_price=448.0, high_price=452.0, low_price=447.0, close_price=450.0,
            volume=1000, k_time=datetime.now(timezone.utc),
        ),
        MetalKline(
            product_id=product.id, k_type="day",
            open_price=450.0, high_price=455.0, low_price=449.0, close_price=453.0,
            volume=1200, k_time=datetime.now(timezone.utc),
        ),
    ]
    for k in klines:
        db_session.add(k)
    db_session.commit()

    return product.id


def test_get_klines(client: TestClient, db_session: Session):
    """测试获取K线数据"""
    product_id = _seed_data(db_session)

    response = client.get(f"/api/klines/?product_id={product_id}&k_type=day")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["k_type"] == "day"


def test_get_latest_klines(client: TestClient, db_session: Session):
    """测试获取最新K线记录"""
    product_id = _seed_data(db_session)

    response = client.get(f"/api/klines/latest?product_id={product_id}&k_type=day&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
