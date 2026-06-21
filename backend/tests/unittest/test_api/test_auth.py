import pytest
from fastapi import HTTPException
from datetime import datetime
from unittest.mock import patch, MagicMock
from app.schemas.user import TokenResponse, UserResponse

#标记为单元测试（可选）
pytestmark = pytest.mark.unit

def test_login_success(client):
    """测试登录成功的情况"""
    fake_user = UserResponse(
        id=1,
        phone="1234567890",
        status=True,
        created_at=datetime.now(),
    )
    fake_token = TokenResponse(access_token="fake-token", token_type="bearer", user=fake_user)
    with patch("app.api.v1.auth.AuthService.login") as mock_login:
        mock_login.return_value = fake_token
        response = client.post("/api/auth/login", json={"phone": "1234567890", "code": "12345678"})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["access_token"] == "fake-token"
        assert data["user"] == fake_user.model_dump(mode="json")


def test_login_invalid_code(client):
    """测试登录失败 - 验证码错误"""
    with patch("app.api.v1.auth.AuthService.login") as mock_login:
        mock_login.side_effect = HTTPException(status_code=400, detail="验证码错误")
        response = client.post("/api/auth/login", json={"phone": "1234567890", "code": "wrong-code"})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "验证码错误"


def test_login_user_not_found(client):
    """测试登录失败 - 用户不存在"""
    with patch("app.api.v1.auth.AuthService.login") as mock_login:
        mock_login.side_effect = HTTPException(status_code=400, detail="该手机号未注册")
        response = client.post("/api/auth/login", json={"phone": "0987654321", "code": "12345678"})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "该手机号未注册"


def test_login_missing_fields(client):
    """测试登录失败 - 缺少必填字段"""
    response = client.post("/api/auth/login", json={"phone": "1234567890"})
    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert "detail" in data
    assert any(error["loc"][-1] == "code" for error in data["detail"])


def test_login_invalid_phone_format(client):
    """测试登录失败 - 手机号格式错误"""
    with patch("app.api.v1.auth.AuthService.login") as mock_login:
        mock_login.side_effect = HTTPException(status_code=400, detail="手机号格式错误")
        response = client.post("/api/auth/login", json={"phone": "invalid-phone", "code": "12345678"})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "手机号格式错误"


def test_login_agree_protocol_false(client):
    """测试登录失败 - 不同意用户协议"""
    with patch("app.api.v1.auth.AuthService.login") as mock_login:
        mock_login.side_effect = HTTPException(status_code=400, detail="请先同意用户使用协议和隐私政策")
        response = client.post("/api/auth/login", json={"phone": "1234567890", "code": "12345678", "agree_protocol": False})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "请先同意用户使用协议和隐私政策"


def test_login_via_password_success(client):
    """测试密码登录成功的情况"""
    fake_user = UserResponse(
        id=1,
        phone="1234567890",
        status=True,
        created_at=datetime.now(),
    )
    fake_token = TokenResponse(access_token="fake-token", token_type="bearer", user=fake_user)
    with patch("app.api.v1.auth.AuthService.login_via_password") as mock_login:
        mock_login.return_value = fake_token
        response = client.post("/api/auth/login/password", json={"phone": "1234567890", "password": "correct-password", "agree_protocol": True})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["access_token"] == "fake-token"
        assert data["user"] == fake_user.model_dump(mode="json")


def test_login_via_password_invalid_password(client):
    """测试密码登录失败 - 密码错误"""
    with patch("app.api.v1.auth.AuthService.login_via_password") as mock_login:
        mock_login.side_effect = HTTPException(status_code=400, detail="密码错误")
        response = client.post("/api/auth/login/password", json={"phone": "1234567890", "password": "wrong-password", "agree_protocol": True})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "密码错误"


def test_login_via_password_user_not_found(client):
    """测试密码登录失败 - 用户不存在"""
    with patch("app.api.v1.auth.AuthService.login_via_password") as mock_login:
        mock_login.side_effect = HTTPException(status_code=400, detail="该手机号未注册")
        response = client.post("/api/auth/login/password", json={"phone": "0987654321", "password": "any-password", "agree_protocol": True})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "该手机号未注册"


