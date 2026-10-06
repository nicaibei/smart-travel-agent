"""启动脚本"""
import uvicorn
from app.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    print("=" * 60)
    print("🚀 智能旅行助手 API 启动中...")
    print("=" * 60)
    print(f"📍 Host: {settings.host}")
    print(f"📍 Port: {settings.port}")
    print(f"🤖 LLM Model: {settings.llm_model_id}")
    print(f"🗺️  AMAP Key: {settings.amap_web_key[:10]}...")
    print("=" * 60)
    print(f"📖 API文档: http://{settings.host}:{settings.port}/docs")
    print(f"🔍 健康检查: http://{settings.host}:{settings.port}/api/trip/health")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level="info"
    )
