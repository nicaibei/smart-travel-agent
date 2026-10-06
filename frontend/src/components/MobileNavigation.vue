<template>
  <div class="mobile-navigation">
    <!-- 浮动导航按钮 -->
    <a-float-button-group
      trigger="click"
      type="primary"
      :style="{ right: '24px', bottom: '24px' }"
    >
      <template #icon>
        <MenuOutlined />
      </template>

      <!-- 回到顶部 -->
      <a-float-button @click="scrollToTop">
        <template #icon>
          <VerticalAlignTopOutlined />
        </template>
      </a-float-button>

      <!-- 打开目录 -->
      <a-float-button @click="showDrawer">
        <template #icon>
          <UnorderedListOutlined />
        </template>
      </a-float-button>

      <!-- 编辑 -->
      <a-float-button @click="$emit('edit')">
        <template #icon>
          <EditOutlined />
        </template>
      </a-float-button>

      <!-- 导出 -->
      <a-float-button @click="$emit('export')">
        <template #icon>
          <DownloadOutlined />
        </template>
      </a-float-button>
    </a-float-button-group>

    <!-- 侧滑抽屉 - 目录 -->
    <a-drawer
      v-model:visible="drawerVisible"
      title="目录导航"
      placement="right"
      :width="280"
    >
      <a-menu
        v-model:selectedKeys="selectedKeys"
        mode="inline"
        @click="handleMenuClick"
      >
        <a-menu-item key="overview">
          <template #icon><FileTextOutlined /></template>
          行程概览
        </a-menu-item>

        <a-menu-item key="budget">
          <template #icon><DollarOutlined /></template>
          预算明细
        </a-menu-item>

        <a-menu-item key="weather">
          <template #icon><CloudOutlined /></template>
          天气信息
        </a-menu-item>

        <a-sub-menu key="days" title="每日行程">
          <template #icon><CalendarOutlined /></template>
          <a-menu-item
            v-for="(day, index) in tripPlan.days"
            :key="`day-${index}`"
          >
            <a-badge :count="day.attractions.length" :offset="[10, 0]">
              第 {{ index + 1 }} 天
            </a-badge>
            <div class="day-info">{{ day.date }}</div>
          </a-menu-item>
        </a-sub-menu>

        <a-menu-item key="hotels">
          <template #icon><HomeOutlined /></template>
          住宿信息
        </a-menu-item>

        <a-menu-item key="suggestions">
          <template #icon><BulbOutlined /></template>
          旅行建议
        </a-menu-item>
      </a-menu>

      <!-- 进度指示 -->
      <div class="drawer-footer">
        <a-divider />
        <div class="reading-progress">
          <div class="progress-label">阅读进度</div>
          <a-progress
            :percent="scrollProgress"
            :stroke-color="{
              '0%': '#108ee9',
              '100%': '#87d068',
            }"
          />
        </div>
      </div>
    </a-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import {
  MenuOutlined,
  VerticalAlignTopOutlined,
  UnorderedListOutlined,
  EditOutlined,
  DownloadOutlined,
  FileTextOutlined,
  DollarOutlined,
  CloudOutlined,
  CalendarOutlined,
  HomeOutlined,
  BulbOutlined,
} from '@ant-design/icons-vue';
import type { TripPlan } from '@/types';

interface Props {
  tripPlan: TripPlan;
}

defineProps<Props>();

const drawerVisible = ref(false);
const selectedKeys = ref<string[]>(['overview']);
const scrollProgress = ref(0);

// 显示抽屉
const showDrawer = () => {
  drawerVisible.value = true;
};

// 回到顶部
const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  });
  selectedKeys.value = ['overview'];
};

// 点击菜单项
const handleMenuClick = ({ key }: { key: string }) => {
  scrollToSection(key);
  drawerVisible.value = false; // 关闭抽屉
};

// 滚动到指定区域
const scrollToSection = (key: string) => {
  let elementId = key;

  if (key.startsWith('day-')) {
    const dayIndex = parseInt(key.split('-')[1]);
    elementId = `day-section-${dayIndex}`;
  }

  const element = document.getElementById(elementId);
  if (element) {
    element.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
    });
    selectedKeys.value = [key];
  }
};

// 更新滚动进度
const updateScrollProgress = () => {
  const windowHeight = window.innerHeight;
  const documentHeight = document.documentElement.scrollHeight;
  const scrollTop = window.scrollY || document.documentElement.scrollTop;

  const totalScroll = documentHeight - windowHeight;
  const progress = (scrollTop / totalScroll) * 100;

  scrollProgress.value = Math.min(Math.max(progress, 0), 100);
};

onMounted(() => {
  window.addEventListener('scroll', updateScrollProgress);
  updateScrollProgress();
});

onUnmounted(() => {
  window.removeEventListener('scroll', updateScrollProgress);
});
</script>

<style scoped>
/* 只在小屏幕显示 */
.mobile-navigation {
  display: none;
}

@media (max-width: 768px) {
  .mobile-navigation {
    display: block;
  }
}

.day-info {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.drawer-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px 24px;
  background: white;
}

.reading-progress {
  text-align: center;
}

.progress-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}
</style>
