from typing import Any

from fastapi import status
from fastapi.responses import JSONResponse, Response

from backend.common.response.response_code import CustomResponseCode, StandardResponseCode


class ResponseModel:
    """统一响应模型"""

    @staticmethod
    def success(
        data: Any = None,
        msg: str = 'Success',
        code: int = CustomResponseCode.OK,
    ) -> JSONResponse:
        """成功响应"""
        return JSONResponse(
            content={
                'code': code,
                'msg': msg,
                'data': data,
            },
            status_code=StandardResponseCode.HTTP_200,
        )

    @staticmethod
    def fail(
        msg: str = 'Bad Request',
        code: int = StandardResponseCode.HTTP_400,
        data: Any = None,
        status_code: int = StandardResponseCode.HTTP_400,
    ) -> JSONResponse:
        """失败响应"""
        return JSONResponse(
            content={
                'code': code,
                'msg': msg,
                'data': data,
            },
            status_code=status_code,
        )

    @staticmethod
    def created(
        data: Any = None,
        msg: str = 'Created',
    ) -> JSONResponse:
        """创建成功"""
        return JSONResponse(
            content={
                'code': CustomResponseCode.OK,
                'msg': msg,
                'data': data,
            },
            status_code=StandardResponseCode.HTTP_201,
        )

    @staticmethod
    def error(
        msg: str = 'Internal Server Error',
        code: int = StandardResponseCode.HTTP_500,
        data: Any = None,
    ) -> JSONResponse:
        """服务器错误响应"""
        return JSONResponse(
            content={
                'code': code,
                'msg': msg,
                'data': data,
            },
            status_code=StandardResponseCode.HTTP_500,
        )

    @staticmethod
    def response(
        *,
        code: int,
        msg: str,
        data: Any = None,
        status_code: int = StandardResponseCode.HTTP_200,
    ) -> JSONResponse:
        """自定义响应"""
        return JSONResponse(
            content={
                'code': code,
                'msg': msg,
                'data': data,
            },
            status_code=status_code,
        )
