# 侧边导航完整指南

## 📦 功能概述

智能侧边导航包括：
- ✅ 多级菜单导航
- ✅ 平滑滚动锚点跳转
- ✅ 自动高亮当前区域
- ✅ 阅读进度指示
- ✅ 快捷操作按钮
- ✅ 响应式设计（PC + 移动端）

---

## 🎨 组件结构

### 1. 桌面端侧边栏 - `SidebarNavigation.vue`

```
┌─────────────────────┐
│  📋 行程概览        │
│  💰 预算明细        │
│  🌤️ 天气信息        │
│  📅 每日行程 ▼      │
│    - 第1天          │
│    - 第2天          │
│    - 第3天          │
│  📍 景点列表 ▼      │
│    - 故宫           │
│    - 长城           │
│  🏨 住宿信息        │
│  💡 旅行建议        │
├─────────────────────┤
│  [编辑行程]         │
│  [导出PDF]          │
│  [分享]             │
│  [回到顶部]         │
├─────────────────────┤
│  阅读进度 75%       │
│  ▓▓▓▓▓▓▓▓░░         │
└─────────────────────┘
```

### 2. 移动端浮动按钮 - `MobileNavigation.vue`

```
                  ┌──┐
                  │☰ │ ← 主按钮
                  ├──┤
                  │↑ │ ← 回到顶部
                  ├──┤
                  │≡ │ ← 打开目录
                  ├──┤
                  │✎ │ ← 编辑
                  ├──┤
                  │↓ │ ← 导出
                  └──┘
```

---

## 🔧 使用方法

### 1. 在结果页面中集成

```vue
<template>
  <div class="trip-plan-page">
    <div class="page-layout">
      <!-- 侧边导航（桌面端） -->
      <aside class="sidebar">
        <SidebarNavigation
          :trip-plan="tripPlan"
          @edit="handleEdit"
          @export="handleExport"
          @share="handleShare"
        />
      </aside>

      <!-- 主内容区域 -->
      <main class="main-content">
        <!-- 行程概览 -->
        <section id="overview">
          <h2>行程概览</h2>
          <!-- 内容 -->
        </section>

        <!-- 预算明细 -->
        <section id="budget">
          <h2>预算明细</h2>
          <!-- 内容 -->
        </section>

        <!-- 天气信息 -->
        <section id="weather">
          <h2>天气信息</h2>
          <!-- 内容 -->
        </section>

        <!-- 每日行程 -->
        <section
          v-for="(day, index) in tripPlan.days"
          :key="index"
          :id="`day-section-${index}`"
        >
          <h2>第 {{ index + 1 }} 天 - {{ day.date }}</h2>
          
          <!-- 景点列表 -->
          <div
            v-for="(attraction, attrIndex) in day.attractions"
            :key="attrIndex"
            :id="`day-${index}-attraction-${attrIndex}`"
          >
            <h3>{{ attraction.name }}</h3>
            <!-- 景点内容 -->
          </div>
        </section>

        <!-- 住宿信息 -->
        <section id="hotels">
          <h2>住宿信息</h2>
          <!-- 内容 -->
        </section>

        <!-- 旅行建议 -->
        <section id="suggestions">
          <h2>旅行建议</h2>
          <!-- 内容 -->
        </section>
      </main>
    </div>

    <!-- 移动端导航 -->
    <MobileNavigation
      :trip-plan="tripPlan"
      @edit="handleEdit"
      @export="handleExport"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import SidebarNavigation from '@/components/SidebarNavigation.vue';
import MobileNavigation from '@/components/MobileNavigation.vue';
import type { TripPlan } from '@/types';

const tripPlan = ref<TripPlan>({ /* ... */ });

const handleEdit = () => {
  console.log('编辑行程');
};

const handleExport = () => {
  console.log('导出PDF');
};

const handleShare = () => {
  console.log('分享');
};
</script>

<style scoped>
.page-layout {
  display: flex;
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}

.sidebar {
  width: 250px;
  flex-shrink: 0;
}

.main-content {
  flex: 1;
  min-width: 0;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .sidebar {
    display: none;
  }

  .page-layout {
    padding: 16px;
  }
}
</style>
```

---

## ✨ 核心功能

### 1. 平滑滚动

```typescript
const scrollToSection = (key: string) => {
  const element = document.getElementById(key);
  if (element) {
    element.scrollIntoView({
      behavior: 'smooth',  // 平滑滚动
      block: 'start',      // 对齐到顶部
    });
  }
};
```

**参数说明：**
- `behavior: 'smooth'` - 平滑滚动动画
- `behavior: 'auto'` - 瞬间跳转
- `block: 'start'` - 元素顶部对齐视口顶部
- `block: 'center'` - 元素居中
- `block: 'end'` - 元素底部对齐视口底部

