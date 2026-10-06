# services package
from app.config import get_settings
from .unsplash_service import UnsplashService

def get_unsplash_service():
    """获取Unsplash服务实例"""
    settings = get_settings()
    return UnsplashService(access_key=settings.unsplash_access_key)

__all__ = ["UnsplashService", "get_unsplash_service"]
