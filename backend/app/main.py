"""FastAPI应用主入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import trip

app = FastAPI(
    title="智能旅行助手API",
    description="基于AI的智能旅行规划助手",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需要限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(trip.router)


@app.get("/")
async def root():
    """健康检查"""
    return {"status": "ok", "message": "智能旅行助手API正在运行"}


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}