### 2. 自动高亮当前区域

```typescript
const updateActiveSection = () => {
  const sections = ['overview', 'budget', 'weather', ...];
  const scrollTop = window.scrollY + 100; // 偏移量

  for (const sectionKey of sections) {
    const element = document.getElementById(sectionKey);
    if (element) {
      const rect = element.getBoundingClientRect();
      const elementTop = rect.top + window.scrollY;

      // 判断是否在可视区域
      if (scrollTop >= elementTop && 
          scrollTop < elementTop + element.offsetHeight) {
        selectedKeys.value = [sectionKey];
        break;
      }
    }
  }
};

// 监听滚动
window.addEventListener('scroll', updateActiveSection);
```

### 3. 阅读进度

```typescript
const updateScrollProgress = () => {
  const windowHeight = window.innerHeight;
  const documentHeight = document.documentElement.scrollHeight;
  const scrollTop = window.scrollY;

  const totalScroll = documentHeight - windowHeight;
  const progress = (scrollTop / totalScroll) * 100;

  scrollProgress.value = Math.min(Math.max(progress, 0), 100);
};
```

### 4. 高亮动画

```typescript
const highlightElement = (element: HTMLElement) => {
  element.classList.add('highlighted');
  setTimeout(() => {
    element.classList.remove('highlighted');
  }, 2000);
};
```

```css
.highlighted {
  animation: highlight 2s ease-in-out;
}

@keyframes highlight {
  0%, 100% { background-color: transparent; }
  50% { background-color: rgba(24, 144, 255, 0.1); }
}
```

---

## 📱 响应式设计

### 桌面端（>768px）
- 固定侧边栏（Affix组件）
- 完整菜单展示
- 快捷操作按钮

### 移动端（≤768px）
- 浮动按钮组
- 侧滑抽屉菜单
- 精简操作选项

```css
/* 桌面端显示侧边栏 */
@media (min-width: 769px) {
  .sidebar-navigation {
    display: block;
  }
  .mobile-navigation {
    display: none;
  }
}

/* 移动端显示浮动按钮 */
@media (max-width: 768px) {
  .sidebar-navigation {
    display: none;
  }
  .mobile-navigation {
    display: block;
  }
}
```

---

## 🎯 高级特性

### 1. 多级菜单

```vue
<a-sub-menu key="days" title="每日行程">
  <template #icon><CalendarOutlined /></template>
  <a-menu-item
    v-for="(day, index) in tripPlan.days"
    :key="`day-${index}`"
  >
    第 {{ index + 1 }} 天
    <span class="day-date">{{ day.date }}</span>
  </a-menu-item>
</a-sub-menu>
```

### 2. 景点列表展开

```vue
<a-sub-menu key="attractions" title="景点列表">
  <template #icon><PushpinOutlined /></template>
  <a-menu-item
    v-for="(attraction, index) in allAttractions"
    :key="`attraction-${index}`"
  >
    {{ attraction.name }}
  </a-menu-item>
</a-sub-menu>
```

### 3. 固定定位（Affix）

```vue
<a-affix :offset-top="80">
  <div class="sidebar-menu">
    <!-- 菜单内容 -->
  </div>
</a-affix>
```

**参数：**
- `offset-top` - 距离顶部的偏移量
- `offset-bottom` - 距离底部的偏移量
- `target` - 监听滚动的容器

### 4. 浮动按钮组（移动端）

```vue
<a-float-button-group
  trigger="click"
  type="primary"
  :style="{ right: '24px', bottom: '24px' }"
>
  <template #icon>
    <MenuOutlined />
  </template>

  <a-float-button @click="scrollToTop">
    <template #icon><VerticalAlignTopOutlined /></template>
  </a-float-button>
  
  <!-- 更多按钮 -->
</a-float-button-group>
```

---

## 💡 使用技巧

### 1. 添加新的导航项

```typescript
// 1. 在页面中添加锚点
<section id="new-section">
  <h2>新内容</h2>
</section>

// 2. 在侧边栏菜单中添加菜单项
<a-menu-item key="new-section">
  <template #icon><StarOutlined /></template>
  新内容
</a-menu-item>

// 3. 在 updateActiveSection 中添加区域检测
const sections = ['overview', 'budget', 'new-section', ...];
```

### 2. 自定义滚动偏移

```typescript
const scrollToSection = (key: string) => {
  const element = document.getElementById(key);
  if (element) {
    const offsetTop = element.offsetTop - 100; // 减去100px
    window.scrollTo({
      top: offsetTop,
      behavior: 'smooth',
    });
  }
};
```

