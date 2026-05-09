"""融通金 API - FastAPI 应用入口"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, products, quotes, klines, global_config, user_config, warns
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="融通金 - 黄金回收/交易平台 API",
    version="2.0.0",
)

# CORS 配置（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由（符合需求文档 API 规范）
app.include_router(auth.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(quotes.router, prefix="/api")
app.include_router(klines.router, prefix="/api")
app.include_router(global_config.router, prefix="/api")
app.include_router(user_config.router, prefix="/api")
app.include_router(warns.router, prefix="/api")


@app.get("/")
def root():
    """根路径"""
    return {"message": "融通金 API 服务运行中", "version": "2.0.0"}


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "ok"}
