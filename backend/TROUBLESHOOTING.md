# 快速修复指南

## 问题：No module named 'app.agents.orchestrator'

这个错误通常是因为：
1. 运行目录不正确
2. 缺少 `__init__.py` 文件
3. Python路径配置问题

---

## ✅ 解决步骤

### 步骤1：确认项目结构

确保你的项目结构如下：

```
backend/
├── app/
│   ├── __init__.py          ← 必须有
│   ├── main.py
│   ├── config.py
│   ├── agents/
│   │   ├── __init__.py      ← 必须有
│   │   └── orchestrator.py
│   ├── api/
│   │   ├── __init__.py      ← 必须有
│   │   └── trip.py
│   ├── models/
│   │   ├── __init__.py      ← 必须有
│   │   └── location.py
│   └── services/
│       ├── __init__.py      ← 必须有
│       ├── mcp_tools.py
│       ├── llm_client.py
│       ├── simple_agent.py
│       └── unsplash_service.py
├── run.py
└── requirements.txt
```

### 步骤2：创建缺失的 __init__.py 文件

在每个目录下创建空的 `__init__.py` 文件。

**使用命令行创建（Windows CMD）：**

```cmd
cd backend
type nul > app\__init__.py
type nul > app\agents\__init__.py
type nul > app\api\__init__.py
type nul > app\models\__init__.py
type nul > app\services\__init__.py
```

**或者手动创建：**
在每个目录（app, agents, api, models, services）下创建一个名为 `__init__.py` 的空文件。

### 步骤3：从正确的目录运行

**一定要在 backend 目录下运行：**

```cmd
cd backend
python run.py
```

**不要在项目根目录运行！**

### 步骤4：检查 run.py 文件

确保 `run.py` 内容正确：

```python
"""启动脚本"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

### 步骤5：使用 uvicorn 直接运行（替代方案）

如果上面方法不行，直接使用 uvicorn：

```cmd
cd backend
uvicorn app.main:app --reload --port 8000
```

---

## 🔍 详细排查步骤

### 1. 确认当前目录

```cmd
cd
```

应该显示类似：`D:\...\实战项目1_智能旅行助手\backend`

### 2. 检查文件是否存在

```cmd
dir app\agents\orchestrator.py
```

应该能看到文件信息。

### 3. 检查 Python 导入

```cmd
python -c "import sys; print('\n'.join(sys.path))"
```

当前目录应该在列表中。

### 4. 测试导入

```cmd
python -c "from app.agents import orchestrator; print('Success!')"
```

如果成功，说明模块可以导入。

---

## 🆘 如果还是不行

### 选项A：使用绝对路径

修改 `run.py`：

```python
import sys
import os

# 添加项目路径到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

### 选项B：设置 PYTHONPATH

**Windows CMD：**
```cmd
set PYTHONPATH=%CD%
python run.py
```

**PowerShell：**
```powershell
$env:PYTHONPATH=$PWD
python run.py
```

---

## 💡 推荐的运行方式

```cmd
# 1. 进入backend目录
cd backend

# 2. 确认 __init__.py 文件存在
dir app\__init__.py
dir app\agents\__init__.py

# 3. 使用 uvicorn 直接运行（最可靠）
uvicorn app.main:app --reload --port 8000
```

---

## ✅ 验证成功

如果看到以下输出，说明启动成功：

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

然后访问：http://localhost:8000/docs
