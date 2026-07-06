"""
API 路由汇总
"""

from fastapi import APIRouter, Depends

from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.products import router as products_router
from backend.app.api.v1.klines import router as lines_router
from backend.common.security.rbac import DependsRBAC
v1 = APIRouter(prefix='/api')

# 公开路由（无需登录）
v1.include_router(auth_router)
v1.include_router(products_router)
v1.include_router(lines_router)

# 需要 RBAC 校验的路由（登录后才能访问）
# v1.include_router(klines_router, dependencies=[Depends(DependsRBAC)])
