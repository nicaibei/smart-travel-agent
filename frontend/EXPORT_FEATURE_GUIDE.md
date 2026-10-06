# 导出功能完整指南

## 📦 功能概述

支持将旅行计划导出为：
- ✅ PNG图片（高清）
- ✅ PDF文档（单页）
- ✅ 精美PDF（带封面、页眉页脚）

---

## 🔧 技术实现

### 核心依赖

```json
{
  "html2canvas": "^1.4.1",  // DOM转Canvas
  "jspdf": "^2.5.1"         // 生成PDF
}
```

### 工作原理

```
DOM元素 
  ↓ html2canvas
Canvas
  ↓ toDataURL
Base64图片
  ↓ jsPDF
PDF文件
```

---

## 📝 使用方法

### 1. 基础导出（图片）

```typescript
import { exportAsImage } from '@/utils/exportUtils';

const handleExportImage = () => {
  exportAsImage('trip-plan-content', tripPlan.value);
};
```

**参数说明：**
- `elementId`: 要导出的DOM元素ID
- `tripPlan`: 旅行计划数据（用于文件名）

### 2. 基础导出（PDF）

```typescript
import { exportAsPDF } from '@/utils/exportUtils';

const handleExportPDF = () => {
  exportAsPDF('trip-plan-content', tripPlan.value);
};
```

### 3. 精美PDF（推荐）

```typescript
import { exportAsFormattedPDF } from '@/utils/exportUtils';

const handleExportFormattedPDF = () => {
  exportAsFormattedPDF('trip-plan-content', tripPlan.value);
};
```

**特点：**
- ✅ 渐变色封面
- ✅ 城市名和日期
- ✅ 页眉页脚
- ✅ 页码

### 4. 通用导出函数

```typescript
import { exportTripPlan } from '@/utils/exportUtils';

// 导出为PNG
exportTripPlan(tripPlan.value, { format: 'png' });

// 导出为PDF
exportTripPlan(tripPlan.value, { format: 'pdf' });

// 导出为精美PDF
exportTripPlan(tripPlan.value, { format: 'formatted-pdf' });
```

---

## 🎨 在组件中集成

### 完整示例

```vue
<template>
  <div class="trip-plan-page">
    <!-- 导出按钮 -->
    <div class="export-buttons">
      <a-dropdown>
        <template #overlay>
          <a-menu @click="handleMenuClick">
            <a-menu-item key="image">
              <PictureOutlined />
              导出为图片
            </a-menu-item>
            <a-menu-item key="pdf">
              <FilePdfOutlined />
              导出为PDF
            </a-menu-item>
            <a-menu-item key="formatted-pdf">
              <FileTextOutlined />
              导出精美PDF
            </a-menu-item>
          </a-menu>
        </template>
        <a-button type="primary">
          <template #icon><DownloadOutlined /></template>
          导出
          <DownOutlined />
        </a-button>
      </a-dropdown>
    </div>

    <!-- 要导出的内容 -->
    <div id="trip-plan-content" class="plan-content">
      <!-- 旅行计划内容 -->
      <h1>{{ tripPlan.city }} 旅行计划</h1>
      <!-- ... 其他内容 ... -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import {
  DownloadOutlined,
  DownOutlined,
  PictureOutlined,
  FilePdfOutlined,
  FileTextOutlined,
} from '@ant-design/icons-vue';
import { exportTripPlan } from '@/utils/exportUtils';
import type { TripPlan } from '@/types';

const tripPlan = ref<TripPlan>({ /* ... */ });

const handleMenuClick = ({ key }: { key: string }) => {
  switch (key) {
    case 'image':
      exportTripPlan(tripPlan.value, { format: 'png' });
      break;
    case 'pdf':
      exportTripPlan(tripPlan.value, { format: 'pdf' });
      break;
    case 'formatted-pdf':
      exportTripPlan(tripPlan.value, { format: 'formatted-pdf' });
      break;
  }
};
</script>

<style scoped>
.export-buttons {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

/* 打印时隐藏导出按钮 */
@media print {
  .export-buttons {
    display: none;
  }
}
</style>
```

---

## ⚙️ 高级配置

### html2canvas 配置项

```typescript
const canvas = await html2canvas(element, {
  backgroundColor: '#ffffff',  // 背景色
  scale: 2,                    // 分辨率倍数（1-3）
  useCORS: true,               // 允许跨域图片
  allowTaint: false,           // 不允许污染画布
  logging: false,              // 关闭日志
  imageTimeout: 0,             // 图片加载超时
  windowWidth: 1200,           // 渲染窗口宽度
  windowHeight: 800,           // 渲染窗口高度
});
```

### jsPDF 配置项

```typescript
const pdf = new jsPDF({
  orientation: 'portrait',  // 纵向 (portrait) 或横向 (landscape)
  unit: 'mm',               // 单位：mm, cm, in, px
  format: 'a4',             // 纸张：a4, letter, legal
  compress: true,           // 压缩PDF
});
```

