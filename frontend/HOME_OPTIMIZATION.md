/**
 * Home.vue 优化方案 - 集成美化进度条
 */

// ===================================
// 步骤1: 导入 LoadingProgress 组件
// ===================================

// 在 script setup 中添加：
import LoadingProgress from '@/components/LoadingProgress.vue';

// 移除 LoadingOutlined 的导入（不再需要）


// ===================================
// 步骤2: 优化进度模拟函数
// ===================================

// 更详细的进度步骤
const simulateProgress = () => {
  const steps = [
    { progress: 0, status: '🚀 开始生成旅行计划...', duration: 0 },
    { progress: 20, status: '🔍 正在搜索景点信息...', duration: 2000 },
    { progress: 40, status: '🌤️ 正在查询天气数据...', duration: 1500 },
    { progress: 60, status: '🏨 正在推荐酒店住宿...', duration: 1500 },
    { progress: 80, status: '📋 正在生成详细行程...', duration: 2000 },
    { progress: 95, status: '🎨 正在获取景点图片...', duration: 1000 },
    { progress: 100, status: '✅ 计划生成完成！', duration: 500 },
  ];

  let currentStepIndex = 0;

  const updateStep = () => {
    if (currentStepIndex < steps.length) {
      const step = steps[currentStepIndex];
      const prevProgress = loadingProgress.value;
      const targetProgress = step.progress;
      const duration = step.duration;
      
      // 平滑过渡进度
      if (duration > 0) {
        const steps = 20;
        const increment = (targetProgress - prevProgress) / steps;
        const intervalTime = duration / steps;
        
        let currentStep = 0;
        const smoothInterval = setInterval(() => {
          if (currentStep < steps) {
            loadingProgress.value += increment;
            currentStep++;
          } else {
            clearInterval(smoothInterval);
            loadingProgress.value = targetProgress;
            loadingStatus.value = step.status;
            currentStepIndex++;
            updateStep();
          }
        }, intervalTime);
      } else {
        loadingProgress.value = targetProgress;
        loadingStatus.value = step.status;
        currentStepIndex++;
        updateStep();
      }
    }
  };

  updateStep();
};


// ===================================
// 步骤3: 优化提交函数
// ===================================

const handleSubmit = async () => {
  loading.value = true;
  loadingProgress.value = 0;
  loadingStatus.value = '准备开始...';

  // 启动进度动画
  simulateProgress();

  try {
    const response = await TripPlannerAPI.createTripPlan(formData.value);

    if (response.error) {
      message.error(response.error);
      loading.value = false;
    } else if (response.data) {
      // 确保进度到100%
      loadingProgress.value = 100;
      loadingStatus.value = '✅ 旅行计划生成成功！';
      
      // 短暂延迟后跳转
      setTimeout(() => {
        message.success('旅行计划生成成功！', 2);
        router.push({
          name: 'TripPlan',
          params: { plan: JSON.stringify(response.data) },
        });
      }, 800);
    }
  } catch (error) {
    message.error('生成旅行计划失败，请重试');
    console.error(error);
    loading.value = false;
  }
};


// ===================================
// 步骤4: 在模板中使用组件
// ===================================

/*
在 template 的最后（</div> 之前）添加：

<!-- 美化的加载进度组件 -->
<LoadingProgress
  :visible="loading"
  :progress="loadingProgress"
  :status="loadingStatus"
  :show-steps="true"
  :show-tips="true"
/>
*/


// ===================================
// 步骤5: 移除旧的加载进度UI
// ===================================

/*
删除或注释掉原来的加载UI部分：

<!-- 加载进度 -->
<div v-if="loading" class="loading-container">
  <a-progress
    :percent="loadingProgress"
    status="active"
    :show-info="false"
  />
  <div class="loading-status">
    <LoadingOutlined spin />
    <span>{{ loadingStatus }}</span>
  </div>
</div>
*/


// ===================================
// 步骤6: 移除旧的CSS样式
// ===================================

/*
删除以下CSS（不再需要）：

.loading-container {
  margin-top: 24px;
  padding: 24px;
  background: #f5f5f5;
  border-radius: 8px;
}

.loading-status {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 16px;
  font-size: 16px;
  color: #1890ff;
}

.loading-status span {
  margin-left: 12px;
}
*/


// ===================================
// 完整的优化代码示例
// ===================================

/*
<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import {
  GlobalOutlined,
  EditOutlined,
  EnvironmentOutlined,
  // ... 其他图标导入
  // 注意：移除 LoadingOutlined
} from '@ant-design/icons-vue';
import { TripPlannerAPI } from '@/services';
import type { TripPlanRequest } from '@/types';
import LoadingProgress from '@/components/LoadingProgress.vue'; // 新增

const router = useRouter();
const loading = ref(false);
const loadingProgress = ref(0);
const loadingStatus = ref('');

const formData = ref<TripPlanRequest>({
  // ... 表单数据
});

// 使用上面优化的 simulateProgress 函数

// 使用上面优化的 handleSubmit 函数

// 其他函数保持不变...
</script>
*/


// ===================================
// 额外优化建议
// ===================================

/*
1. 可以根据实际API响应时间动态调整进度
2. 如果API很快完成，确保进度动画也完成
3. 添加错误处理时的进度重置
4. 考虑添加取消按钮（可选）
*/

// 示例：基于API响应动态调整进度
const handleSubmitAdvanced = async () => {
  loading.value = true;
  loadingProgress.value = 0;
  
  try {
    // 并行执行进度动画和API调用
    const progressPromise = new Promise<void>((resolve) => {
      simulateProgress();
      // 假设总时长约8秒
      setTimeout(resolve, 8000);
    });
    
    const apiPromise = TripPlannerAPI.createTripPlan(formData.value);
    
    // 等待两者都完成
    const [_, response] = await Promise.all([progressPromise, apiPromise]);
    
    // 如果API提前完成，进度会继续到100%
    // 如果进度提前完成，会等待API
    
    if (response.error) {
      message.error(response.error);
    } else if (response.data) {
      loadingProgress.value = 100;
      loadingStatus.value = '✅ 完成！';
      
      setTimeout(() => {
        router.push({
          name: 'TripPlan',
          params: { plan: JSON.stringify(response.data) },
        });
      }, 800);
    }
  } catch (error) {
    message.error('生成失败');
    console.error(error);
  } finally {
    setTimeout(() => {
      loading.value = false;
    }, 1000);
  }
};
