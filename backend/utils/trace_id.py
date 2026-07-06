import uuid

from backend.core.conf import settings


def get_trace_id() -> str:
    """
    生成请求追踪 ID

    用于串联单次请求的所有日志
    :return:
    """
    trace_id = uuid.uuid4().hex[:settings.TRACE_ID_LOG_LENGTH]
    return trace_id
