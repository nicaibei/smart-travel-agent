# 🚀 项目运行完整指南

## 📋 准备工作

### 1. 环境要求

**后端环境：**
- Python 3.8+
- pip 包管理器

**前端环境：**
- Node.js 16+
- npm 或 yarn

---

## 🔑 步骤1：配置API密钥

### 1.1 编辑 `.env` 文件

在项目根目录找到 `.env` 文件，填入你的API密钥：

```env
# 高德地图配置（必需）
AMAP_WEB_KEY=你的高德Web服务Key
AMAP_JS_KEY=你的高德JS_Key
AMAP_SECURITY_CODE=你的安全密钥

# Unsplash图片API配置（必需）
UNSPLASH_ACCESS_KEY=你的Unsplash_Access_Key
UNSPLASH_SECRET_KEY=你的Unsplash_Secret_Key

# LLM配置 - 阿里云通义千问（必需）
LLM_API_KEY=你的通义千问API_Key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_ID=qwen-turbo
LLM_TIMEOUT=60

# 服务配置
PORT=8000
HOST=127.0.0.1
```

### 1.2 如何获取API密钥

#### 高德地图API
1. 访问：https://console.amap.com/
2. 注册/登录账号
3. 进入"应用管理" → "我的应用"
4. 创建新应用，获取：
   - Web服务Key（AMAP_WEB_KEY）
   - JS Key（AMAP_JS_KEY）
   - 安全密钥（AMAP_SECURITY_CODE）

#### Unsplash API
1. 访问：https://unsplash.com/developers
2. 注册/登录账号
3. 创建新应用
4. 获取：
   - Access Key
   - Secret Key

#### 通义千问API
1. 访问：https://dashscope.aliyuncs.com/
2. 注册/登录阿里云账号
3. 开通DashScope服务
4. 获取API Key

---

## 🔧 步骤2：启动后端服务

### 2.1 进入后端目录

```bash
cd backend
```

### 2.2 安装依赖

```bash
pip install -r requirements.txt
```

如果速度慢，可以使用国内镜像：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2.3 启动后端服务

**方式1：使用run.py（推荐）**
```bash
python run.py
```

**方式2：使用uvicorn**
```bash
uvicorn app.main:app --reload --port 8000
```

### 2.4 验证后端启动

看到以下输出表示启动成功：

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 2.5 访问后端API文档

浏览器打开：http://localhost:8000/docs

你会看到完整的API文档（Swagger UI）

### 2.6 测试后端API

**方式1：使用测试脚本**
```bash
python test_planner.py
```

**方式2：使用curl**
```bash
curl http://localhost:8000/api/trip/health
```

预期返回：
```json
{
  "status": "ok",
  "service": "trip-planner",
  "orchestrator_ready": true,
  "unsplash_ready": true,
  "agents": ["attraction", "weather", "hotel", "planner"]
}
```

---

## 🎨 步骤3：启动前端服务

### 3.1 打开新的终端窗口

保持后端服务运行，打开新终端

### 3.2 进入前端目录

```bash
cd frontend
```

### 3.3 安装依赖

```bash
npm install
```

如果速度慢，可以使用淘宝镜像：

```bash
npm install --registry=https://registry.npmmirror.com
```

或者使用yarn：

```bash
yarn install
```

### 3.4 启动前端服务

```bash
npm run dev
```

或使用yarn：

```bash
yarn dev
```

### 3.5 验证前端启动

看到以下输出表示启动成功：

```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

### 3.6 访问前端页面

浏览器打开：http://localhost:3000

你会看到智能旅行助手的首页

---

## ✅ 步骤4：测试完整功能

### 4.1 生成旅行计划

1. 在首页填写表单：
   - 目的地城市：`北京`
   - 开始日期：`2024-06-01`
   - 结束日期：`2024-06-03`
   - 旅行天数：`3`
   - 旅行偏好：`历史文化`
   - 预算：`3000`
   - 交通方式：`公共交通`
   - 住宿类型：`经济型`

2. 点击"开始规划"按钮

3. 观察加载进度：
   - 🔍 正在搜索景点信息...
   - 🌤️ 正在查询天气数据...
   - 🏨 正在推荐酒店住宿...
   - 📋 正在生成详细行程...
   - 🎨 正在获取景点图片...
   - ✅ 计划生成完成！

4. 查看生成的旅行计划

### 4.2 测试其他功能

**编辑功能：**
1. 点击"编辑行程"按钮
2. 尝试上移/下移景点
3. 删除某个景点
4. 点击"保存修改"

**导出功能：**
1. 点击"导出"按钮
2. 选择导出格式（PNG或PDF）
3. 查看下载的文件

**侧边导航：**
1. 使用左侧导航菜单跳转到不同部分
2. 观察平滑滚动效果
3. 查看阅读进度

**移动端（可选）：**
1. 按F12打开开发者工具
2. 切换到移动设备模式
3. 测试浮动按钮和抽屉菜单

---

## 🐛 常见问题排查

### 问题1：后端启动失败

**错误：ModuleNotFoundError**
```
ModuleNotFoundError: No module named 'xxx'
```

**解决：**
```bash
pip install -r requirements.txt --upgrade
```

---

**错误：API Key未配置**
```
Error: AMAP_WEB_KEY not found in environment
```

**解决：**
检查 `.env` 文件是否存在且配置正确

---

**错误：端口被占用**
```
Error: Address already in use
```

**解决：**
修改端口或关闭占用端口的程序
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <进程ID> /F

# Mac/Linux
lsof -i :8000
kill -9 <进程ID>
```

