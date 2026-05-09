"""点差配置接口测试"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.metal_global_config import MetalGlobalConfig
from app.models.metal_product import MetalProduct


def _seed_data(db_session: Session):
    """插入测试数据"""
    product = MetalProduct(code="Au99.99", name="黄金99.99", unit="元/克")
    db_session.add(product)
    db_session.commit()

    config = MetalGlobalConfig(
        product_id=product.id,
        sell_add_price=3.0,
        buy_back_sub_price=2.0,
    )
    db_session.add(config)
    db_session.commit()

    return product.id


def test_get_global_configs(client: TestClient, db_session: Session):
    """测试获取全局点差配置"""
    _seed_data(db_session)

    response = client.get("/api/global/config/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["sell_add_price"] == 3.0
    assert data[0]["buy_back_sub_price"] == 2.0


def test_get_global_config_by_product(client: TestClient, db_session: Session):
    """测试获取指定品种点差配置"""
    product_id = _seed_data(db_session)

    response = client.get(f"/api/global/config/{product_id}")
    assert response.status_code == 200
    assert response.json()["sell_add_price"] == 3.0


def test_update_global_config(client: TestClient, db_session: Session):
    """测试更新全局点差配置"""
    product_id = _seed_data(db_session)

    response = client.patch(
        f"/api/global/config/{product_id}",
        json={"sell_add_price": 5.0},
    )
    assert response.status_code == 200
    assert response.json()["sell_add_price"] == 5.0
    assert response.json()["buy_back_sub_price"] == 2.0  # 未修改的值保持不变
