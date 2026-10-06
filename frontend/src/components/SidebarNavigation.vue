<template>
  <div class="sidebar-navigation">
    <!-- 侧边导航栏 -->
    <a-affix :offset-top="80">
      <div class="sidebar-menu">
        <a-menu
          v-model:selectedKeys="selectedKeys"
          mode="inline"
          :style="{ borderRight: 0 }"
          @click="handleMenuClick"
        >
          <!-- 行程概览 -->
          <a-menu-item key="overview">
            <template #icon><FileTextOutlined /></template>
            行程概览
          </a-menu-item>

          <!-- 预算明细 -->
          <a-menu-item key="budget">
            <template #icon><DollarOutlined /></template>
            预算明细
          </a-menu-item>

          <!-- 天气信息 -->
          <a-menu-item key="weather">
            <template #icon><CloudOutlined /></template>
            天气信息
          </a-menu-item>

          <!-- 每日行程 -->
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

          <!-- 景点列表 -->
          <a-sub-menu key="attractions" title="景点列表">
            <template #icon><PushpinOutlined /></template>
            <a-menu-item
              v-for="(attraction, index) in allAttractions"
              :key="`attraction-${index}`"
            >
              {{ attraction.name }}
            </a-menu-item>
          </a-sub-menu>

          <!-- 住宿信息 -->
          <a-menu-item key="hotels">
            <template #icon><HomeOutlined /></template>
            住宿信息
          </a-menu-item>

          <!-- 旅行建议 -->
          <a-menu-item key="suggestions">
            <template #icon><BulbOutlined /></template>
            旅行建议
          </a-menu-item>
        </a-menu>

        <!-- 快捷操作按钮 -->
        <div class="quick-actions">
          <a-divider />
          <a-space direction="vertical" :size="8" style="width: 100%;">
            <a-button
              type="primary"
              block
              size="small"
              @click="$emit('edit')"
            >
              <template #icon><EditOutlined /></template>
              编辑行程
            </a-button>

            <a-button block size="small" @click="$emit('export')">
              <template #icon><DownloadOutlined /></template>
              导出PDF
            </a-button>

            <a-button block size="small" @click="$emit('share')">
              <template #icon><ShareAltOutlined /></template>
              分享
            </a-button>

            <a-button block size="small" @click="scrollToTop">
              <template #icon><VerticalAlignTopOutlined /></template>
              回到顶部
            </a-button>
          </a-space>
        </div>

        <!-- 进度指示器 -->
        <div class="scroll-progress">
          <a-progress
            :percent="scrollProgress"
            :show-info="false"
            stroke-color="#1890ff"
            size="small"
          />
          <div class="progress-text">阅读进度 {{ Math.round(scrollProgress) }}%</div>
        </div>
      </div>
    </a-affix>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import {
  FileTextOutlined,
  DollarOutlined,
  CloudOutlined,
  CalendarOutlined,
  PushpinOutlined,
  HomeOutlined,
  BulbOutlined,
  EditOutlined,
  DownloadOutlined,
  ShareAltOutlined,
  VerticalAlignTopOutlined,
} from '@ant-design/icons-vue';
import type { TripPlan } from '@/types';

interface Props {
  tripPlan: TripPlan;
}

const props = defineProps<Props>();
const emit = defineEmits(['edit', 'export', 'share']);

// 当前选中的菜单项
const selectedKeys = ref<string[]>(['overview']);

// 滚动进度
const scrollProgress = ref(0);

// 所有景点列表（扁平化）
const allAttractions = computed(() => {
  const attractions: any[] = [];
  props.tripPlan.days.forEach((day, dayIndex) => {
    day.attractions.forEach((attraction, attrIndex) => {
      attractions.push({
        ...attraction,
        dayIndex,
        attrIndex,
        id: `day-${dayIndex}-attraction-${attrIndex}`,
      });
    });
  });
  return attractions;
});

// 点击菜单项
const handleMenuClick = ({ key }: { key: string }) => {
  scrollToSection(key);
};

// 滚动到指定区域
const scrollToSection = (key: string) => {
  let elementId = key;

  // 处理每日行程
  if (key.startsWith('day-') && !key.includes('attraction')) {
    const dayIndex = parseInt(key.split('-')[1]);
    elementId = `day-section-${dayIndex}`;
  }
  // 处理景点
  else if (key.startsWith('attraction-')) {
    const attrIndex = parseInt(key.split('-')[1]);
    const attraction = allAttractions.value[attrIndex];
    if (attraction) {
      elementId = attraction.id;
    }
  }

  const element = document.getElementById(elementId);
  if (element) {
    // 平滑滚动
    element.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
    });

    // 高亮元素（可选）
    highlightElement(element);

    // 更新选中状态
    selectedKeys.value = [key];
  }
};

// 高亮元素
const highlightElement = (element: HTMLElement) => {
  element.classList.add('highlighted');
  setTimeout(() => {
    element.classList.remove('highlighted');
  }, 2000);
};

// 回到顶部
const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  });
  selectedKeys.value = ['overview'];
};

// 更新滚动进度
const updateScrollProgress = () => {
  const windowHeight = window.innerHeight;
  const documentHeight = document.documentElement.scrollHeight;
  const scrollTop = window.scrollY || document.documentElement.scrollTop;

  const totalScroll = documentHeight - windowHeight;
  const progress = (scrollTop / totalScroll) * 100;

  scrollProgress.value = Math.min(Math.max(progress, 0), 100);

  // 根据滚动位置自动更新选中菜单
  updateActiveSection();
};

// 根据滚动位置更新选中菜单
const updateActiveSection = () => {
  const sections = [
    'overview',
    'budget',
    'weather',
    ...props.tripPlan.days.map((_, i) => `day-${i}`),
    'hotels',
    'suggestions',
  ];

  const scrollTop = window.scrollY + 100; // 偏移100px

  for (const sectionKey of sections) {
    let elementId = sectionKey;
    if (sectionKey.startsWith('day-')) {
      const dayIndex = parseInt(sectionKey.split('-')[1]);
      elementId = `day-section-${dayIndex}`;
    }

    const element = document.getElementById(elementId);
    if (element) {
      const rect = element.getBoundingClientRect();
      const elementTop = rect.top + window.scrollY;

      if (scrollTop >= elementTop && scrollTop < elementTop + element.offsetHeight) {
        selectedKeys.value = [sectionKey];
        break;
      }
    }
  }
};

// 监听滚动事件
onMounted(() => {
  window.addEventListener('scroll', updateScrollProgress);
  updateScrollProgress();
});

onUnmounted(() => {
  window.removeEventListener('scroll', updateScrollProgress);
});
</script>

<style scoped>
.sidebar-navigation {
  width: 250px;
  position: sticky;
  top: 80px;
}

.sidebar-menu {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.day-date {
  font-size: 12px;
  color: #999;
  margin-left: 8px;
}

.quick-actions {
  padding: 16px;
}

.scroll-progress {
  padding: 16px;
  padding-top: 0;
}

.progress-text {
  font-size: 12px;
  color: #666;
  margin-top: 8px;
  text-align: center;
}

/* 高亮动画 */
:global(.highlighted) {
  animation: highlight 2s ease-in-out;
}

@keyframes highlight {
  0%,
  100% {
    background-color: transparent;
  }
  50% {
    background-color: rgba(24, 144, 255, 0.1);
  }
}

/* 响应式：小屏幕隐藏侧边栏 */
@media (max-width: 768px) {
  .sidebar-navigation {
    display: none;
  }
}
</style>
