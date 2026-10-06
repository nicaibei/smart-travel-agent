"""景点搜索智能体"""

ATTRACTION_AGENT_PROMPT = """你是景点搜索专家。

**工具调用格式:**
`[TOOL_CALL:amap_maps_text_search:keywords=景点,city=城市名]`

**示例:**
- `[TOOL_CALL:amap_maps_text_search:keywords=景点,city=北京]`
- `[TOOL_CALL:amap_maps_text_search:keywords=博物馆,city=上海]`

**重要:**
- 必须使用工具搜索,不要编造信息
- 根据用户偏好({preferences})搜索{city}的景点
"""

ATTRACTION_AGENT_SYSTEM = """你是一个专业的景点推荐助手。
你的任务是根据用户的偏好和目的地城市，搜索并推荐合适的景点。

你必须：
1. 使用高德地图API搜索真实的景点信息
2. 根据用户偏好筛选景点
3. 返回结构化的景点数据
"""


class AttractionAgent:
    """景点搜索智能体"""
    
    def __init__(self, llm_client, tools):
        self.llm_client = llm_client
        self.tools = tools
        self.prompt = ATTRACTION_AGENT_PROMPT
        self.system_message = ATTRACTION_AGENT_SYSTEM
    
    async def search_attractions(self, city: str, preferences: str | dict) -> list:
        """
        搜索景点
        
        Args:
            city: 城市名称
            preferences: 用户偏好
            
        Returns:
            景点列表
        """
        preference = preferences if isinstance(preferences, str) else preferences.get("interests", "")
        keywords = {
            "历史文化": "博物馆|古迹|历史景点",
            "自然风光": "公园|山|湖|风景区",
            "美食探索": "美食街|小吃街|特色餐厅",
            "购物娱乐": "商业街|购物中心|娱乐场所",
            "休闲度假": "度假村|温泉|休闲",
        }.get(preference, "景点")
        result = self.tools.call_tool("amap_maps_text_search", {
            "keywords": keywords, "city": city, "types": "",
        })
        return result.get("pois", []) if isinstance(result, dict) else []
