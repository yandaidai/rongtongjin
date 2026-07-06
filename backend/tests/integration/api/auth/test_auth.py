"""用户认证接口测试 - 手机验证码方式（全异步）"""

from httpx import AsyncClient

from tests.integration.utils.assertions import (
    assert_bad_request,
    assert_unauthorized,
    assert_api_not_found,
    assert_has_token,
    assert_user_fields,
    assert_error_msg,
    assert_db_user_exists,
)


async def test_register_success(async_client: AsyncClient, auth_empty_db, test_db_session):
    """测试用户注册成功"""
    phone = auth_empty_db.get("unregistered_phone", "13800138000")
    response = await async_client.post("/api/auth/register", json={
        "phone": phone,
        "code": "123456",
        "agree_protocol": True,
    })

    assert response.status_code == 200
    data = response.json()
    assert_has_token(data)

    user_data = data["user"]
    expected_nickname = f"用户{phone[-4:]}"
    assert_user_fields(user_data, phone=phone, nickname=expected_nickname)

    db_user = await assert_db_user_exists(test_db_session, phone)
    assert db_user.nickname == expected_nickname
    assert db_user.hashed_password is None
    assert db_user.created_at is not None


async def test_register_without_agreement(async_client: AsyncClient):
    """测试未同意协议注册"""
    response = await async_client.post("/api/auth/register", json={
        "phone": "13800138002",
        "code": "123456",
        "agree_protocol": False,
    })
    body = assert_bad_request(response)
    assert_error_msg(body, "同意")


async def test_register_wrong_code(async_client: AsyncClient):
    """测试错误验证码注册"""
    response = await async_client.post("/api/auth/register", json={
        "phone": "13800138003",
        "code": "000000",
        "agree_protocol": True,
    })
    body = assert_bad_request(response)
    assert_error_msg(body, "验证码错误")


async def test_register_duplicate_phone(async_client: AsyncClient, auth_user_without_password):  # noqa: ARG001
    """测试重复手机号注册"""
    response = await async_client.post("/api/auth/register", json={
        "phone": "13800138001",
        "code": "123456",
        "agree_protocol": True,
    })
    body = assert_bad_request(response)
    assert_error_msg(body, "已注册")


async def test_login_success(async_client: AsyncClient):
    """测试登录成功"""
    await async_client.post("/api/auth/register", json={
        "phone": "13800138005",
        "code": "123456",
        "agree_protocol": True,
    })
    response = await async_client.post("/api/auth/login", json={
        "phone": "13800138005",
        "code": "123456",
    })
    assert response.status_code == 200
    data = response.json()
    assert_has_token(data)
    assert data["user"]["phone"] == "13800138005"


async def test_login_wrong_code(async_client: AsyncClient):
    """测试错误验证码登录"""
    await async_client.post("/api/auth/register", json={
        "phone": "13800138006",
        "code": "123456",
        "agree_protocol": True,
    })
    response = await async_client.post("/api/auth/login", json={
        "phone": "13800138006",
        "code": "000000",
    })
    assert_bad_request(response)


async def test_login_user_not_found(async_client: AsyncClient):
    """测试未注册用户登录"""
    response = await async_client.post("/api/auth/login", json={
        "phone": "13900139000",
        "code": "123456",
    })
    assert_api_not_found(response)


async def test_get_user_info(async_client: AsyncClient):
    """测试获取用户信息"""
    reg = await async_client.post("/api/auth/register", json={
        "phone": "13800138007",
        "code": "123456",
        "agree_protocol": True,
    })
    token = assert_has_token(reg.json())

    response = await async_client.get(
        "/api/auth/user/info",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["phone"] == "13800138007"


async def test_get_user_info_unauthorized(async_client: AsyncClient):
    """测试未授权访问用户信息"""
    response = await async_client.get("/api/auth/user/info")
    assert_unauthorized(response)


async def test_update_nickname(async_client: AsyncClient):
    """测试更新昵称"""
    reg = await async_client.post("/api/auth/register", json={
        "phone": "13800138008",
        "code": "123456",
        "agree_protocol": True,
    })
    token = assert_has_token(reg.json())

    response = await async_client.patch(
        "/api/auth/user/nickname",
        headers={"Authorization": f"Bearer {token}"},
        json={"nickname": "新昵称"},
    )
    assert response.status_code == 200
    assert response.json()["nickname"] == "新昵称"


async def test_update_avatar(async_client: AsyncClient):
    """测试更新头像"""
    reg = await async_client.post("/api/auth/register", json={
        "phone": "13800138009",
        "code": "123456",
        "agree_protocol": True,
    })
    token = assert_has_token(reg.json())

    response = await async_client.patch(
        "/api/auth/user/avatar",
        headers={"Authorization": f"Bearer {token}"},
        json={"avatar": "https://example.com/avatar.jpg"},
    )
    assert response.status_code == 200
    assert response.json()["avatar"] == "https://example.com/avatar.jpg"


async def test_set_password(async_client: AsyncClient):
    """测试设置密码"""
    reg = await async_client.post("/api/auth/register", json={
        "phone": "13800138010",
        "code": "123456",
        "agree_protocol": True,
    })
    token = assert_has_token(reg.json())

    response = await async_client.post(
        "/api/auth/user/password",
        headers={"Authorization": f"Bearer {token}"},
        json={"password": "newpassword123"},
    )
    assert response.status_code == 200
    assert "成功" in response.json().get("msg", response.json().get("message", ""))


async def test_deactivate_account(async_client: AsyncClient):
    """测试注销账号"""
    reg = await async_client.post("/api/auth/register", json={
        "phone": "13800138011",
        "code": "123456",
        "agree_protocol": True,
    })
    token = assert_has_token(reg.json())

    response = await async_client.delete(
        "/api/auth/user/account",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert "注销" in response.json().get("msg", response.json().get("message", ""))
