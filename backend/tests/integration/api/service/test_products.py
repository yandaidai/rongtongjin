"""贵金属品种接口测试"""

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.metal_product import MetalProduct


async def _seed_products(db: AsyncSession):
    """插入测试数据"""
    products = [
        MetalProduct(code="Au99.99", name="黄金99.99", unit="元/克"),
        MetalProduct(code="Ag99.99", name="白银99.99", unit="元/克"),
        MetalProduct(code="Pt99.95", name="铂金99.95", unit="元/克"),
    ]
    for p in products:
        db.add(p)
    await db.commit()


async def test_get_products_empty(async_client: AsyncClient):
    """测试获取品种列表（空数据）"""
    response = await async_client.get("/api/products/")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_products(async_client: AsyncClient, db: AsyncSession):
    """测试获取品种列表"""
    await _seed_products(db)

    response = await async_client.get("/api/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["code"] == "Au99.99"
