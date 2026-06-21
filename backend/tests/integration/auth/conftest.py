import pytest
from app.models import User
from app.core.security import hash_password


def clear_users(session):
    """清空 users 表 — 公共函数，供各 fixture 调用"""
    session.query(User).delete()
    session.flush()


@pytest.fixture
def auth_empty_db(test_session):
    """
    场景1：空数据库（没有任何用户）
    用于测试注册、首次登录等场景
    """
    clear_users(test_session)
    yield {}
    # 无需清理，事务会自动回滚


@pytest.fixture
def auth_user_with_password(test_session):
    """
    场景2：已注册且设置了密码的用户
    用于测试密码登录、修改密码等场景
    """
    clear_users(test_session)

    user = User(
        phone="13800138000",
        nickname="完整用户",
        email="user@example.com",
        hashed_password=hash_password("Test@123"),
    )
    test_session.add(user)
    test_session.flush()

    yield {
        "user": user,
        "phone": user.phone,
        "password": "Test@123",
        "nickname": user.nickname,
        "email": user.email,
    }


@pytest.fixture
def auth_user_without_password(test_session):
    """
    场景3：已注册但未设置密码的用户
    用于测试"未设置密码"的提示、设置密码流程等
    """
    clear_users(test_session)

    user = User(
        phone="13800138001",
        nickname="无密码用户",
        email=None,
        hashed_password=None,  # 未设置密码
    )
    test_session.add(user)
    test_session.flush()

    yield {
        "user": user,
        "phone": user.phone,
        "nickname": user.nickname,
    }


@pytest.fixture
def auth_user_without_email(test_session):
    """
    场景4：已注册但未绑定邮箱的用户
    用于测试邮箱绑定流程
    """
    clear_users(test_session)

    user = User(
        phone="13800138002",
        nickname="无邮箱用户",
        email=None,
        hashed_password=hash_password("Test@456"),
    )
    test_session.add(user)
    test_session.flush()

    yield {
        "user": user,
        "phone": user.phone,
        "password": "Test@456",
    }


@pytest.fixture
def auth_user_without_phone(test_session):
    """
    场景5：未注册的手机号
    用于测试注册流程
    """
    clear_users(test_session)

    yield {
        "phone": "13800138999",  # 未注册的手机号
    }