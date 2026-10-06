"""Unsplash图片服务"""
import requests
from typing import Optional, List, Dict
import logging
from app.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


class UnsplashService:
    """Unsplash图片服务"""

    def __init__(self, access_key: str):
        self.access_key = access_key
        self.base_url = "https://api.unsplash.com"

    def search_photos(self, query: str, per_page: int = 10) -> List[Dict]:
        """
        搜索图片
        
        Args:
            query: 搜索关键词
            per_page: 每页返回数量
            
        Returns:
            图片列表
        """
        try:
            url = f"{self.base_url}/search/photos"
            params = {
                "query": query,
                "per_page": per_page,
                "client_id": self.access_key
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])

            # 提取图片URL
            photos = []
            for result in results:
                photos.append({
                    "url": result["urls"]["regular"],
                    "thumbnail": result["urls"]["small"],
                    "description": result.get("description", ""),
                    "photographer": result["user"]["name"],
                    "photographer_url": result["user"]["links"]["html"]
                })

            return photos

        except Exception as e:
            logger.error(f"搜索图片失败: {e}")
            return []

    def get_photo_url(self, query: str) -> Optional[str]:
        """
        获取单张图片URL
        
        Args:
            query: 搜索关键词
            
        Returns:
            图片URL或None
        """
        photos = self.search_photos(query, per_page=1)
        return photos[0].get("url") if photos else None


# 全局实例
unsplash_service = UnsplashService(settings.unsplash_access_key)


def get_unsplash_service() -> UnsplashService:
    """获取Unsplash服务实例"""
    return unsplash_service