### 3. 添加滚动动画

```css
/* 平滑滚动（全局） */
html {
  scroll-behavior: smooth;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-thumb {
  background: #1890ff;
  border-radius: 4px;
}

::-webkit-scrollbar-track {
  background: #f0f0f0;
}
```

### 4. 节流优化

```typescript
import { throttle } from 'lodash-es';

// 使用节流优化滚动事件
const throttledUpdate = throttle(updateScrollProgress, 100);

onMounted(() => {
  window.addEventListener('scroll', throttledUpdate);
});
```

---

## 🐛 常见问题

### 1. 滚动不平滑

**问题：** 点击菜单跳转不够平滑

**解决：**
```typescript
// 方案1：添加全局CSS
html {
  scroll-behavior: smooth;
}

// 方案2：使用JS实现
element.scrollIntoView({ behavior: 'smooth' });

// 方案3：使用动画库
import { gsap } from 'gsap';
gsap.to(window, { duration: 1, scrollTo: element });
```

### 2. 锚点偏移问题

**问题：** 跳转后内容被头部遮挡

**解决：**
```typescript
// 方案1：调整scrollIntoView
element.scrollIntoView({ 
  behavior: 'smooth',
  block: 'start' 
});
window.scrollBy(0, -100); // 向上偏移100px

// 方案2：使用CSS
section {
  scroll-margin-top: 100px;
}
```

### 3. 自动高亮不准确

**问题：** 滚动时菜单高亮不正确

**解决：**
```typescript
// 调整偏移量和判断逻辑
const scrollTop = window.scrollY + 150; // 增加偏移

// 添加容差范围
const tolerance = 50;
if (scrollTop >= elementTop - tolerance && 
    scrollTop < elementTop + element.offsetHeight + tolerance) {
  // 高亮菜单项
}
```

### 4. 移动端抽屉卡顿

**问题：** 移动端抽屉打开/关闭不流畅

**解决：**
```vue
<!-- 使用Drawer的afterVisibleChange -->
<a-drawer
  v-model:visible="drawerVisible"
  @after-visible-change="handleAfterVisible"
>
  <!-- 内容 -->
</a-drawer>

<script>
const handleAfterVisible = (visible: boolean) => {
  if (visible) {
    // 抽屉完全打开后执行
  }
};
</script>
```

---

## 📊 性能优化

### 1. 滚动监听优化

```typescript
// 使用 Intersection Observer API
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const key = entry.target.id;
        selectedKeys.value = [key];
      }
    });
  },
  { threshold: 0.5 }
);

// 观察所有section
sections.forEach((section) => {
  const element = document.getElementById(section);
  if (element) observer.observe(element);
});
```

### 2. 防抖与节流

```typescript
import { debounce, throttle } from 'lodash-es';

// 防抖：用户停止滚动后执行
const debouncedUpdate = debounce(updateActiveSection, 300);

// 节流：每100ms最多执行一次
const throttledUpdate = throttle(updateScrollProgress, 100);
```

### 3. 虚拟滚动

```typescript
// 对于超长列表，使用虚拟滚动
import { VirtualList } from 'vue-virtual-scroller';

<VirtualList
  :items="allAttractions"
  :item-height="50"
>
  <template #default="{ item }">
    <a-menu-item :key="item.id">
      {{ item.name }}
    </a-menu-item>
  </template>
</VirtualList>
```

---

## 🎓 技术要点总结

### 1. scrollIntoView API

```typescript
element.scrollIntoView({
  behavior: 'smooth',  // 'auto' | 'smooth'
  block: 'start',      // 'start' | 'center' | 'end' | 'nearest'
  inline: 'nearest'    // 'start' | 'center' | 'end' | 'nearest'
});
```

### 2. 滚动位置计算

```typescript
// 文档总高度
const documentHeight = document.documentElement.scrollHeight;

// 视口高度
const windowHeight = window.innerHeight;

// 当前滚动位置
const scrollTop = window.scrollY;

// 可滚动距离
const scrollable = documentHeight - windowHeight;

// 滚动进度
const progress = (scrollTop / scrollable) * 100;
```

### 3. 元素位置计算

```typescript
const element = document.getElementById('section');

// getBoundingClientRect: 相对视口
const rect = element.getBoundingClientRect();
const viewportTop = rect.top; // 相对视口顶部

// offsetTop: 相对文档
const documentTop = element.offsetTop; // 相对文档顶部

// 判断是否在视口内
const isInView = viewportTop >= 0 && 
                 viewportTop <= window.innerHeight;
```

---

**🎉 侧边导航功能完成！用户现在可以轻松浏览长页面内容了！**
