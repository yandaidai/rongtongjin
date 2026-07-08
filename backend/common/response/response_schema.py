"""统一响应模型（泛型）

使用方式：

    # 路由装饰器 — 自动生成 OpenAPI 文档
    @router.get("/products", response_model=ResponseModel[List[MetalProductResponse]])
    async def get_products():
        return ResponseModel.success(data=products)

    # 异常处理器 — 序列化为 JSONResponse
    return ResponseModel.fail(msg="...").to_response(status_code=400)
"""

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

from fastapi.responses import JSONResponse

from backend.common.response.response_code import StandardResponseCode

DataT = TypeVar("DataT")


class ResponseModel(BaseModel, Generic[DataT]):
    """统一响应模型"""

    code: int
    msg: str = "Success"
    data: Optional[DataT] = None

    @classmethod
    def success(
        cls,
        data: DataT = None,
        msg: str = "Success",
        code: int = StandardResponseCode.HTTP_200,
    ) -> "ResponseModel[DataT]":
        """成功响应"""
        return cls(code=code, msg=msg, data=data)

    @classmethod
    def fail(
        cls,
        msg: str = "Bad Request",
        data: Any = None,
        code: int = StandardResponseCode.HTTP_400,
    ) -> "ResponseModel[Any]":
        """失败响应"""
        return cls(code=code, msg=msg, data=data)

    @classmethod
    def error(
        cls,
        msg: str = "Internal Server Error",
        data: Any = None,
        code: int = StandardResponseCode.HTTP_500,
    ) -> "ResponseModel[Any]":
        """服务器错误响应"""
        return cls(code=code, msg=msg, data=data)

    def to_response(self, status_code: int = StandardResponseCode.HTTP_200) -> JSONResponse:
        """序列化为 JSONResponse（用于异常处理器）"""
        return JSONResponse(
            content=self.model_dump(),
            status_code=status_code,
        )