---

### 问题2：前端启动失败

**错误：依赖安装失败**

**解决：**
```bash
# 清除缓存
rm -rf node_modules package-lock.json

# 重新安装
npm install
```

---

**错误：端口被占用**

**解决：**
修改端口（在 `vite.config.ts` 中）
```typescript
export default defineConfig({
  server: {
    port: 3001, // 改为3001
  },
});
```

---

### 问题3：API调用失败

**错误：Network Error**

**检查：**
1. 后端是否正常运行（http://localhost:8000/docs）
2. 前端代理配置是否正确（vite.config.ts）
3. 防火墙是否阻止

---

**错误：API返回错误**

**检查：**
1. API密钥是否正确配置
2. 查看后端日志输出
3. 查看浏览器控制台错误

---

### 问题4：图片无法显示

**原因：Unsplash API限制或跨域问题**

**解决：**
1. 检查Unsplash API密钥
2. 检查网络连接
3. 查看浏览器控制台错误

---

## 📊 性能优化建议

### 开发环境

```bash
# 后端 - 使用热重载
uvicorn app.main:app --reload

# 前端 - Vite自动热更新
npm run dev
```

### 生产环境

**后端：**
```bash
# 使用gunicorn（推荐）
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# 或使用uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**前端：**
```bash
# 构建生产版本
npm run build

# 预览生产版本
npm run preview

# 部署dist目录到服务器
```

---

## 🔍 调试技巧

### 后端调试

**查看日志：**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**使用断点：**
```python
import pdb; pdb.set_trace()
```

**使用VS Code调试：**
创建 `.vscode/launch.json`：
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload"
      ]
    }
  ]
}
```

### 前端调试

**浏览器开发者工具：**
- F12 打开
- Console查看日志
- Network查看API请求
- Vue Devtools查看组件状态

**VS Code调试：**
安装 Debugger for Chrome 插件

---

## 📱 移动端测试

### 本地测试

1. 启动服务
2. 按F12打开开发者工具
3. 点击设备工具栏图标
4. 选择移动设备（iPhone、iPad等）
5. 测试响应式布局和移动端功能

### 真机测试

1. 确保手机和电脑在同一局域网
2. 修改前端 `.env` 文件：
   ```env
   VITE_API_BASE_URL=http://你的电脑IP:8000
   ```
3. 启动前端服务时使用 `--host` 参数：
   ```bash
   npm run dev -- --host
   ```
4. 在手机浏览器访问：`http://你的电脑IP:3000`

---

## 🎓 学习建议

### 第一次运行

1. ✅ 先运行后端，确保API正常
2. ✅ 再运行前端，测试完整流程
3. ✅ 查看API文档了解接口
4. ✅ 阅读代码注释理解逻辑

### 深入学习

1. 📖 阅读各个功能的文档
2. 🔧 尝试修改和扩展功能
3. 🐛 解决遇到的问题
4. 💡 提出改进建议

---

## 📞 获取帮助

### 日志位置

- **后端日志**：终端输出
- **前端日志**：浏览器Console
- **API日志**：http://localhost:8000/docs

### 检查清单

- [ ] Python版本 >= 3.8
- [ ] Node.js版本 >= 16
- [ ] .env文件已配置
- [ ] API密钥有效
- [ ] 端口未被占用（8000、3000）
- [ ] 网络连接正常
- [ ] 依赖安装完整

---

**🎉 祝你运行顺利！如果遇到问题，请按照上面的排查步骤逐一检查。**
