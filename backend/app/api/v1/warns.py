"""用户价格预警 API 路由"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.core.dependencies import get_current_user
from backend.database.db import get_db
from app.models.user import User
from app.schemas.metal_warn import MetalWarnCreate, MetalWarnResponse, MetalWarnUpdate
from app.services.warn_service import WarnService

router = APIRouter(prefix="/user/warn", tags=["价格预警"])


@router.get("/", response_model=list[MetalWarnResponse])
def get_warns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取当前用户的所有预警配置"""
    service = WarnService(db)
    return service.get_user_warns(current_user.id)


@router.get("/{warn_id}", response_model=MetalWarnResponse)
def get_warn(
    warn_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取单个预警配置"""
    service = WarnService(db)
    return service.get_warn(warn_id, current_user.id)


@router.post("/", response_model=MetalWarnResponse)
def create_warn(
    data: MetalWarnCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """创建价格预警"""
    service = WarnService(db)
    return service.create_warn(current_user.id, data)


@router.patch("/{warn_id}", response_model=MetalWarnResponse)
def update_warn(
    warn_id: int,
    data: MetalWarnUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新价格预警"""
    service = WarnService(db)
    return service.update_warn(warn_id, current_user.id, data)


@router.delete("/{warn_id}")
def delete_warn(
    warn_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除价格预警"""
    service = WarnService(db)
    return service.delete_warn(warn_id, current_user.id)
