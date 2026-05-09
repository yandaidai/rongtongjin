"""用户自定义点差配置 API 路由"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.metal_user_config import MetalUserConfigResponse, MetalUserConfigUpdate
from app.services.config_service import UserConfigService

router = APIRouter(prefix="/user/config", tags=["用户点差配置"])


@router.get("/", response_model=list[MetalUserConfigResponse])
def get_user_configs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取当前用户的所有自定义点差配置"""
    service = UserConfigService(db)
    return service.get_user_configs(current_user.id)


@router.post("/", response_model=MetalUserConfigResponse)
def upsert_user_config(
    data: MetalUserConfigUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """创建或更新用户自定义点差配置"""
    service = UserConfigService(db)
    return service.upsert_config(current_user.id, data)
