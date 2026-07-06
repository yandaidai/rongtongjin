"""
请求上下文

存储当前请求的上下文信息，用于日志追踪和权限校验
"""

from contextvars import ContextVar
from typing import Any

from starlette_context import context


class ContextHelper:
    """请求上下文辅助类"""

    def __init__(self):
        self._permission_ctx: ContextVar[str | None] = ContextVar('permission', default=None)

    @property
    def permission(self) -> str | None:
        """获取当前请求的权限标识"""
        return self._permission_ctx.get()

    @permission.setter
    def permission(self, value: str | None) -> None:
        """设置当前请求的权限标识"""
        self._permission_ctx.set(value)

    @property
    def trace_id(self) -> str | None:
        """获取当前请求的追踪 ID"""
        return context.get('X-Request-ID')

    @trace_id.setter
    def trace_id(self, value: str) -> None:
        context['X-Request-ID'] = value


# 全局上下文实例
ctx = ContextHelper()
