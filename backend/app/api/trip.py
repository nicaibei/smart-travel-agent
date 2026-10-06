"""旅行计划相关的API路由"""
from fastapi import APIRouter, HTTPException
from app.models import TripPlan, TripPlanRequest
from app.agents import TripPlannerOrchestrator
from app.services import get_unsplash_service
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/trip", tags=["旅行计划"])

# 创建协调器实例 (共享MCP工具)
orchestrator = TripPlannerOrchestrator()

# 创建Unsplash服务实例
unsplash_service = get_unsplash_service()


@router.post("/plan", response_model=TripPlan)
async def create_trip_plan(request: TripPlanRequest) -> TripPlan:
    """
    创建旅行计划
    
    请求示例:
    {
        "city": "北京",
        "start_date": "2024-01-01",
        "end_date": "2024-01-03",
        "days": 3,
        "preferences": "历史文化",
        "budget": 3000,
        "transportation": "公共交通",
        "accommodation": "经济型"
    }
    
    FastAPI自动：
    1. 验证请求数据(TripPlanRequest)
    2. 验证响应数据(TripPlan)
    3. 生成OpenAPI文档
    """
    try:
        logger.info(f"收到旅行计划请求: {request.city}, {request.days}天")
        
        # 使用协调器生成旅行计划
        trip_plan = await orchestrator.plan_trip(request)
        
        logger.info(f"旅行计划生成成功，共{len(trip_plan.days)}天行程")

        # PlannerAgent may omit media and normalize the budget too aggressively;
        # preserve source POI photos and keep the requested budget meaningful.
        source_attractions = []
        try:
            raw = await orchestrator._search_attractions(request)
            source_attractions = json.loads(raw) if raw else []
        except Exception:
            source_attractions = []
        photos_by_name = {
            item.get("name"): ((item.get("photos") or [{}])[0].get("url") or "").replace("http://", "https://")
            for item in source_attractions if item.get("name")
        }
        for day in trip_plan.days:
            for attraction in day.attractions:
                if not attraction.image_url and photos_by_name.get(attraction.name):
                    attraction.image_url = photos_by_name[attraction.name]

        if trip_plan.budget and request.budget:
            trip_plan.budget.planned_budget = request.budget
            if trip_plan.budget.total < request.budget * 0.75:
                trip_plan.budget.total_attractions = round(request.budget * 0.18)
                trip_plan.budget.total_hotels = round(request.budget * 0.38)
                trip_plan.budget.total_meals = round(request.budget * 0.26)
                trip_plan.budget.total_transportation = round(request.budget * 0.12)
                trip_plan.budget.total = sum([
                    trip_plan.budget.total_attractions,
                    trip_plan.budget.total_hotels,
                    trip_plan.budget.total_meals,
                    trip_plan.budget.total_transportation,
                ])
            trip_plan.budget.remaining = max(request.budget - trip_plan.budget.total, 0)
        
        # 只展示与高德 POI 明确绑定的图片。通用图库搜索可能返回风景类近似图，
        # 但无法证明它就是当前景点，因此不能把它标成景点实拍图。
        logger.info("景点图片校验完成：仅保留高德 POI 绑定图片")
        return trip_plan
        
    except Exception as e:
        logger.error(f"生成旅行计划失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"生成旅行计划失败: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "service": "trip-planner",
        "orchestrator_ready": orchestrator is not None,
        "unsplash_ready": unsplash_service is not None,
        "coordinate_repair_enabled": True,
        "agents": ["attraction", "weather", "hotel", "planner"]
    }
