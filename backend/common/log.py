import os
import sys

from loguru import logger as log

from backend.core.conf import settings
from backend.core.path_conf import LOG_DIR


def setup_logging() -> None:
    """配置 Loguru 日志"""
    log.remove()

    # 控制台日志
    log.add(
        sys.stdout,
        level=settings.LOG_STD_LEVEL,
        format=settings.LOG_FORMAT,
        colorize=True,
    )

    # 确保日志目录存在
    os.makedirs(LOG_DIR, exist_ok=True)

    # 访问日志文件
    log.add(
        os.path.join(LOG_DIR, settings.LOG_ACCESS_FILENAME),
        level=settings.LOG_FILE_ACCESS_LEVEL,
        format=settings.LOG_FORMAT,
        rotation='1 day',
        retention='30 days',
        enqueue=True,
    )

    # 错误日志文件
    log.add(
        os.path.join(LOG_DIR, settings.LOG_ERROR_FILENAME),
        level=settings.LOG_FILE_ERROR_LEVEL,
        format=settings.LOG_FORMAT,
        rotation='1 day',
        retention='30 days',
        enqueue=True,
    )
