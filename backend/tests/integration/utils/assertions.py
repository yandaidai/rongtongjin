"""通用测试断言工具"""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import Response as HttpxResponse
from app.models.user import User


# ============================================================
# 响应断言助手
# ============================================================

def assert_api_success(response: HttpxResponse, expected_status: int = 200) -> dict[str, Any]:
    """
    断言 API 返回成功响应。

     验证：
    - HTTP 状态码符合预期
    - JSON body 包含 code / msg / data 三个字段
    - code 为 0（业务成功码）

    Args:
        response: httpx 响应对象
        expected_status: 期望的 HTTP 状态码，默认 200
    
    Returns:
        解析后的 JSON data 字段内容

    Raises:
        AssertionError: 任一验证失败
    """
    assert response.status_code == expected_status, (
        f'HTTP 状态码不匹配: 期望 {expected_status}, 实际 {response.status_code}\n'
        f'响应内容: {response.text}'
    )

    body = response.json()
    assert 'code' in body, f'响应 JSON 缺少 code 字段: {body}'
    assert 'msg' in body, f'响应 JSON 缺少 msg 字段: {body}'
    assert 'data' in body, f'响应 JSON 缺少 data 字段: {body}'

    code = body['code']
    assert code == 0, (
        f'业务响应码不为 0: code={code}, msg={body["msg"]}\n'
        f'完整响应: {body}'
    )

    return body['data']


def assert_api_error(
    response: HttpxResponse,
    expected_http_status: int = 400,
    expected_code: int | None = None
) -> dict[str, Any]:
    """
    断言 API 返回错误响应。

    Args:
        response: httpx 响应对象
        expected_http_status: 期望的 HTTP 状态码，默认 400
        expected_code: 期望的业务响应码（可选）

    Returns:
        完整的 JSON body
    """
    assert response.status_code == expected_http_status, (
        f'HTTP 状态码不匹配: 期望 {expected_http_status}, 实际 {response.status_code}\n'
        f'响应内容: {response.text}'
    )

    body = response.json()
    assert 'code' in body, f'响应 JSON 缺少 code 字段: {body}'
    assert 'msg' in body, f'响应 JSON 缺少 msg 字段: {body}'

    if expected_code is not None:
        code = body['code']
        assert code == expected_code, (
            f'业务响应码不匹配: 期望 {expected_code}, 实际 {code}, msg={body["msg"]}'
        )
    return body


def assert_ok(response, msg: str | None = None) -> dict:
    """断言 200 OK"""
    return assert_api_success(response, 200)


def assert_api_unauthorized(response: HttpxResponse) -> dict[str, Any]:
    """
    断言 API 返回未授权响应（401）。

    Args:
        response: httpx 响应对象

    Returns:
        完整的 JSON body
    """
    assert_api_error(response, expected_http_status=401)


def assert_api_not_found(response: HttpxResponse) -> None:
    """断言 API 返回 404 未找到"""
    assert_api_error(response, expected_http_status=404)


def assert_api_validation_error(response: HttpxResponse) -> None:
    """断言 API 返回 422 参数校验错误"""
    assert_api_error(response, expected_http_status=422)


def assert_bad_request(response, msg: str | None = None) -> dict:
    """断言 400 Bad Request"""
    return assert_api_error(response, 400, msg)


def assert_unauthorized(response, msg: str | None = None) -> dict:
    """断言 401 Unauthorized"""
    return assert_api_error(response, 401, msg)


def assert_has_token(data: dict) -> str:
    """断言响应含有 access_token，返回 token"""
    assert "access_token" in data, "响应中缺少 access_token"
    assert data.get("token_type") == "bearer", f"token_type 应为 bearer，实际为 {data.get('token_type')}"
    return data["access_token"]


def assert_user_fields(user_data: dict, *, phone: str | None = None, nickname: str | None = None):
    """断言用户信息的必要字段"""
    assert "id" in user_data, "缺少 id"
    if phone:
        assert user_data.get("phone") == phone, f"手机号不匹配"
    if nickname:
        assert user_data.get("nickname") == nickname, f"昵称不匹配"
    # 敏感字段不应泄露
    assert "hashed_password" not in user_data, "不应返回 hashed_password"
    assert "password" not in user_data, "不应返回 password"


def assert_error_msg(body: dict, keyword: str):
    """断言错误消息包含关键词（兼容 msg/detail 两种格式）"""
    msg = body.get("msg", body.get("detail", ""))
    assert keyword in msg, f"错误消息应包含 '{keyword}'，实际为 '{msg}'"


# ── 数据库断言 ──

async def assert_db_user_exists(db: AsyncSession, phone: str) -> User:
    """断言数据库中某手机号的用户存在，返回该用户"""
    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()
    assert user is not None, f"数据库中未找到手机号为 {phone} 的用户"
    return user


async def assert_db_user_not_exists(db: AsyncSession, phone: str):
    """断言数据库中某手机号的用户不存在"""
    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()
    assert user is None, f"数据库中手机号为 {phone} 的用户应不存在，但找到了"


async def assert_db_password_set(db: AsyncSession, phone: str):
    """断言用户已设置密码"""
    user = await assert_db_user_exists(db, phone)
    assert user.hashed_password is not None, f"用户 {phone} 密码应为非空"
    return user


async def assert_db_password_not_set(db: AsyncSession, phone: str):
    """断言用户未设置密码"""
    user = await assert_db_user_exists(db, phone)
    assert user.hashed_password is None, f"用户 {phone} 密码应为空"
    return user
