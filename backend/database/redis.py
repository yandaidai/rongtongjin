import sys

from redis.asyncio import Redis
from redis.exceptions import AuthenticationError, TimeoutError

from backend.common.log import log
from backend.core.conf import settings


class RedisCli(Redis):
    """Redis 客户端封装"""

    def __init__(
        self,
        host: str = settings.REDIS_HOST,
        port: int = settings.REDIS_PORT,
        password: str = settings.REDIS_PASSWORD,
        db: int = settings.REDIS_DATABASE,
        socket_timeout: int | None = settings.REDIS_TIMEOUT,
        socket_connect_timeout: int = settings.REDIS_TIMEOUT,
        *,
        socket_keepalive: bool = True,
        health_check_interval: int = 30,
        decode_responses: bool = True,
    ) -> None:
        super().__init__(
            host=host,
            port=port,
            password=password,
            db=db,
            socket_timeout=socket_timeout,
            socket_connect_timeout=socket_connect_timeout,
            socket_keepalive=socket_keepalive,
            health_check_interval=health_check_interval,
            decode_responses=decode_responses,
        )

    async def init(self) -> None:
        """初始化 Redis 连接"""
        try:
            await self.ping()
        except TimeoutError:
            log.error('Redis 服务器连接超时')
            sys.exit()
        except AuthenticationError:
            log.error('Redis 服务器连接认证失败')
            sys.exit()
        except Exception as e:
            log.error('Redis 服务器连接异常 {error}', error=e)
            sys.exit()

    async def delete_prefix(self, prefix: str, exclude: str | list[str] | None = None, batch_size: int = 1000) -> None:
        """删除指定前缀的所有 key"""
        exclude_set = set(exclude) if isinstance(exclude, list) else {exclude} if isinstance(exclude, str) else set()
        batch_keys = []

        async for key in self.scan_iter(match=f'{prefix}*'):
            if key not in exclude_set:
                batch_keys.append(key)
                if len(batch_keys) >= batch_size:
                    await self.delete(*batch_keys)
                    batch_keys.clear()

        if batch_keys:
            await self.delete(*batch_keys)


# Redis 客户端单例
redis_client: RedisCli = RedisCli()
