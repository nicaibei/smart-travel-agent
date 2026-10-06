"""旅行规划多Agent协调器 - 使用HelloAgents框架"""
import json
from typing import Dict, Any
from openai import OpenAI
from app.models import TripPlan, TripPlanRequest, Attraction, Meal
from app.config import get_settings
from app.services.mcp_tools import get_mcp_tools
from app.agents.attraction_agent import AttractionAgent
from app.agents.weather_agent import WeatherAgent
from app.agents.hotel_agent import HotelAgent
from app.agents.planner_agent import PlannerAgent


class TripPlannerOrchestrator:
    """旅行规划协调器"""
    
    def __init__(self):
        """初始化协调器"""
        self.settings = get_settings()
        self.client = OpenAI(
            api_key=self.settings.llm_api_key,
            base_url=self.settings.llm_base_url,
            timeout=self.settings.llm_timeout
        )
        self.model = self.settings.llm_model_id
        
        # 初始化MCP工具
        self.mcp_tools = get_mcp_tools()
        self.attraction_agent = AttractionAgent(self.client, self.mcp_tools)
        self.weather_agent = WeatherAgent(self.client, self.mcp_tools)
        self.hotel_agent = HotelAgent(self.client, self.mcp_tools)
        self.planner_agent = PlannerAgent(self.client, self.model)
        
        print("✓ 旅行规划协调器初始化成功")
    
    async def plan_trip(self, request: TripPlanRequest) -> TripPlan:
        """
        生成旅行计划
        
        Args:
            request: 旅行计划请求
            
        Returns:
            TripPlan: 完整的旅行计划
        """
        print(f"\n开始为 {request.city} 规划 {request.days} 天的旅行...")
        
        # 1. 搜索景点
        print("🔍 步骤1: 搜索景点...")
        attractions_data = await self._search_attractions(request)
        
        # 2. 查询天气
        print("🌤️ 步骤2: 查询天气...")
        weather_data = await self._query_weather(request)
        
        # 3. 推荐酒店
        print("🏨 步骤3: 推荐酒店...")
        hotels_data = await self._recommend_hotels(request)
        
        # 4. 生成行程计划
        print("📋 步骤4: 生成详细行程...")
        trip_plan = await self._generate_plan(
            request, attractions_data, weather_data, hotels_data
        )
        
        print(f"✅ 旅行计划生成完成！")
        return trip_plan
    
    async def _search_attractions(self, request: TripPlanRequest) -> str:
        """搜索景点"""
        keywords = self._get_keywords_by_preference(request.preferences)
        
        try:
            result = await self.attraction_agent.search_attractions(request.city, request.preferences)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ 景点搜索失败: {e}")
            return "[]"
    
    async def _query_weather(self, request: TripPlanRequest) -> str:
        """查询天气"""
        try:
            result = await self.weather_agent.query_weather(
                request.city, request.start_date, request.end_date
            )
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ 天气查询失败: {e}")
            return "{}"
    
    async def _recommend_hotels(self, request: TripPlanRequest) -> str:
        """推荐酒店"""
        hotel_type = f"{request.accommodation}酒店"
        
        try:
            result = await self.hotel_agent.search_hotels(
                request.city, request.accommodation, request.budget
            )
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ 酒店推荐失败: {e}")
            return "[]"
    
    async def _generate_plan(
        self, 
        request: TripPlanRequest,
        attractions_data: str,
        weather_data: str,
        hotels_data: str
    ) -> TripPlan:
        """使用LLM生成详细行程"""

        # Let the planner model integrate the live search results.
        try:
            weather_items = json.loads(weather_data) if weather_data else []
            if isinstance(weather_items, dict):
                weather_items = weather_items.get("casts", [])
            plan_data = await self.planner_agent.generate_plan(
                request.model_dump(),
                json.loads(attractions_data),
                self._normalize_weather(weather_items, request),
                json.loads(hotels_data),
            )
            plan_data = self._repair_plan_locations(plan_data, json.loads(attractions_data))
            plan = TripPlan(**plan_data)
            return self._enrich_plan(plan, request, json.loads(attractions_data), json.loads(hotels_data))
        except Exception as e:
            print(f"⚠️ 旅行规划模型不可用，保留已获取的外部数据: {e}")
            return self._create_default_plan(
                request,
                attractions=json.loads(attractions_data) if attractions_data else [],
                weather=json.loads(weather_data) if weather_data else [],
                hotels=json.loads(hotels_data) if hotels_data else [],
            )

    @staticmethod
    def _poi_coordinates(poi: dict) -> dict | None:
        """Parse and validate AMap coordinates, whose location is usually 'lng,lat'."""
        raw_location = poi.get("location")
        try:
            if isinstance(raw_location, dict):
                longitude = float(raw_location["longitude"])
                latitude = float(raw_location["latitude"])
            else:
                longitude_raw, latitude_raw = str(raw_location or "").split(",", 1)
                longitude = float(longitude_raw)
                latitude = float(latitude_raw)
        except (KeyError, TypeError, ValueError):
            return None

        if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
            return None
        return {"longitude": longitude, "latitude": latitude}

    @classmethod
    def _repair_plan_locations(cls, plan_data: dict, source_attractions: list) -> dict:
        """Use matched AMap POI coordinates instead of model-generated coordinates."""
        coordinates_by_name = {}
        for poi in source_attractions:
            if not isinstance(poi, dict) or not poi.get("name"):
                continue
            coordinates = cls._poi_coordinates(poi)
            if coordinates:
                coordinates_by_name[poi["name"].strip().casefold()] = coordinates

        for day in plan_data.get("days", []) if isinstance(plan_data, dict) else []:
            if not isinstance(day, dict) or not isinstance(day.get("attractions"), list):
                continue
            repaired = []
            for attraction in day["attractions"]:
                if not isinstance(attraction, dict):
                    continue
                name = str(attraction.get("name", "")).strip().casefold()
                coordinates = coordinates_by_name.get(name)
                if coordinates:
                    attraction["location"] = coordinates
                else:
                    location = attraction.get("location")
                    try:
                        longitude = float(location["longitude"])
                        latitude = float(location["latitude"])
                        if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
                            raise ValueError("coordinates out of range")
                        attraction["location"] = {"longitude": longitude, "latitude": latitude}
                    except (KeyError, TypeError, ValueError):
                        continue
                repaired.append(attraction)
            day["attractions"] = repaired
        return plan_data

    def _enrich_plan(self, plan: TripPlan, request: TripPlanRequest, attractions: list, hotels: list) -> TripPlan:
        """Ensure the model output remains a useful, concrete day-by-day plan."""
        from datetime import datetime, timedelta

        source = []
        for poi in attractions:
            try:
                coords = str(poi.get("location", "")).split(",")
                if len(coords) != 2:
                    continue
                source.append({
                    "name": poi.get("name", "推荐景点"),
                    "address": poi.get("address") or poi.get("pname", request.city),
                    "location": {"longitude": float(coords[0]), "latitude": float(coords[1])},
                    "visit_duration": 90,
                    "description": f"{poi.get('type', '当地景点')}，建议结合周边街区步行游览。",
                    "category": poi.get("type", "景点"),
                    "rating": 4.5,
                    "image_url": ((poi.get("photos") or [{}])[0].get("url") or "").replace("http://", "https://") or None,
                    "ticket_price": 0,
                })
            except (TypeError, ValueError, AttributeError):
                continue
        seen = set()
        source = [item for item in source if not (item["name"] in seen or seen.add(item["name"]))]
        if source:
            def name_of(item):
                return item.name if hasattr(item, "name") else item.get("name", "")
            for index, day in enumerate(plan.days):
                existing = {name_of(item) for item in day.attractions}
                source_by_name = {item["name"]: item for item in source}
                for item in day.attractions:
                    item_name = name_of(item)
                    source_item = source_by_name.get(item_name)
                    if source_item:
                        if isinstance(item, dict):
                            item.setdefault("image_url", source_item["image_url"])
                        elif not item.image_url:
                            item.image_url = source_item["image_url"]
                additions = [item for item in source if item["name"] not in existing]
                for item in additions[:max(0, 3 - len(day.attractions))]:
                    day.attractions.append(Attraction(**item))
                if day.attractions:
                    names = "、".join(name_of(item) for item in day.attractions)
                    day.description = f"第{index + 1}天：{names}。上午安排重点景点，午餐后游览周边，傍晚留出自由活动时间。"
                meal_types = {meal.type for meal in day.meals}
                meal_defaults = {
                    "breakfast": (f"{request.city}当地早餐", "早点出发，预留景点排队时间", 30),
                    "lunch": (f"{request.city}特色午餐", "选择景点附近本地餐馆", 80),
                    "dinner": (f"{request.city}晚餐推荐", "晚间慢慢用餐并整理第二天行程", 100),
                }
                for meal_type, (name, description, cost) in meal_defaults.items():
                    if meal_type not in meal_types:
                        day.meals.append(Meal(type=meal_type, name=name, address=f"{request.city}市中心", description=description, estimated_cost=cost))
        if request.budget and plan.budget:
            plan.budget.planned_budget = request.budget
            if plan.budget.total < request.budget * 0.75:
                plan.budget.total_attractions = round(request.budget * 0.18)
                plan.budget.total_hotels = round(request.budget * 0.38)
                plan.budget.total_meals = round(request.budget * 0.26)
                plan.budget.total_transportation = round(request.budget * 0.12)
                plan.budget.total = sum((plan.budget.total_attractions, plan.budget.total_hotels, plan.budget.total_meals, plan.budget.total_transportation))
            plan.budget.remaining = max(request.budget - plan.budget.total, 0)
        return plan
    
    def _create_default_plan(self, request: TripPlanRequest, attractions=None, weather=None, hotels=None) -> TripPlan:
        """创建兜底计划，并尽量保留已成功获取的外部数据。"""
        from datetime import datetime, timedelta

        attractions = attractions or []
        weather = weather or []
        hotels = hotels or []
        has_external_data = bool(attractions or weather or hotels)

        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")

        city_data = {
            "北京": {
                "center": (116.397, 39.916),
                "attractions": [("故宫博物院", "北京市东城区景山前街4号", 116.3972, 39.9163, "历史文化"), ("天坛公园", "北京市东城区天坛东里甲1号", 116.4074, 39.8841, "历史文化"), ("颐和园", "北京市海淀区新建宫门路19号", 116.2755, 39.9999, "自然风光")],
                "hotel": "北京城市便捷酒店",
            },
            "上海": {
                "center": (121.4737, 31.2304),
                "attractions": [("外滩", "上海市黄浦区中山东一路", 121.4903, 31.2400, "城市风光"), ("豫园", "上海市黄浦区福佑路168号", 121.4920, 31.2272, "历史文化"), ("陆家嘴", "上海市浦东新区陆家嘴环路", 121.4998, 31.2389, "城市风光")],
                "hotel": "上海舒适型酒店",
            },
            "杭州": {
                "center": (120.1551, 30.2741),
                "attractions": [("西湖", "浙江省杭州市西湖区", 120.1480, 30.2420, "自然风光"), ("灵隐寺", "浙江省杭州市西湖区法云弄1号", 120.1014, 30.2408, "历史文化"), ("河坊街", "浙江省杭州市上城区河坊街", 120.1715, 30.2350, "美食探索")],
                "hotel": "杭州西湖舒适酒店",
            },
        }
        selected = city_data.get(request.city, {
            "center": (116.397, 39.916),
            "attractions": [(f"{request.city}城市公园", f"{request.city}市中心", 116.397, 39.916, "自然风光"), (f"{request.city}历史街区", f"{request.city}市中心历史街区", 116.407, 39.884, "历史文化"), (f"{request.city}特色美食街", f"{request.city}市中心美食街", 116.418, 39.900, "美食探索")],
            "hotel": f"{request.city}精选酒店",
        })
        # 高德 POI 字段转换为前端统一模型；字段不完整时跳过该条，避免破坏整个计划。
        external_attractions = []
        for poi in attractions[:12]:
            try:
                location = str(poi.get("location", "")).split(",")
                if len(location) != 2:
                    continue
                external_attractions.append({
                    "name": poi.get("name", "推荐景点"),
                    "address": poi.get("address") or poi.get("pname", request.city),
                    "location": {"longitude": float(location[0]), "latitude": float(location[1])},
                    "visit_duration": 120,
                    "description": poi.get("type", "当地热门景点"),
                    "category": poi.get("type", "景点"),
                    "rating": 4.5,
                    "image_url": ((poi.get("photos") or [{}])[0].get("url") or "").replace("http://", "https://") or None,
                    "ticket_price": 0,
                })
            except (TypeError, ValueError):
                continue

        external_hotels = []
        for poi in hotels[:10]:
            try:
                coordinates = str(poi.get("location", "")).split(",")
                location = (
                    {"longitude": float(coordinates[0]), "latitude": float(coordinates[1])}
                    if len(coordinates) == 2 else None
                )
                external_hotels.append({
                    "name": poi.get("name", "高德推荐酒店"),
                    "address": poi.get("address", ""),
                    "location": location,
                    "price_range": "请以酒店实际报价为准",
                    "rating": str(poi.get("biz_ext", {}).get("rating", "")),
                    "distance": str(poi.get("distance", "")),
                    "type": request.accommodation,
                    "estimated_cost": 0,
                })
            except (TypeError, ValueError, AttributeError):
                continue

        days = []
        source_weather = list(weather)
        for i in range(request.days):
            current_date = start_date + timedelta(days=i)
            day_attractions = []
            source_attractions = external_attractions or selected["attractions"]
            for offset, attraction in enumerate(source_attractions[i * 3:(i + 1) * 3] or source_attractions[:3]):
                if external_attractions:
                    day_attractions.append(attraction)
                    continue
                name, address, longitude, latitude, category = attraction
                day_attractions.append({
                    "name": name,
                    "address": address,
                    "location": {"longitude": longitude, "latitude": latitude},
                    "visit_duration": 120,
                    "description": f"{request.city}热门{category}目的地，适合安排半日游览。",
                    "category": category,
                    "rating": 4.7,
                    # 兜底数据没有景点级实拍图时保持为空，避免把通用风景图误标为具体景点。
                    "image_url": None,
                    "ticket_price": 40 + offset * 20,
                })
            days.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "day_index": i,
                "description": f"第{i+1}天：游览{day_attractions[0]['name']}等景点，留出充足时间慢慢体验。",
                "transportation": request.transportation,
                "accommodation": external_hotels[0]["name"] if external_hotels else selected["hotel"],
                "hotel": external_hotels[0] if external_hotels else {"name": selected["hotel"], "address": f"{request.city}市中心", "price_range": "¥300-500/晚", "rating": "4.5", "distance": "距景点约2公里", "type": request.accommodation, "estimated_cost": 380},
                "attractions": day_attractions,
                "meals": [
                    {"type": "breakfast", "name": f"{request.city}早餐铺", "address": f"{request.city}市中心", "description": "当地早餐，建议早点出发避开人流", "estimated_cost": 30},
                    {"type": "lunch", "name": f"{request.city}本地特色餐厅", "address": f"{request.city}市中心美食街", "description": "当地特色菜", "estimated_cost": 80},
                    {"type": "dinner", "name": "晚间精选餐厅", "address": f"{request.city}市中心", "description": "适合休息用餐", "estimated_cost": 100},
                ],
            })
            if not source_weather:
                source_weather.append({"date": current_date.strftime("%Y-%m-%d"), "day_weather": "晴", "night_weather": "晴", "day_temp": 24, "night_temp": 15, "wind_direction": "东南风", "wind_power": "3级"})

        if source_weather and isinstance(source_weather[0], dict) and "casts" in source_weather[0]:
            source_weather = source_weather[0]["casts"]
        normalized_weather = []
        for index, item in enumerate(source_weather[:request.days]):
            try:
                normalized_weather.append({
                    "date": item.get("date", (start_date + timedelta(days=index)).strftime("%Y-%m-%d")),
                    "day_weather": item.get("dayweather", item.get("day_weather", "晴")),
                    "night_weather": item.get("nightweather", item.get("night_weather", "晴")),
                    "day_temp": int(float(item.get("daytemp", item.get("daytemp_float", item.get("day_temp", 24))))),
                    "night_temp": int(float(item.get("nighttemp", item.get("nighttemp_float", item.get("night_temp", 15))))),
                    "wind_direction": item.get("daywind", item.get("wind_direction", "微风")),
                    "wind_power": item.get("daypower", item.get("wind_power", "2级")),
                })
            except (TypeError, ValueError):
                pass
        normalized_weather = normalized_weather or source_weather

        return TripPlan(
            city=request.city,
            start_date=request.start_date,
            end_date=request.end_date,
            days=days,
            weather_info=normalized_weather,
            overall_suggestions=(f"为您规划了{request.city}{request.days}天的旅行计划。" if has_external_data else f"为您规划了{request.city}{request.days}天的旅行计划。外部服务暂时不可用，当前显示本地演示数据。"),
            budget={
                "total_attractions": round(request.budget * 0.18) if request.budget else request.days * 100,
                "total_hotels": round(request.budget * 0.38) if request.budget else max(request.days - 1, 1) * 380,
                "total_meals": round(request.budget * 0.26) if request.budget else request.days * 180,
                "total_transportation": round(request.budget * 0.12) if request.budget else request.days * 50,
                "total": round(request.budget * 0.94) if request.budget else request.days * 510 + max(request.days - 1, 1) * 380,
                "planned_budget": request.budget,
                "remaining": round(request.budget * 0.06) if request.budget else 0,
            }
        )

    @staticmethod
    def _normalize_weather(weather, request):
        """Convert AMap forecast fields into the API response model."""
        from datetime import datetime, timedelta

        if isinstance(weather, dict):
            weather = weather.get("casts", [])
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        normalized = []
        for index, item in enumerate((weather or [])[:request.days]):
            try:
                normalized.append({
                    "date": item.get("date", (start_date + timedelta(days=index)).strftime("%Y-%m-%d")),
                    "day_weather": item.get("dayweather", item.get("day_weather", "晴")),
                    "night_weather": item.get("nightweather", item.get("night_weather", "晴")),
                    "day_temp": int(float(item.get("daytemp", item.get("daytemp_float", item.get("day_temp", 24))))),
                    "night_temp": int(float(item.get("nighttemp", item.get("nighttemp_float", item.get("night_temp", 15))))),
                    "wind_direction": item.get("daywind", item.get("wind_direction", "微风")),
                    "wind_power": item.get("daypower", item.get("wind_power", "2级")),
                })
            except (TypeError, ValueError, AttributeError):
                continue
        return normalized
    
    def _get_keywords_by_preference(self, preference: str) -> str:
        """根据偏好获取搜索关键词"""
        keywords_map = {
            "历史文化": "博物馆|古迹|历史景点",
            "自然风光": "公园|山|湖|风景区",
            "美食探索": "美食街|小吃街|特色餐厅",
            "购物娱乐": "商业街|购物中心|娱乐场所",
            "休闲度假": "度假村|温泉|休闲"
        }
        return keywords_map.get(preference, "景点")


# 导出
__all__ = ["TripPlannerOrchestrator"]
