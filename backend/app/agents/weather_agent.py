"""天气查询智能体"""

WEATHER_AGENT_PROMPT = """你是天气查询专家。

**工具调用格式:**
`[TOOL_CALL:amap_weather_query:city=城市名]`

**示例:**
- `[TOOL_CALL:amap_weather_query:city=北京]`
- `[TOOL_CALL:amap_weather_query:city=上海]`

**重要:**
- 必须使用工具查询真实天气数据
- 查询{city}在{start_date}到{end_date}期间的天气
- 提供穿衣建议
"""

WEATHER_AGENT_SYSTEM = """你是一个专业的天气查询助手。
你的任务是查询目的地的天气信息，并提供相关建议。

你必须：
1. 使用高德地图API查询真实的天气数据
2. 分析天气对旅行的影响
3. 提供穿衣和出行建议
"""


class WeatherAgent:
    """天气查询智能体"""
    
    def __init__(self, llm_client, tools):
        self.llm_client = llm_client
        self.tools = tools
        self.prompt = WEATHER_AGENT_PROMPT
        self.system_message = WEATHER_AGENT_SYSTEM
    
    async def query_weather(self, city: str, start_date: str, end_date: str) -> list:
        """
        查询天气信息
        
        Args:
            city: 城市名称
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            天气信息列表
        """
        result = self.tools.call_tool("amap_weather_query", {"city": city})
        if not isinstance(result, dict):
            return []
        return result.get("casts", []) or []
