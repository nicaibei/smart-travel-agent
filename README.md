# 智能旅行助手

基于四个 Agent 协作的智能旅行规划助手，使用 FastAPI、Vue、通义千问和高德地图服务生成包含景点、天气、酒店、餐饮和预算的旅行计划。

## 项目结构

```text
智能旅行助手/
├── .env.example                  # 配置模板，真实 .env 不提交
├── .gitignore
├── README.md
├── 智能旅行助手.md               # Agent 学习与项目笔记
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI 入口
│   │   ├── config.py             # 配置管理
│   │   ├── agents/               # 四个 Agent 与协调器
│   │   ├── api/trip.py           # 旅行规划接口
│   │   ├── models/location.py    # Pydantic 数据模型
│   │   └── services/             # 高德、LLM、图片服务
│   ├── requirements.txt
│   ├── AGENT_PROMPTS.py
│   └── run.py
└── frontend/
    ├── src/                      # 页面、组件、类型、API 和工具
    ├── package.json
    └── vite.config.ts
```

## 快速开始

复制 `.env.example` 为 `.env`，填写高德、通义千问和图片服务的密钥。真实 `.env` 只保存在本地，不要上传到 GitHub。

```powershell
cd backend
.venv\Scripts\python.exe -m pip install -r requirements.txt

cd ..\frontend
npm install
```

启动后端：

```powershell
cd backend
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

另开终端启动前端：

```powershell
cd frontend
npm run dev -- --host 0.0.0.0 --port 3001
```

访问：

- 前端：http://localhost:3001/
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/trip/health

## Agent 协作

```text
用户需求 → TripPlannerOrchestrator
              ├── AttractionAgent：搜索高德景点
              ├── WeatherAgent：查询天气
              ├── HotelAgent：推荐酒店
              └── PlannerAgent：整合每日行程
                         ↓
                    TripPlan 响应
```

后端使用 Pydantic 校验请求和响应。外部服务不可用时，协调器会切换到本地演示数据；模型生成的坐标也会在返回前进行校验和修正。

## API 示例

```http
POST /api/trip/plan
Content-Type: application/json
```

```json
{
  "city": "北京",
  "start_date": "2026-10-06",
  "end_date": "2026-10-08",
  "days": 3,
  "preferences": "历史文化",
  "budget": 3000,
  "transportation": "公共交通",
  "accommodation": "经济型"
}
```

## 安全说明

- `.env`、API Key 和本地日志不会提交。
- `.env.example` 只包含占位值。
- 不要在 README、截图或提交信息中粘贴真实密钥。

## 学习文档

Agent 的 Prompt 设计、工具调用、四 Agent 编排、结构化输出、降级策略、测试和可观测性见 [智能旅行助手.md](智能旅行助手.md)。