---

## 🐛 常见问题

### 1. 跨域图片问题

**问题：** Unsplash图片因跨域无法导出

**解决方案：**
```typescript
// 方案1：使用代理
const proxyUrl = `/api/proxy?url=${encodeURIComponent(imageUrl)}`;

// 方案2：在服务器端下载图片
const localUrl = await downloadImage(imageUrl);

// 方案3：使用 useCORS: true
const canvas = await html2canvas(element, { useCORS: true });
```

### 2. 地图无法导出

**问题：** 高德地图是Canvas渲染，html2canvas无法正确处理

**解决方案：**
```typescript
// 方案1：导出前隐藏地图
const prepareForExport = () => {
  const map = document.querySelector('.amap-container');
  if (map) map.style.display = 'none';
  
  return () => {
    if (map) map.style.display = '';
  };
};

// 方案2：使用静态地图
const staticMapUrl = await getStaticMapUrl(locations);
// 用图片替换动态地图

// 方案3：在服务器端截图
await api.captureMap(tripPlan);
```

### 3. PDF分页问题

**问题：** 内容过长，一页显示不完

**解决方案：**
```typescript
// 自动分页
if (imgHeight > pdfHeight) {
  let position = 0;
  const pageHeight = (canvas.width * pdfHeight) / pdfWidth;
  
  while (position < canvas.height) {
    // 截取当前页内容
    const pageCanvas = createPageCanvas(canvas, position, pageHeight);
    
    if (position > 0) pdf.addPage();
    pdf.addImage(pageCanvas.toDataURL(), 'PNG', 0, 0, pdfWidth, pdfHeight);
    
    position += pageHeight;
  }
}
```

### 4. 导出速度慢

**问题：** 内容多时导出需要等待

**解决方案：**
```typescript
// 显示加载提示
const hideLoading = message.loading('正在生成PDF，请稍候...', 0);

try {
  await exportAsPDF(elementId, tripPlan);
} finally {
  hideLoading();
}

// 或使用进度条
const progress = ref(0);

const updateProgress = (value: number) => {
  progress.value = value;
};

await exportWithProgress(elementId, updateProgress);
```

### 5. 导出图片模糊

**问题：** 导出的图片不清晰

**解决方案：**
```typescript
// 使用更高的 scale 值
const canvas = await html2canvas(element, {
  scale: 2, // 或 3，更高的值会更慢
});

// 设置更高的 DPI
const imgData = canvas.toDataURL('image/png', 1.0); // 质量设为最高
```

---

## 🎯 优化建议

### 1. 准备导出内容

```typescript
// 隐藏不需要导出的元素
export const prepareForExport = () => {
  const elementsToHide = [
    '.edit-buttons',    // 编辑按钮
    '.action-buttons',  // 操作按钮
    '.export-buttons',  // 导出按钮
    '.amap-container',  // 地图容器
  ];

  const hiddenElements: HTMLElement[] = [];

  elementsToHide.forEach(selector => {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
      const htmlEl = el as HTMLElement;
      htmlEl.style.display = 'none';
      hiddenElements.push(htmlEl);
    });
  });

  // 返回恢复函数
  return () => hiddenElements.forEach(el => el.style.display = '');
};
```

### 2. 添加水印

```typescript
const addWatermark = (canvas: HTMLCanvasElement) => {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  ctx.font = '20px Arial';
  ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
  ctx.textAlign = 'center';
  ctx.fillText('智能旅行助手', canvas.width / 2, canvas.height - 30);
};
```

### 3. 压缩PDF

```typescript
const pdf = new jsPDF({
  orientation: 'portrait',
  unit: 'mm',
  format: 'a4',
  compress: true, // 启用压缩
});

// 降低图片质量
const imgData = canvas.toDataURL('image/jpeg', 0.8); // 使用JPEG，质量80%
```

---

## 📊 性能对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| PNG导出 | 简单快速 | 文件较大 | 快速分享 |
| 基础PDF | 兼容性好 | 无封面 | 简单存档 |
| 精美PDF | 专业美观 | 文件较大 | 正式分享 |
| 服务端截图 | 效果最好 | 需要后端 | 商业应用 |

---

## 🚀 未来优化方向

- [ ] 支持自定义模板
- [ ] 添加更多导出选项（Word、Excel）
- [ ] 实现服务端截图
- [ ] 支持批量导出
- [ ] 添加导出历史记录
- [ ] 集成云存储（OSS）

---

## 📖 相关文档

- [html2canvas文档](https://html2canvas.hertzen.com/)
- [jsPDF文档](https://github.com/parallax/jsPDF)
- [Canvas API](https://developer.mozilla.org/zh-CN/docs/Web/API/Canvas_API)

---

**🎉 导出功能完成！用户可以方便地保存和分享旅行计划了！**
