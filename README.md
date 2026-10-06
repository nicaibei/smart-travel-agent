# 智能旅行助手 - 实战项目

基于多 Agent 协作的智能旅行规划助手，使用阿里云通义千问大模型和高德地图API。

## 🎯 项目特点

- ✅ **多 Agent 协作架构**：景点搜索、天气查询、酒店推荐、行程规划
- ✅ **MCP 工具集成**：使用 Model Context Protocol 调用高德地图API
- ✅ **共享工具实例**：多个Agent共享同一个MCP工具，提高性能
- ✅ **类型安全**：前后端使用 Pydantic 和 TypeScript 保证类型一致
- ✅ **阿里云通义千问**：使用国内高性能大模型

## 📁 项目结构

```
实战项目1_智能旅行助手/
├── .env                          # 环境变量配置
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI应用入口
│   │   ├── config.py            # 配置管理
│   │   ├── agents/              # AI智能体层
│   │   │   ├── orchestrator.py # 协调器(核心)
│   │   │   ├── attraction_agent.py
│   │   │   ├── weather_agent.py
│   │   │   ├── hotel_agent.py
│   │   │   └── planner_agent.py
│   │   ├── api/                 # API路由层
│   │   │   └── trip.py
│   │   ├── models/              # 数据模型层
│   │   │   └── location.py
│   │   └── services/            # 服务层
│   │       ├── mcp_tools.py
│   │       └── llm_client.py
│   ├── requirements.txt         # Python依赖
│   ├── run.py                   # 启动脚本
│   └── test_planner.py          # 测试脚本
│
└── frontend/
    ├── src/
    │   ├── types/               # TypeScript类型
    │   ├── services/            # API服务
    │   ├── views/               # 页面组件
    │   └── router/              # 路由配置
    └── package.json
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑 `.env` 文件，确保包含以下配置：

```env
# 高德地图配置
AMAP_WEB_KEY=你的高德Web服务Key
AMAP_JS_KEY=你的高德JS_Key
AMAP_SECURITY_CODE=你的安全密钥

# Unsplash图片API配置
UNSPLASH_ACCESS_KEY=你的Unsplash_Access_Key
UNSPLASH_SECRET_KEY=你的Unsplash_Secret_Key

# LLM配置 (阿里云通义千问)
LLM_API_KEY=你的通义千问API_Key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_ID=qwen-turbo
LLM_TIMEOUT=60

# 服务配置
PORT=8000
HOST=127.0.0.1
```

### 3. 启动服务

```bash
# 方式1: 使用启动脚本
python run.py

# 方式2: 使用uvicorn命令
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 测试API

```bash
# 测试健康检查
curl http://localhost:8000/api/trip/health

# 运行测试脚本
python test_planner.py

# 访问API文档
浏览器打开: http://localhost:8000/docs
```

## 📖 API 使用示例

### 创建旅行计划

**请求：**
```bash
POST /api/trip/plan
Content-Type: application/json

{
  "city": "北京",
  "start_date": "2024-06-01",
  "end_date": "2024-06-03",
  "days": 3,
  "preferences": "历史文化",
  "budget": 3000,
  "transportation": "公共交通",
  "accommodation": "经济型"
}
```

**响应：**
```json
{
  "city": "北京",
  "start_date": "2024-06-01",
  "end_date": "2024-06-03",
  "days": [...],
  "weather_info": [...],
  "overall_suggestions": "...",
  "budget": {...}
}
```

## 🤖 多 Agent 架构

### Agent 分工

1. **AttractionAgent (景点搜索专家)**
   - 根据用户偏好搜索景点
   - 使用高德地图POI搜索

2. **WeatherAgent (天气查询专家)**
   - 查询目的地天气预报
   - 提供穿衣建议

3. **HotelAgent (酒店推荐专家)**
   - 根据预算推荐酒店
   - 使用高德地图POI搜索

4. **PlannerAgent (行程规划专家)**
   - 整合所有信息
   - 生成详细的旅行计划

### 工作流程

```
用户请求
    ↓
TripPlannerOrchestrator (协调器)
    ├─→ AttractionAgent + MCP工具
    ├─→ WeatherAgent + MCP工具
    ├─→ HotelAgent + MCP工具
    ↓
PlannerAgent (整合)
    ↓
TripPlan (结构化输出)
```

## 🔧 技术栈

### 后端
- **FastAPI**: Web框架
- **Pydantic**: 数据验证
- **HelloAgents**: Agent框架
- **MCP**: Model Context Protocol
- **通义千问**: 阿里云大模型

### 工具
- **高德地图API**: POI搜索、天气查询
- **Unsplash API**: 图片服务

## 📝 开发说明

### 添加新的 Agent

1. 在 `app/agents/` 创建新的 Agent 文件
2. 定义 Agent 的提示词
3. 在 `orchestrator.py` 中注册 Agent
4. 如需工具支持，调用 `agent.add_tool(self.mcp_tool)`

### 添加新的 API 端点

1. 在 `app/api/` 创建或修改路由文件
2. 在 `app/main.py` 中注册路由
3. 使用 Pydantic 模型验证请求和响应

## 🐛 常见问题

### 1. MCP 工具无法启动
确保已安装 Node.js，并且网络可以访问 npm。

### 2. LLM 调用失败
检查 `.env` 中的 `LLM_API_KEY` 是否正确。

### 3. 高德地图 API 调用失败
检查 `.env` 中的 `AMAP_WEB_KEY` 是否正确。

## 📄 License

MIT

## 👥 贡献

欢迎提交 Issue 和 Pull Request！