def test_login_via_password_missing_fields(client):
    """测试密码登录失败 - 缺少必填字段"""
    response = client.post("/api/auth/login/password", json={"phone": "1234567890"})
    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert "detail" in data
    assert any(error["loc"][-1] == "password" for error in data["detail"])


def test_login_via_password_invalid_phone_format(client):
    """测试密码登录失败 - 手机号格式错误"""
    with patch("app.api.v1.auth.AuthService.login_via_password") as mock_login:
        mock_login.side_effect = HTTPException(status_code=400, detail="手机号格式错误")
        response = client.post("/api/auth/login/password", json={"phone": "invalid-phone", "password": "any-password", "agree_protocol": True})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "手机号格式错误"


def test_login_via_password_agree_protocol_false(client):
    """测试密码登录失败 - 不同意用户协议"""
    with patch("app.api.v1.auth.AuthService.login_via_password") as mock_login:
        mock_login.side_effect = HTTPException(status_code=400, detail="请先同意用户使用协议和隐私政策")
        response = client.post("/api/auth/login/password", json={"phone": "1234567890", "password": "any-password", "agree_protocol": False})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "请先同意用户使用协议和隐私政策"


def test_register_success(client):
    """测试注册成功的情况"""
    fake_user = UserResponse(
        id=1,
        phone="1234567890",
        status=True,
        created_at=datetime.now(),
    )
    fake_token = TokenResponse(access_token="fake-token", token_type="bearer", user=fake_user)
    with patch("app.api.v1.auth.AuthService.register") as mock_register:
        mock_register.return_value = fake_token
        response = client.post("/api/auth/register", json={"phone": "1234567890", "code": "12345678", "agree_protocol": True})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["access_token"] == "fake-token"
        assert data["user"] == fake_user.model_dump(mode="json")


def test_register_invalid_code(client):
    """测试注册失败 - 验证码错误"""
    with patch("app.api.v1.auth.AuthService.register") as mock_register:
        mock_register.side_effect = HTTPException(status_code=400, detail="验证码错误")
        response = client.post("/api/auth/register", json={"phone": "1234567890", "code": "wrong-code", "agree_protocol": True})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "验证码错误"


def test_register_phone_already_registered(client):
    """测试注册失败 - 手机号已注册"""
    with patch("app.api.v1.auth.AuthService.register") as mock_register:
        mock_register.side_effect = HTTPException(status_code=400, detail="该手机号已注册")
        response = client.post("/api/auth/register", json={"phone": "1234567890", "code": "12345678", "agree_protocol": True})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "该手机号已注册"


def test_register_missing_fields(client):
    """测试注册失败 - 缺少必填字段"""
    with patch("app.api.v1.auth.AuthService.register") as mock_register:
        response = client.post("/api/auth/register", json={"phone": "1234567890"})
        assert response.status_code == 422  # Unprocessable Entity
        data = response.json()
        assert "detail" in data
        assert any(error["loc"][-1] == "code" for error in data["detail"])


def test_register_invalid_phone_format(client):
    """测试注册失败 - 手机号格式错误"""
    with patch("app.api.v1.auth.AuthService.register") as mock_register:
        mock_register.side_effect = HTTPException(status_code=400, detail="手机号格式错误")
        response = client.post("/api/auth/register", json={"phone": "invalid-phone", "code": "12345678", "agree_protocol": True})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "手机号格式错误"


def test_register_agree_protocol_false(client):
    """测试注册失败 - 不同意用户协议"""
    with patch("app.api.v1.auth.AuthService.register") as mock_register:
        mock_register.side_effect = HTTPException(status_code=400, detail="请先同意用户使用协议和隐私政策")
        response = client.post("/api/auth/register", json={"phone": "1234567890", "code": "12345678", "agree_protocol": False})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "请先同意用户使用协议和隐私政策"


def test_register_agree_protocol_missing(client):
    """测试注册失败 - 缺少同意用户协议字段"""
    with patch("app.api.v1.auth.AuthService.register") as mock_register:
        mock_register.side_effect = HTTPException(status_code=422, detail="请先同意用户使用协议和隐私政策")
        response = client.post("/api/auth/register", json={"phone": "1234567890", "code": "12345678"})
        assert response.status_code == 422  # Unprocessable Entity
        data = response.json()
        assert "detail" in data
