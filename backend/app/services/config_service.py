"""点差配置服务"""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.metal_global_config import MetalGlobalConfig
from app.models.metal_product import MetalProduct
from app.models.metal_user_config import MetalUserConfig
from app.schemas.metal_global_config import MetalGlobalConfigResponse, MetalGlobalConfigUpdate
from app.schemas.metal_user_config import MetalUserConfigResponse, MetalUserConfigUpdate


class GlobalConfigService:
    """全局默认点差配置服务"""

    def __init__(self, db: Session):
        self.db = db

    def get_all_configs(self) -> list[MetalGlobalConfigResponse]:
        """获取所有全局点差配置"""
        configs = self.db.query(MetalGlobalConfig).filter(
            MetalGlobalConfig.status == True
        ).all()
        return [MetalGlobalConfigResponse.model_validate(c) for c in configs]

    def get_config_by_product(self, product_id: int) -> MetalGlobalConfigResponse:
        """获取指定品种的全局点差配置"""
        config = self.db.query(MetalGlobalConfig).filter(
            MetalGlobalConfig.product_id == product_id,
            MetalGlobalConfig.status == True,
        ).first()
        if not config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到该品种的点差配置",
            )
        return MetalGlobalConfigResponse.model_validate(config)

    def update_config(
        self, product_id: int, data: MetalGlobalConfigUpdate
    ) -> MetalGlobalConfigResponse:
        """更新指定品种的全局点差配置"""
        config = self.db.query(MetalGlobalConfig).filter(
            MetalGlobalConfig.product_id == product_id,
        ).first()

        if not config:
            # 如果不存在则创建
            config = MetalGlobalConfig(product_id=product_id)
            self.db.add(config)

        if data.sell_add_price is not None:
            config.sell_add_price = data.sell_add_price
        if data.buy_back_sub_price is not None:
            config.buy_back_sub_price = data.buy_back_sub_price

        self.db.commit()
        self.db.refresh(config)
        return MetalGlobalConfigResponse.model_validate(config)


class UserConfigService:
    """用户自定义点差配置服务"""

    def __init__(self, db: Session):
        self.db = db

    def get_user_configs(self, user_id: int) -> list[MetalUserConfigResponse]:
        """获取用户的所有自定义点差配置"""
        configs = self.db.query(MetalUserConfig).filter(
            MetalUserConfig.user_id == user_id,
            MetalUserConfig.status == True,
        ).all()
        return [MetalUserConfigResponse.model_validate(c) for c in configs]

    def get_user_config_by_product(
        self, user_id: int, product_id: int
    ) -> Optional[MetalUserConfigResponse]:
        """获取用户指定品种的自定义点差配置"""
        config = self.db.query(MetalUserConfig).filter(
            MetalUserConfig.user_id == user_id,
            MetalUserConfig.product_id == product_id,
            MetalUserConfig.status == True,
        ).first()
        if not config:
            return None
        return MetalUserConfigResponse.model_validate(config)

    def upsert_config(
        self, user_id: int, data: MetalUserConfigUpdate
    ) -> MetalUserConfigResponse:
        """创建或更新用户自定义点差配置"""
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

        config = self.db.query(MetalUserConfig).filter(
            MetalUserConfig.user_id == user_id,
            MetalUserConfig.product_id == data.product_id,
        ).first()

        if not config:
            config = MetalUserConfig(
                user_id=user_id,
                product_id=data.product_id,
            )
            self.db.add(config)

        if data.sell_add_price is not None:
            config.sell_add_price = data.sell_add_price
        if data.buy_back_sub_price is not None:
            config.buy_back_sub_price = data.buy_back_sub_price

        config.status = True
        self.db.commit()
        self.db.refresh(config)
        return MetalUserConfigResponse.model_validate(config)
