# 前端开发文档

## 📁 项目结构

```
frontend/
├── src/
│   ├── views/               # 页面组件
│   │   ├── TripPlanner.vue  # 旅行规划主页面
│   │   └── index.ts
│   ├── services/            # API服务
│   │   ├── api.ts           # API调用封装
│   │   └── index.ts
│   ├── types/               # TypeScript类型定义
│   │   ├── trip.ts          # 旅行计划相关类型
│   │   └── index.ts
│   ├── router/              # 路由配置
│   │   └── index.ts
│   ├── App.vue              # 根组件
│   ├── main.ts              # 应用入口
│   └── env.d.ts             # 类型声明
├── index.html               # HTML入口
├── package.json             # 依赖配置
├── vite.config.ts           # Vite配置
├── tsconfig.json            # TypeScript配置
└── .env                     # 环境变量
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

访问: http://localhost:3000

### 3. 构建生产版本

```bash
npm run build
```

## 📋 核心功能

### 1. 类型安全

所有数据类型都与后端 Pydantic 模型完全对应：

```typescript
// 请求类型
interface TripPlanRequest {
  city: string;
  start_date: string;
  end_date: string;
  days: number;
  preferences: string;
  budget: number;
  transportation: string;
  accommodation: string;
}

// 响应类型
interface TripPlan {
  city: string;
  start_date: string;
  end_date: string;
  days: DayPlan[];
  weather_info: WeatherInfo[];
  overall_suggestions: string;
  budget?: Budget;
}
```

### 2. API 服务

```typescript
import { TripPlannerAPI } from '@/services';

// 创建旅行计划
const response = await TripPlannerAPI.createTripPlan(request);

// 健康检查
const health = await TripPlannerAPI.healthCheck();
```

### 3. 页面组件

- **TripPlanner.vue**: 主页面，包含表单和结果展示
  - 表单输入
  - 加载状态
  - 错误处理
  - 结果展示（天气、景点、餐饮、住宿、预算）

## 🎨 界面展示

### 表单区域
- 目的地城市
- 开始/结束日期
- 旅行天数
- 旅行偏好
- 预算
- 交通方式
- 住宿类型

### 结果展示
- 📅 旅行概览
- 🌤️ 天气预报
- 📍 每日景点安排（含图片）
- 🍽️ 餐饮推荐
- 🏨 住宿信息
- 💰 预算汇总
- 💡 旅行建议

## 🔧 技术栈

- **Vue 3**: 渐进式框架
- **TypeScript**: 类型安全
- **Vue Router**: 路由管理
- **Vite**: 构建工具
- **Fetch API**: HTTP请求

## 📝 开发规范

### 1. 类型定义

所有组件使用 TypeScript，确保类型安全：

```typescript
import type { TripPlan, TripPlanRequest } from '@/types';

const form = ref<TripPlanRequest>({...});
const tripPlan = ref<TripPlan | null>(null);
```

### 2. API 调用

使用封装的 API 服务，统一错误处理：

```typescript
try {
  const response = await TripPlannerAPI.createTripPlan(request);
  if (response.error) {
    // 处理错误
  } else if (response.data) {
    // 处理数据
  }
} catch (error) {
  // 异常处理
}
```

### 3. 组件结构

```vue
<template>
  <!-- HTML模板 -->
</template>

<script setup lang="ts">
// TypeScript逻辑
import { ref } from 'vue';
import type { ... } from '@/types';
</script>

<style scoped>
/* 组件样式 */
</style>
```

## 🌐 代理配置

开发环境下，API请求会被代理到后端：

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

## 🎯 特性

- ✅ TypeScript 类型安全
- ✅ Vue 3 Composition API
- ✅ 响应式设计
- ✅ 加载状态显示
- ✅ 错误处理
- ✅ 图片展示
- ✅ 路由管理
- ✅ 代码分割

## 📦 打包部署

```bash
# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

构建产物在 `dist/` 目录。

## 🔍 环境变量

`.env` 文件配置：

```env
VITE_API_BASE_URL=http://localhost:8000
```

生产环境可以创建 `.env.production` 文件。

## 💡 后续优化

- [ ] 添加地图展示（高德地图集成）
- [ ] 实现行程编辑功能
- [ ] 添加历史记录
- [ ] 支持分享功能
- [ ] 优化移动端体验
- [ ] 添加动画效果
- [ ] 实现离线缓存
