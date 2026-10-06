"""应用配置"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用设置"""
    
    # 高德地图配置
    amap_web_key: str = ""
    amap_js_key: str = ""
    amap_security_code: str = ""
    
    # Unsplash配置
    unsplash_access_key: str = ""
    unsplash_secret_key: str = ""
    
    # LLM配置 (通义千问/阿里云)
    llm_api_key: str = ""
    llm_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    llm_model_id: str = "qwen-turbo"
    llm_timeout: int = 60
    
    # 服务配置
    host: str = "127.0.0.1"
    port: int = 8000
    
    class Config:
        # 从项目根目录加载配置，避免从 backend/ 启动时找不到根目录 .env。
        env_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
        env_file_encoding = "utf-8"
        # 环境变量名转换：LLM_API_KEY -> llm_api_key
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()
