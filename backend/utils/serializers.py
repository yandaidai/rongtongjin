import orjson

from typing import Any

from fastapi.responses import JSONResponse


class MsgSpecJSONResponse(JSONResponse):
    """
    基于 orjson 的高性能 JSON 响应

    orjson 比标准 json 库快 3-5 倍，支持 bytes、datetime 等类型自动序列化
    """

    def render(self, content: Any) -> bytes:
        return orjson.dumps(
            content,
            default=self._serialize_default,
            option=orjson.OPT_UTC_Z | orjson.OPT_SERIALIZE_NUMPY,
        )

    @staticmethod
    def _serialize_default(obj: Any) -> str:
        raise TypeError(f'Type {type(obj)} not serializable')
