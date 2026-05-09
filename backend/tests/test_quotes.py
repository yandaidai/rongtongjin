"""实时行情接口测试"""

from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.metal_global_config import MetalGlobalConfig
from app.models.metal_product import MetalProduct
from app.models.metal_quote import MetalQuote


def _seed_data(db_session: Session):
    """插入测试数据"""
    product = MetalProduct(code="Au99.99", name="黄金99.99", unit="元/克")
    db_session.add(product)
    db_session.commit()

    config = MetalGlobalConfig(product_id=product.id, sell_add_price=3.0, buy_back_sub_price=2.0)
    db_session.add(config)

    quote = MetalQuote(
        product_id=product.id,
        price=450.0,
        open=448.0,
        high=452.0,
        low=447.0,
        rise=2.0,
        rise_rate=0.44,
        quote_time=datetime.now(timezone.utc),
    )
    db_session.add(quote)
    db_session.commit()

    return product.id


def test_get_quotes(client: TestClient, db_session: Session):
    """测试获取报价"""
    _seed_data(db_session)

    response = client.get("/api/quotes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["product_code"] == "Au99.99"
    assert data[0]["market_price"] == 450.0
    # 销售价 = 大盘价 + 点差
    assert data[0]["sell_price"] == 453.0
    # 回购价 = 大盘价 - 点差
    assert data[0]["buy_back_price"] == 448.0


def test_get_quote_history(client: TestClient, db_session: Session):
    """测试获取历史行情"""
    product_id = _seed_data(db_session)

    response = client.get(f"/api/quotes/history?product_id={product_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["price"] == 450.0
