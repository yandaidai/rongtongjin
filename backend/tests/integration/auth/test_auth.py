"""用户认证接口测试 - 手机验证码方式"""

from fastapi.testclient import TestClient
from app.models.user import User


def test_register_success(client: TestClient, test_session, auth_empty_db):
    """测试用户注册成功"""
    phone = auth_empty_db.get("unregistered_phone", "13800138000")
    test_code = "123456"  # 与 AuthService._generate_code() 中的固定验证码一致
    response = client.post("/api/auth/register", json={
        "phone": phone,
        "code": test_code,
        "agree_protocol": True,
    })

    # 3. 验证响应
    assert response.status_code == 200
    data = response.json()

    # 3.1 验证顶层字段   
    assert "access_token" in data, "响应中缺少 access_token"
    assert "token_type" in data, "响应中缺少 token_type"
    assert "user" in data, "响应中缺少 user 字段"
    assert data["token_type"] == "bearer", f"期望 token_type 为 bearer，实际为 {data['token_type']}"

    # 3.2 验证 user 对象
    user_data = data["user"]
    expected_nickname = f"用户{phone[-4:]}"
    assert user_data["phone"] == phone, f"期望手机号为 {phone}，实际为 {user_data['phone']}"
    assert user_data["nickname"] == expected_nickname, f"期望昵称为 {expected_nickname}，实际为 {user_data['nickname']}"

    # 3.3 验证敏感字段不泄露（密码哈希等不应返回）
    sensitive_fields = ["hashed_password", "password"]
    for field in sensitive_fields:
        assert field not in user_data, f"不应返回敏感字段: {field}"
    
    # 4. 验证数据库（核心！）
    db_user = test_session.query(User).filter(User.phone == phone).first()
    assert db_user is not None, f"数据库中未找到手机号为 {phone} 的用户"
    
    # 4.1 验证数据库字段正确
    assert db_user.phone == phone, f"数据库手机号期望 {phone}，实际 {db_user.phone}"
    assert db_user.nickname == expected_nickname, f"数据库昵称期望 {expected_nickname}，实际 {db_user.nickname}"
    assert db_user.hashed_password is None, f"注册时密码应为空，实际有哈希值: {db_user.hashed_password}"
    assert db_user.email is None, "注册时邮箱应为空"
    
    # 4.2 验证时间字段自动填充
    assert db_user.created_at is not None, "created_at 应自动填充"
    assert db_user.updated_at is not None, "updated_at 应自动填充"
    
    # 4.3 验证敏感字段（确保没有明文密码）
    assert not hasattr(db_user, "password"), "模型中不应有明文 password 字段"


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


def test_register_duplicate_phone(client: TestClient, test_session, auth_user_without_password):
    """测试重复手机号注册"""
    response = client.post("/api/auth/register", json={
        "phone": "13800138001",
        "code": "123456",
        "agree_protocol": True,
    })
    assert response.status_code == 400
    assert "已注册" in response.json()["detail"]

    db_user = test_session.query(User).filter(User.phone == auth_user_without_password.phone).first()
    assert db_user is not None, f"数据库中未找到手机号为 {auth_user_without_password.phone} 的用户"
    
    #验证数据库字段正确
    assert db_user.phone == auth_user_without_password.phone, f"数据库手机号期望 {auth_user_without_password.phone}，实际 {db_user.phone}"


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
