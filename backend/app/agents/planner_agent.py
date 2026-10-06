"""行程规划智能体 - 整合所有信息生成完整旅行计划"""

PLANNER_AGENT_PROMPT = """你是行程规划专家。

**你的任务:**
整合景点、天气、酒店信息，生成合理的旅行计划。

**输入信息:**
- 用户需求: {user_request}
- 同行人群: {traveler_type}
- 行程节奏: {travel_pace}
- 用户额外要求: {special_requirements}
- 景点列表: {attractions}
- 天气信息: {weather}
- 酒店列表: {hotels}

**规划原则:**
1. 根据天气安排室内/室外活动
2. 合理安排每日游览时间(避免过度疲劳)
3. 考虑景点之间的距离
4. 预留用餐和休息时间
5. 计算总预算
6. 优先满足用户填写的额外出行要求；若与天气、开放时间或安全冲突，要明确说明并给出替代安排
7. 根据同行人群调整步行距离、活动类型和休息安排；严格遵循用户选择的行程节奏

**输出格式（字段名和类型必须遵守；days 必须是数组，不是天数）:**
{{
  "city": "城市名",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "days": [{{
    "date": "YYYY-MM-DD", "day_index": 0, "description": "当日安排",
    "transportation": "交通方式", "accommodation": "住宿安排",
    "attractions": [{{"name": "必须来自景点列表", "address": "地址", "location": {{"longitude": 0.0, "latitude": 0.0}}, "visit_duration": 120, "description": "介绍", "category": "类别", "ticket_price": 0}}],
    "meals": [{{"type": "lunch", "name": "餐厅", "address": "地址", "description": "推荐", "estimated_cost": 0}}]
  }}],
  "weather_info": [{{"date": "YYYY-MM-DD", "day_weather": "天气", "night_weather": "天气", "day_temp": 20, "night_temp": 12, "wind_direction": "风向", "wind_power": "风力"}}],
  "overall_suggestions": "建议",
  "budget": {{"total_attractions": 0, "total_hotels": 0, "total_meals": 0, "total_transportation": 0, "total": 0, "planned_budget": 0, "remaining": 0}}
}}

城市、日期必须照抄用户需求；景点只能从输入列表中选择，不得编造名称或坐标。酒店列表为空时不要编造具体酒店。
"""

PLANNER_AGENT_SYSTEM = """你是一个专业的旅行规划师。
你的任务是将各个专家提供的信息整合成一个完整、可执行的旅行计划。

你必须：
1. 合理安排每日行程顺序
2. 考虑时间、距离、天气等因素
3. 提供详细的交通、住宿、餐饮建议
4. 计算详细的预算
5. 给出旅行注意事项和建议

重要：
- 不需要调用任何工具，专注于信息整合
- 确保行程合理、可行
- 提供备选方案
"""


class PlannerAgent:
    """行程规划智能体"""
    
    def __init__(self, llm_client, model: str = "qwen-turbo"):
        self.llm_client = llm_client
        self.model = model
        self.prompt = PLANNER_AGENT_PROMPT
        self.system_message = PLANNER_AGENT_SYSTEM
    
    async def generate_plan(
        self,
        user_request: dict,
        attractions: list,
        weather: list,
        hotels: list
    ) -> dict:
        """
        生成完整旅行计划
        
        Args:
            user_request: 用户需求 (城市、日期、偏好、预算等)
            attractions: 景点列表
            weather: 天气信息列表
            hotels: 酒店列表
            
        Returns:
            TripPlan 字典
        """
        prompt = self.prompt.format(
            user_request=user_request,
            traveler_type=user_request.get("traveler_type") or "未指定",
            travel_pace=user_request.get("travel_pace") or "适中",
            special_requirements=user_request.get("special_requirements") or "无",
            attractions=attractions[:20],
            weather=weather[:10],
            hotels=hotels[:10],
        ) + "\n只返回合法JSON，不要Markdown代码块。"
        response = self.llm_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=4000,
        )
        content = (response.choices[0].message.content or "").strip()
        if "```" in content:
            content = content.replace("```json", "").replace("```", "").strip()
        import json
        plan = json.loads(content)
        # Qwen may wrap the requested object in a named top-level field.
        if isinstance(plan, dict) and isinstance(plan.get("trip_plan"), dict):
            plan = plan["trip_plan"]
        return plan
