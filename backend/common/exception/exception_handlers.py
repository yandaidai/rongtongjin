from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.common.exception.errors import BaseExceptionError
from backend.common.log import log
from backend.common.response.response_code import StandardResponseCode
from backend.common.response.response_schema import ResponseModel


async def base_exception_handler(request: Request, exc: BaseException) -> Any:
    """自定义异常处理器"""
    log.error(
        'BaseException | {method} {url} | code: {code} | msg: {msg}',
        method=request.method,
        url=request.url.path,
        code=exc.code,
        msg=exc.msg,
    )
    return ResponseModel.response(
        code=exc.code,
        msg=exc.msg,
        data=exc.data,
        status_code=exc.status_code,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> Any:
    """Pydantic 参数校验异常处理器"""
    errors = exc.errors()
    error_msgs = []
    for error in errors:
        loc = ' -> '.join(str(l) for l in error.get('loc', []))
        msg = error.get('msg', '')
        error_msgs.append(f'{loc}: {msg}')

    error_msg = '; '.join(error_msgs) if error_msgs else 'Validation Error'

    log.warning(
        'ValidationError | {method} {url} | errors: {errors}',
        method=request.method,
        url=request.url.path,
        errors=error_msg,
    )

    return ResponseModel.fail(
        msg=error_msg,
        code=StandardResponseCode.HTTP_422,
        status_code=StandardResponseCode.HTTP_422,
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> Any:
    """HTTP 异常处理器"""
    log.warning(
        'HTTPException | {method} {url} | status: {status} | detail: {detail}',
        method=request.method,
        url=request.url.path,
        status=exc.status_code,
        detail=exc.detail,
    )

    return ResponseModel.fail(
        msg=exc.detail,
        code=exc.status_code,
        status_code=exc.status_code,
    )


async def internal_exception_handler(request: Request, exc: Exception) -> Any:
    """未捕获异常处理器"""
    log.error(
        'InternalException | {method} {url} | error: {error}',
        method=request.method,
        url=request.url.path,
        error=str(exc),
    )

    return ResponseModel.error(
        msg='Internal Server Error',
    )


def register_exception(app: Any) -> None:
    """注册异常处理器"""
    from fastapi.exceptions import RequestValidationError
    from starlette.exceptions import HTTPException as StarletteHTTPException

    app.add_exception_handler(BaseExceptionError, base_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, internal_exception_handler)
