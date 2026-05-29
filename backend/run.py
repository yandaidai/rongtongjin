#!/usr/bin/env python3
"""启动入口：FastAPI + 行情定时任务"""

import uvicorn
from app.services.scheduler import start_scheduler


def main():
    start_scheduler()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
