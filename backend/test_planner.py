"""测试脚本 - 测试旅行计划API"""
import asyncio
import json
from app.models import TripPlanRequest
from app.agents import TripPlannerOrchestrator


async def test_trip_planner():
    """测试旅行规划器"""
    
    print("=" * 60)
    print("🧪 测试智能旅行助手")
    print("=" * 60)
    
    # 创建测试请求
    request = TripPlanRequest(
        city="北京",
        start_date="2024-06-01",
        end_date="2024-06-03",
        days=3,
        preferences="历史文化",
        budget=3000,
        transportation="公共交通",
        accommodation="经济型"
    )
    
    print("\n📝 测试请求:")
    print(json.dumps(request.dict(), ensure_ascii=False, indent=2))
    
    try:
        # 创建协调器
        print("\n🤖 初始化协调器...")
        orchestrator = TripPlannerOrchestrator()
        
        # 生成旅行计划
        print("\n⏳ 正在生成旅行计划...")
        trip_plan = await orchestrator.plan_trip(request)
        
        # 输出结果
        print("\n✅ 旅行计划生成成功!")
        print("=" * 60)
        print(json.dumps(trip_plan.dict(), ensure_ascii=False, indent=2))
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_trip_planner())
