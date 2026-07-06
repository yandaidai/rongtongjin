"""
应用级路由汇总
"""

from fastapi import APIRouter

from backend.app.api.router import v1

router = APIRouter()

router.include_router(v1)