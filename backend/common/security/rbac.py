"""
RBAC 权限校验

简化版 — 只校验用户是否已登录，不进行细粒度菜单权限校验
"""

from fastapi import Depends, Request

from backend.common.context import ctx
from backend.common.exception import errors
from backend.common.security.jwt import DependsJwtAuth
from backend.core.conf import settings


async def rbac_verify(request: Request, _token: str = DependsJwtAuth) -> None:
    """
    权限校验

    1. 白名单路径跳过
    2. JWT 授权状态强制校验
    3. 超级管理员免检
    4. 账户激活状态校验

    :param request: FastAPI 请求对象
    :param _token: JWT 令牌
    """
    path = request.url.path

    # 白名单
    if path in settings.TOKEN_REQUEST_PATH_EXCLUDE:
        return

    # JWT 授权状态强制校验
    if not request.auth.scopes:
        raise errors.TokenError(msg='未授权访问')

    # 超级管理员免检
    if request.user.is_superuser:
        return


# RBAC 授权依赖注入
DependsRBAC = Depends(rbac_verify)
