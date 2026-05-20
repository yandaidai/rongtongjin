"""用户认证接口测试 - 手机验证码方式"""

from fastapi.testclient import TestClient


def test_register_success(client: TestClient):
    """测试用户注册成功"""
    response = client.post("/api/auth/register", json={
        "phone": "13800138001",
        "code": "123456",
        "agree_protocol": True,
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["phone"] == "13800138001"
    assert data["user"]["nickname"] == "用户8001"


def test_register_without_agreement(client: TestClient):
    """测试未同意协议注册"""
    response = client.post("/api/auth/register", json={
        "phone": "13800138002",
        "code": "123456",
        "agree_protocol": False,
    })
    assert response.status_code == 400
    assert "同意" in response.json()["detail"]


def test_register_wrong_code(client: TestClient):
    """测试错误验证码注册"""
    response = client.post("/api/auth/register", json={
        "phone": "13800138003",
        "code": "000000",
        "agree_protocol": True,
    })
    assert response.status_code == 400
    assert "验证码错误" in response.json()["detail"]


def test_register_duplicate_phone(client: TestClient):
    """测试重复手机号注册"""
    # 先注册
    client.post("/api/auth/register", json={
        "phone": "13800138004",
        "code": "123456",
        "agree_protocol": True,
    })
    # 再次注册相同手机号
    response = client.post("/api/auth/register", json={
        "phone": "13800138004",
        "code": "123456",
        "agree_protocol": True,
    })
    assert response.status_code == 400
    assert "已注册" in response.json()["detail"]


def test_login_success(client: TestClient):
    """测试登录成功"""
    # 先注册
    client.post("/api/auth/register", json={
        "phone": "13800138005",
        "code": "123456",
        "agree_protocol": True,
    })
    # 登录
    response = client.post("/api/auth/login", json={
        "phone": "13800138005",
        "code": "123456",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["phone"] == "13800138005"


def test_login_wrong_code(client: TestClient):
    """测试错误验证码登录"""
    # 先注册
    client.post("/api/auth/register", json={
        "phone": "13800138006",
        "code": "123456",
        "agree_protocol": True,
    })
    # 错误验证码登录
    response = client.post("/api/auth/login", json={
        "phone": "13800138006",
        "code": "000000",
    })
    assert response.status_code == 400


def test_login_user_not_found(client: TestClient):
    """测试未注册用户登录"""
    response = client.post("/api/auth/login", json={
        "phone": "13900139000",
        "code": "123456",
    })
    assert response.status_code == 404


def test_get_user_info(client: TestClient):
    """测试获取用户信息"""
    # 注册
    reg_resp = client.post("/api/auth/register", json={
        "phone": "13800138007",
        "code": "123456",
        "agree_protocol": True,
    })
    token = reg_resp.json()["access_token"]

    # 获取用户信息
    response = client.get(
        "/api/auth/user/info",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["phone"] == "13800138007"


def test_get_user_info_unauthorized(client: TestClient):
    """测试未授权访问用户信息"""
    response = client.get("/api/auth/user/info")
    assert response.status_code == 401


def test_update_nickname(client: TestClient):
    """测试更新昵称"""
    reg_resp = client.post("/api/auth/register", json={
        "phone": "13800138008",
        "code": "123456",
        "agree_protocol": True,
    })
    token = reg_resp.json()["access_token"]

    response = client.patch(
        "/api/auth/user/nickname",
        headers={"Authorization": f"Bearer {token}"},
        json={"nickname": "新昵称"},
    )
    assert response.status_code == 200
    assert response.json()["nickname"] == "新昵称"


def test_update_avatar(client: TestClient):
    """测试更新头像"""
    reg_resp = client.post("/api/auth/register", json={
        "phone": "13800138009",
        "code": "123456",
        "agree_protocol": True,
    })
    token = reg_resp.json()["access_token"]

    response = client.patch(
        "/api/auth/user/avatar",
        headers={"Authorization": f"Bearer {token}"},
        json={"avatar": "https://example.com/avatar.jpg"},
    )
    assert response.status_code == 200
    assert response.json()["avatar"] == "https://example.com/avatar.jpg"


def test_set_password(client: TestClient):
    """测试设置密码"""
    reg_resp = client.post("/api/auth/register", json={
        "phone": "13800138010",
        "code": "123456",
        "agree_protocol": True,
    })
    token = reg_resp.json()["access_token"]

    response = client.post(
        "/api/auth/user/password",
        headers={"Authorization": f"Bearer {token}"},
        json={"password": "newpassword123"},
    )
    assert response.status_code == 200
    assert "成功" in response.json()["message"]


def test_deactivate_account(client: TestClient):
    """测试注销账号"""
    reg_resp = client.post("/api/auth/register", json={
        "phone": "13800138011",
        "code": "123456",
        "agree_protocol": True,
    })
    token = reg_resp.json()["access_token"]

    response = client.delete(
        "/api/auth/user/account",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert "注销" in response.json()["message"]
