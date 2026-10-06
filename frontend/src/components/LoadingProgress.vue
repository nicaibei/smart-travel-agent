<template>
  <div class="loading-overlay" v-if="visible">
    <div class="loading-container">
      <!-- 进度环 -->
      <div class="progress-circle">
        <svg width="200" height="200" viewBox="0 0 200 200">
          <!-- 背景圆 -->
          <circle
            cx="100"
            cy="100"
            r="90"
            fill="none"
            stroke="#e6e6e6"
            stroke-width="8"
          />
          <!-- 进度圆 -->
          <circle
            cx="100"
            cy="100"
            r="90"
            fill="none"
            stroke="url(#gradient)"
            stroke-width="8"
            stroke-linecap="round"
            :stroke-dasharray="circumference"
            :stroke-dashoffset="progressOffset"
            transform="rotate(-90 100 100)"
            class="progress-circle-path"
          />
          <!-- 渐变定义 -->
          <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
              <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
            </linearGradient>
          </defs>
        </svg>
        
        <!-- 中心内容 -->
        <div class="progress-center">
          <div class="progress-icon">{{ currentIcon }}</div>
          <div class="progress-percent">{{ Math.round(progress) }}%</div>
        </div>
      </div>

      <!-- 状态文本 -->
      <div class="loading-status">
        <div class="status-text">{{ status }}</div>
      </div>

      <!-- 步骤指示器 -->
      <div class="steps-indicator" v-if="showSteps">
        <div
          v-for="(step, index) in steps"
          :key="index"
          class="step-item"
          :class="getStepClass(index)"
        >
          <div class="step-icon">{{ step.icon }}</div>
          <div class="step-label">{{ step.label }}</div>
        </div>
      </div>

      <!-- 提示信息 -->
      <div class="loading-tips" v-if="showTips">
        <div class="tip-item">
          <CheckCircleOutlined class="tip-icon" />
          <span>正在使用AI智能规划行程</span>
        </div>
        <div class="tip-item">
          <CheckCircleOutlined class="tip-icon" />
          <span>自动为景点配图</span>
        </div>
        <div class="tip-item">
          <CheckCircleOutlined class="tip-icon" />
          <span>计算详细预算</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { CheckCircleOutlined } from '@ant-design/icons-vue';

interface Props {
  visible: boolean;
  progress: number;
  status: string;
  showSteps?: boolean;
  showTips?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  visible: false,
  progress: 0,
  status: '',
  showSteps: true,
  showTips: true
});

// 步骤配置
const steps = [
  { icon: '🔍', label: '搜索景点' },
  { icon: '🌤️', label: '查询天气' },
  { icon: '🏨', label: '推荐酒店' },
  { icon: '📋', label: '生成行程' },
  { icon: '🎨', label: '获取图片' }
];

// 圆的周长
const radius = 90;
const circumference = 2 * Math.PI * radius;

// 进度偏移
const progressOffset = computed(() => {
  return circumference - (props.progress / 100) * circumference;
});

// 当前图标
const currentIcon = computed(() => {
  const index = Math.floor((props.progress / 100) * steps.length);
  return steps[Math.min(index, steps.length - 1)].icon;
});

// 获取步骤样式
const getStepClass = (index: number) => {
  const currentStep = Math.floor((props.progress / 100) * steps.length);
  
  if (index < currentStep) {
    return 'completed';
  } else if (index === currentStep) {
    return 'active';
  } else {
    return 'pending';
  }
};
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.loading-container {
  text-align: center;
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* 进度环 */
.progress-circle {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto 30px;
}

.progress-circle-path {
  transition: stroke-dashoffset 0.3s ease;
}

.progress-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.progress-icon {
  font-size: 48px;
  margin-bottom: 8px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.progress-percent {
  font-size: 24px;
  font-weight: bold;
  color: white;
}

/* 状态文本 */
.loading-status {
  margin-bottom: 40px;
}

.status-text {
  font-size: 18px;
  color: white;
  font-weight: 500;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

/* 步骤指示器 */
.steps-indicator {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 40px;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  opacity: 0.5;
  transition: all 0.3s ease;
}

.step-item.active {
  opacity: 1;
  transform: scale(1.1);
}

.step-item.completed {
  opacity: 0.8;
}

.step-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.step-item.active .step-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: white;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.5);
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.step-item.completed .step-icon {
  background: rgba(76, 175, 80, 0.3);
  border-color: #4caf50;
}

.step-label {
  font-size: 12px;
  color: white;
  white-space: nowrap;
}

/* 提示信息 */
.loading-tips {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 300px;
  margin: 0 auto;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: white;
  font-size: 14px;
  animation: slideInLeft 0.5s ease-out;
}

.tip-item:nth-child(1) {
  animation-delay: 0.1s;
}

.tip-item:nth-child(2) {
  animation-delay: 0.2s;
}

.tip-item:nth-child(3) {
  animation-delay: 0.3s;
}

@keyframes slideInLeft {
  from {
    transform: translateX(-20px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.tip-icon {
  color: #4caf50;
  font-size: 16px;
}
</style>
