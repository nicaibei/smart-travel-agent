"""LLM客户端配置"""
from openai import AsyncOpenAI
from app.config import get_settings

settings = get_settings()


def create_llm_client() -> AsyncOpenAI:
    """
    创建OpenAI异步客户端
    
    Returns:
        AsyncOpenAI客户端实例
    """
    client = AsyncOpenAI(
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
        timeout=settings.llm_timeout,
    )
    return client


# 全局LLM客户端实例
llm_client = create_llm_client()


def get_llm_client() -> AsyncOpenAI:
    """获取LLM客户端"""
    return llm_client
