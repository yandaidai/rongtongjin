"""全局点差配置 API 路由"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.metal_global_config import MetalGlobalConfigResponse, MetalGlobalConfigUpdate
from app.services.config_service import GlobalConfigService

router = APIRouter(prefix="/global/config", tags=["全局点差配置"])


@router.get("/", response_model=list[MetalGlobalConfigResponse])
def get_global_configs(db: Session = Depends(get_db)):
    """获取所有默认销售价&回购价点差"""
    service = GlobalConfigService(db)
    return service.get_all_configs()


@router.get("/{product_id}", response_model=MetalGlobalConfigResponse)
def get_global_config_by_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    """获取指定品种的默认点差配置"""
    service = GlobalConfigService(db)
    return service.get_config_by_product(product_id)


@router.patch("/{product_id}", response_model=MetalGlobalConfigResponse)
def update_global_config(
    product_id: int,
    data: MetalGlobalConfigUpdate,
    db: Session = Depends(get_db),
):
    """更新指定品种的默认点差配置"""
    service = GlobalConfigService(db)
    return service.update_config(product_id, data)
