# logger_config.py
import logging.config
from logging.handlers import RotatingFileHandler

# 日志配置字典
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,  # 不禁用已有的logger
    'formatters': {
        'standard': {  # 标准格式，包含时间、模块、级别、消息
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'detailed': {  # 更详细的格式，包含文件名和行号，方便调试
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {  # 控制台输出
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {  # 文件输出，带自动轮转
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': 'logs/app.log',  # 日志文件路径
            'maxBytes': 10 * 1024 * 1024,  # 单个文件最大10MB
            'backupCount': 5  # 保留5个旧文件
        }
    },
    'loggers': {
        '': {  # root logger 配置
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'uvicorn': {  # 单独控制 uvicorn 的日志级别，减少噪音
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'sqlalchemy.engine': {  # 控制 SQLAlchemy 的日志级别
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False
        }
    }
}

def setup_logging():
    """应用日志配置"""
    logging.config.dictConfig(LOGGING_CONFIG)