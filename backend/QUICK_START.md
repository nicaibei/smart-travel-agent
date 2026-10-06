# 🚀 快速启动指南

## ✅ 问题已修复

所有导入错误已解决：
- ✅ 创建了所有 `__init__.py` 文件
- ✅ 重写了 `orchestrator.py`（不依赖 hello-agents）
- ✅ 配置了模块导出
- ✅ 简化了 Agent 实现

---

## 🎯 现在可以启动了！

### 步骤1：确认位置

```cmd
# 确保在 backend 目录
cd d:\github_agentlearning\实战项目1_智能旅行助手\backend
```

### 步骤2：检查 .env 配置

确保根目录的 `.env` 文件已配置：

```env
# 高德地图API
AMAP_WEB_KEY=你的Key
AMAP_JS_KEY=你的Key
AMAP_SECURITY_CODE=你的密钥

# Unsplash API
UNSPLASH_ACCESS_KEY=你的Key
UNSPLASH_SECRET_KEY=你的Key

# 通义千问LLM
LLM_API_KEY=你的Key
```

### 步骤3：启动后端

```cmd
python run.py
```

### 步骤4：验证启动

看到以下输出表示成功：

```
✓ 旅行规划协调器初始化成功
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 步骤5：访问API文档

浏览器打开：http://localhost:8000/docs

---

## 📝 完整命令序列（复制粘贴）

```cmd
cd backend
python run.py
```

---

## 🎨 启动前端（新终端）

```cmd
cd frontend
npm install
npm run dev
```

访问：http://localhost:3000

---

## 🐛 如果还有错误

### 错误：模块导入失败

```cmd
# 检查Python路径
python -c "import sys; print(sys.path)"

# 测试导入
python -c "from app.agents import TripPlannerOrchestrator; print('OK')"
```

### 错误：API Key未配置

检查 `.env` 文件是否在项目根目录，且内容正确。

### 错误：端口被占用

```cmd
# 修改端口
python -c "import uvicorn; uvicorn.run('app.main:app', port=8001)"
```

---

## ✅ 成功标志

后端启动成功后，访问这些URL应该有响应：

- http://localhost:8000/ - 返回状态信息
- http://localhost:8000/health - 健康检查
- http://localhost:8000/docs - API文档

---

## 🎉 祝你好运！

现在运行 `python run.py` 启动后端吧！
