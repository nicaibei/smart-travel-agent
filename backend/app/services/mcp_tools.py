"""MCP工具集成 - 高德地图服务（简化版）"""
import requests
import json
from typing import Dict, Any, Optional
from app.config import get_settings


class MCPTools:
    """MCP工具集成类 - 直接调用高德地图API"""
    
    def __init__(self):
        """初始化MCP工具"""
        self.settings = get_settings()
        self.amap_key = self.settings.amap_web_key
        self.base_url = "https://restapi.amap.com/v3"
        
        print("✓ MCP工具初始化成功")
    
    def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """
        调用MCP工具
        
        Args:
            tool_name: 工具名称
            params: 参数
            
        Returns:
            工具调用结果
        """
        if tool_name == "amap_maps_text_search":
            return self.text_search(params)
        elif tool_name == "amap_weather_query":
            return self.weather_query(params)
        else:
            raise ValueError(f"未知工具: {tool_name}")
    
    def text_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        高德地图POI搜索
        
        Args:
            params: 搜索参数
                - keywords: 搜索关键词
                - city: 城市
                - types: POI类型（可选）
                
        Returns:
            搜索结果列表
        """
        try:
            url = f"{self.base_url}/place/text"
            
            request_params = {
                "key": self.amap_key,
                "keywords": params.get("keywords", ""),
                "city": params.get("city", ""),
                "offset": 20,  # 返回数量
                "page": 1,
                "extensions": "all"  # 返回详细信息
            }
            
            # 如果指定了types
            if params.get("types"):
                request_params["types"] = params["types"]
            
            response = requests.get(url, params=request_params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "1":
                pois = data.get("pois", [])
                print(f"  找到 {len(pois)} 个POI")
                return {"pois": pois, "count": len(pois)}
            else:
                print(f"  搜索失败: {data.get('info')}")
                return {"pois": [], "count": 0}
                
        except Exception as e:
            print(f"  POI搜索错误: {e}")
            return {"pois": [], "count": 0, "error": str(e)}
    
    def weather_query(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        查询天气信息
        
        Args:
            params: 查询参数
                - city: 城市名称或城市编码
                
        Returns:
            天气信息
        """
        try:
            url = f"{self.base_url}/weather/weatherInfo"
            
            request_params = {
                "key": self.amap_key,
                "city": params.get("city", ""),
                "extensions": "all"  # 返回预报天气
            }
            
            response = requests.get(url, params=request_params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "1":
                forecasts = data.get("forecasts", [])
                if forecasts:
                    print(f"  获取到 {forecasts[0]['city']} 的天气信息")
                    return forecasts[0]
                else:
                    print("  未获取到天气信息")
                    return {}
            else:
                print(f"  天气查询失败: {data.get('info')}")
                return {}
                
        except Exception as e:
            print(f"  天气查询错误: {e}")
            return {"error": str(e)}
    
    def geocode(self, address: str, city: Optional[str] = None) -> Dict[str, Any]:
        """
        地理编码 - 将地址转换为经纬度
        
        Args:
            address: 地址
            city: 城市（可选）
            
        Returns:
            经纬度信息
        """
        try:
            url = f"{self.base_url}/geocode/geo"
            
            request_params = {
                "key": self.amap_key,
                "address": address
            }
            
            if city:
                request_params["city"] = city
            
            response = requests.get(url, params=request_params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "1":
                geocodes = data.get("geocodes", [])
                if geocodes:
                    return geocodes[0]
            
            return {}
            
        except Exception as e:
            print(f"  地理编码错误: {e}")
            return {"error": str(e)}


# 全局实例
_mcp_tools_instance = None


def get_mcp_tools() -> MCPTools:
    """获取MCP工具实例（单例模式）"""
    global _mcp_tools_instance
    if _mcp_tools_instance is None:
        _mcp_tools_instance = MCPTools()
    return _mcp_tools_instance


# 导出
__all__ = ["MCPTools", "get_mcp_tools"]
