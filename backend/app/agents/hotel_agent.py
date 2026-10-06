"""酒店推荐智能体"""

HOTEL_AGENT_PROMPT = """你是酒店推荐专家。

**工具调用格式:**
`[TOOL_CALL:amap_maps_text_search:keywords=酒店,city=城市名]`

**示例:**
- `[TOOL_CALL:amap_maps_text_search:keywords=经济型酒店,city=北京]`
- `[TOOL_CALL:amap_maps_text_search:keywords=豪华酒店,city=上海]`

**重要:**
- 必须使用工具搜索,不要编造信息
- 根据用户住宿需求({accommodation_type})搜索{city}的酒店
- 考虑预算范围
"""

HOTEL_AGENT_SYSTEM = """你是一个专业的酒店推荐助手。
你的任务是根据用户的住宿需求和预算，搜索并推荐合适的酒店。

你必须：
1. 使用高德地图API搜索真实的酒店信息
2. 根据用户预算和需求筛选酒店
3. 返回结构化的酒店数据
"""


class HotelAgent:
    """酒店推荐智能体"""
    
    def __init__(self, llm_client, tools):
        self.llm_client = llm_client
        self.tools = tools
        self.prompt = HOTEL_AGENT_PROMPT
        self.system_message = HOTEL_AGENT_SYSTEM
    
    async def search_hotels(self, city: str, accommodation_type: str, budget: int = None) -> list:
        """
        搜索酒店
        
        Args:
            city: 城市名称
            accommodation_type: 住宿类型 (经济型/舒适型/豪华型)
            budget: 预算
            
        Returns:
            酒店列表
        """
        keywords = f"{accommodation_type or '经济型'}酒店"
        result = self.tools.call_tool("amap_maps_text_search", {
            "keywords": keywords, "city": city, "types": "100000",
        })
        return result.get("pois", []) if isinstance(result, dict) else []
