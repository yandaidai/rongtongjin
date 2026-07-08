"""
JWT 认证中间件

支持双通道 Token 获取：
1. Authorization: Bearer <token>（API 调用）
2. Cookie: news_refresh_token=<token>（页面浏览）

刷新 Token 自动续期机制
"""

from typing import Any

from starlette.authentication import AuthCredentials, AuthenticationBackend, AuthenticationError, BaseUser, SimpleUser

from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings


class _User(BaseUser):
    """登录用户信息"""

    def __init__(
        self,
        user_id: int,
        username: str,
        nickname: str,
        is_superuser: bool = False,
    ):
        self.user_id = user_id
        self.username = username
        self.nickname = nickname
        self.is_superuser = is_superuser

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.nickname or self.username


class JwtAuthMiddleware(AuthenticationBackend):
    """JWT 认证中间件"""

    async def authenticate(self, conn: Any) -> tuple[AuthCredentials, _User] | None:
        """
        从请求中提取并验证 JWT Token

        优先级：Authorization Header > Cookie
        """
        token = None

        # 1. 尝试从 Authorization Header 获取
        auth_header = conn.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header[7:]

        # 2. 尝试从 Cookie 获取
        if not token:
            token = conn.cookies.get(settings.COOKIE_REFRESH_TOKEN_KEY)

        if not token:
            return None

        try:
            from jose import jwt as jose_jwt

            payload = jose_jwt.decode(
                token,
                settings.TOKEN_SECRET_KEY,
                algorithms=[settings.TOKEN_ALGORITHM],
            )

            user_id: int = payload.get('sub')
            username: str | None = payload.get('username')
            nickname: str = payload.get('nickname', username or '')
            is_superuser: bool = payload.get('is_superuser', False)
            token_type: str = payload.get('type', 'access')

            if user_id is None:
                raise errors.TokenError(msg='Token 格式无效')

            user = _User(
                user_id=user_id,
                username=username or '',
                nickname=nickname,
                is_superuser=is_superuser,
            )

            return AuthCredentials(scopes=[token_type]), user

        except errors.TokenError:
            raise
        except Exception as e:
            log.warning('JWT 认证失败: {error}', error=str(e))
            return None

    @staticmethod
    async def auth_exception_handler(conn: Any, exc: AuthenticationError) -> Any:
        """认证异常处理器"""
        from backend.common.response.response_code import CustomResponseCode, StandardResponseCode
        from backend.common.response.response_schema import ResponseModel

        return ResponseModel.fail(
            msg='认证失败，请重新登录',
            code=CustomResponseCode.TOKEN_INVALID,
        ).to_response(status_code=StandardResponseCode.HTTP_401)
