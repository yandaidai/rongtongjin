"""用户价格预警服务"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.metal_product import MetalProduct
from app.models.metal_warn import MetalWarn
from app.schemas.metal_warn import MetalWarnCreate, MetalWarnResponse, MetalWarnUpdate


class WarnService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_warns(self, user_id: int) -> list[MetalWarnResponse]:
        """获取用户的所有预警配置"""
        warns = self.db.query(MetalWarn).filter(
            MetalWarn.user_id == user_id,
        ).all()
        return [MetalWarnResponse.model_validate(w) for w in warns]

    def get_warn(self, warn_id: int, user_id: int) -> MetalWarnResponse:
        """获取单个预警配置"""
        warn = self.db.query(MetalWarn).filter(
            MetalWarn.id == warn_id,
            MetalWarn.user_id == user_id,
        ).first()
        if not warn:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="预警配置不存在",
            )
        return MetalWarnResponse.model_validate(warn)

    def create_warn(self, user_id: int, data: MetalWarnCreate) -> MetalWarnResponse:
        """创建价格预警"""
        # 检查品种是否存在
        product = self.db.query(MetalProduct).filter(
            MetalProduct.id == data.product_id,
            MetalProduct.status == True,
        ).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="贵金属品种不存在",
            )

        # 检查是否已存在该品种的预警
        existing = self.db.query(MetalWarn).filter(
            MetalWarn.user_id == user_id,
            MetalWarn.product_id == data.product_id,
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该品种已存在预警配置",
            )

        warn = MetalWarn(
            user_id=user_id,
            product_id=data.product_id,
            upper_limit=data.upper_limit,
            lower_limit=data.lower_limit,
            warn_enable=data.warn_enable,
        )
        self.db.add(warn)
        self.db.commit()
        self.db.refresh(warn)
        return MetalWarnResponse.model_validate(warn)

    def update_warn(
        self, warn_id: int, user_id: int, data: MetalWarnUpdate
    ) -> MetalWarnResponse:
        """更新价格预警"""
        warn = self.db.query(MetalWarn).filter(
            MetalWarn.id == warn_id,
            MetalWarn.user_id == user_id,
        ).first()
        if not warn:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="预警配置不存在",
            )

        if data.upper_limit is not None:
            warn.upper_limit = data.upper_limit
            warn.upper_trigger = False  # 修改后重置触发状态
        if data.lower_limit is not None:
            warn.lower_limit = data.lower_limit
            warn.lower_trigger = False
        if data.warn_enable is not None:
            warn.warn_enable = data.warn_enable

        self.db.commit()
        self.db.refresh(warn)
        return MetalWarnResponse.model_validate(warn)

    def delete_warn(self, warn_id: int, user_id: int) -> dict:
        """删除价格预警"""
        warn = self.db.query(MetalWarn).filter(
            MetalWarn.id == warn_id,
            MetalWarn.user_id == user_id,
        ).first()
        if not warn:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="预警配置不存在",
            )

        self.db.delete(warn)
        self.db.commit()
        return {"message": "预警已删除"}
