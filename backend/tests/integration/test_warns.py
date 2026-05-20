"""价格预警接口测试"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.metal_product import MetalProduct


def _register_and_login(client: TestClient) -> str:
    """辅助函数：注册并登录，返回 token"""
    resp = client.post("/api/auth/register", json={
        "phone": "13800138000",
        "code": "123456",
        "agree_protocol": True,
    })
    return resp.json()["access_token"]


def _seed_product(db_session: Session) -> int:
    """插入测试品种数据"""
    product = MetalProduct(code="Au99.99", name="黄金99.99", unit="元/克")
    db_session.add(product)
    db_session.commit()
    return product.id


def test_create_warn(client: TestClient, db_session: Session):
    """测试创建预警"""
    token = _register_and_login(client)
    product_id = _seed_product(db_session)

    response = client.post(
        "/api/user/warn/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "product_id": product_id,
            "upper_limit": 500.0,
            "lower_limit": 400.0,
            "warn_enable": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["upper_limit"] == 500.0
    assert data["lower_limit"] == 400.0
    assert data["warn_enable"] is True


def test_get_warns(client: TestClient, db_session: Session):
    """测试获取预警列表"""
    token = _register_and_login(client)
    product_id = _seed_product(db_session)

    # 创建预警
    client.post(
        "/api/user/warn/",
        headers={"Authorization": f"Bearer {token}"},
        json={"product_id": product_id, "upper_limit": 500.0},
    )

    # 获取列表
    response = client.get(
        "/api/user/warn/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_update_warn(client: TestClient, db_session: Session):
    """测试更新预警"""
    token = _register_and_login(client)
    product_id = _seed_product(db_session)

    # 创建预警
    create_resp = client.post(
        "/api/user/warn/",
        headers={"Authorization": f"Bearer {token}"},
        json={"product_id": product_id, "upper_limit": 500.0},
    )
    warn_id = create_resp.json()["id"]

    # 更新预警
    response = client.patch(
        f"/api/user/warn/{warn_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"upper_limit": 600.0, "warn_enable": False},
    )
    assert response.status_code == 200
    assert response.json()["upper_limit"] == 600.0
    assert response.json()["warn_enable"] is False


def test_delete_warn(client: TestClient, db_session: Session):
    """测试删除预警"""
    token = _register_and_login(client)
    product_id = _seed_product(db_session)

    # 创建预警
    create_resp = client.post(
        "/api/user/warn/",
        headers={"Authorization": f"Bearer {token}"},
        json={"product_id": product_id, "upper_limit": 500.0},
    )
    warn_id = create_resp.json()["id"]

    # 删除预警
    response = client.delete(
        f"/api/user/warn/{warn_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    # 确认已删除
    get_resp = client.get(
        "/api/user/warn/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert len(get_resp.json()) == 0
