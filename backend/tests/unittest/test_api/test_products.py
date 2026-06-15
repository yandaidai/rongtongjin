import pytest
from fastapi import HTTPException
from datetime import datetime
from unittest.mock import patch, MagicMock
from app.schemas.user import TokenResponse, UserResponse

#标记为单元测试（可选）
pytestmark = pytest.mark.unit

def test_get_all_products_success(client):
    """测试获取所有启用的贵金属品种成功的情况"""
    fake_products = [
        {"id": 1, "name": "黄金", "code": "AU", "unit": "克", "status": True, "created_at": datetime.now()},
        {"id": 2, "name": "白银", "code": "AG", "unit": "克", "status": True, "created_at": datetime.now()},
    ]
    with patch("app.api.v1.products.ProductService.get_all_products") as mock_get_all:
        mock_get_all.return_value = fake_products
        response = client.get("/api/products/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["name"] == "黄金"
        assert data[1]["name"] == "白银"


def test_get_all_products_empty(client):
    """测试获取所有启用的贵金属品种为空的情况"""
    with patch("app.api.v1.products.ProductService.get_all_products") as mock_get_all:
        mock_get_all.return_value = []
        response = client.get("/api/products/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0


def test_get_all_products_exception(client):
    """测试获取所有启用的贵金属品种发生异常的情况"""
    with patch("app.api.v1.products.ProductService.get_all_products") as mock_get_all:
        mock_get_all.side_effect = Exception("Failed to fetch products")
        response = client.get("/api/products/")
        # FastAPI 默认异常处理器不会直接把异常 message 暴露给客户端
        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "Failed to fetch products"
