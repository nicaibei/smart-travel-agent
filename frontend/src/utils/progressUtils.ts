// This file contains legacy progress experiments and is not part of the runtime.
// @ts-nocheck
/**
 * 进度条优化方案
 */

// ===================================
// 方案1：基于实际API响应的进度更新
// ===================================

const loading = ref(false);
const loadingProgress = ref(0);
const loadingStatus = ref('');
const currentStep = ref(0);

// 进度步骤配置
const progressSteps = [
  { progress: 0, status: '🚀 开始生成旅行计划...', duration: 0 },
  { progress: 15, status: '🔍 正在搜索景点信息...', duration: 2000 },
  { progress: 35, status: '🌤️ 正在查询天气数据...', duration: 1500 },
  { progress: 55, status: '🏨 正在推荐酒店住宿...', duration: 1500 },
  { progress: 75, status: '📋 正在生成详细行程...', duration: 2000 },
  { progress: 90, status: '🎨 正在获取景点图片...', duration: 1000 },
  { progress: 100, status: '✅ 旅行计划生成完成！', duration: 500 }
];

// 模拟进度更新（更流畅的动画）
const simulateProgress = () => {
  return new Promise<void>((resolve) => {
    let stepIndex = 0;

    const updateProgress = () => {
      if (stepIndex < progressSteps.length) {
        const step = progressSteps[stepIndex];
        
        // 平滑过渡到目标进度
        const startProgress = loadingProgress.value;
        const targetProgress = step.progress;
        const stepDuration = step.duration;
        const stepCount = 20; // 分20步完成过渡
        const progressIncrement = (targetProgress - startProgress) / stepCount;
        const intervalDuration = stepDuration / stepCount;

        let currentStepCount = 0;
        const smoothInterval = setInterval(() => {
          if (currentStepCount < stepCount) {
            loadingProgress.value += progressIncrement;
            currentStepCount++;
          } else {
            clearInterval(smoothInterval);
            loadingProgress.value = targetProgress;
            loadingStatus.value = step.status;
            stepIndex++;
            
            if (stepIndex < progressSteps.length) {
              setTimeout(updateProgress, 100);
            } else {
              resolve();
            }
          }
        }, intervalDuration);
      }
    };

    updateProgress();
  });
};

// 提交表单（改进版）
const handleSubmit = async () => {
  loading.value = true;
  loadingProgress.value = 0;
  loadingStatus.value = progressSteps[0].status;
  currentStep.value = 0;

  try {
    // 启动进度模拟
    const progressPromise = simulateProgress();
    
    // 调用API
    const apiPromise = generateTripPlan(formData.value);
    
    // 等待两者都完成
    const [_, response] = await Promise.all([progressPromise, apiPromise]);
    
    // 显示完成状态
    await new Promise(resolve => setTimeout(resolve, 500));
    
    message.success('旅行计划生成成功！', 2);
    
    // 跳转到结果页
    router.push({ 
      name: 'result', 
      params: { plan: JSON.stringify(response) }
    });
    
  } catch (error) {
    console.error('生成计划失败:', error);
    loadingProgress.value = 0;
    loadingStatus.value = '❌ 生成失败';
    message.error('生成旅行计划失败，请重试');
  } finally {
    setTimeout(() => {
      loading.value = false;
    }, 1000);
  }
};


// ===================================
// 方案2：基于时间的渐进式进度
// ===================================

const loading2 = ref(false);
const loadingProgress2 = ref(0);
const loadingStatus2 = ref('');

// 进度配置（更细粒度）
const progressConfig = {
  phases: [
    {
      name: '初始化',
      icon: '🚀',
      message: '准备开始生成旅行计划...',
      progress: [0, 5],
      duration: 500
    },
    {
      name: '景点搜索',
      icon: '🔍',
      message: '正在搜索热门景点...',
      progress: [5, 30],
      duration: 3000
    },
    {
      name: '天气查询',
      icon: '🌤️',
      message: '正在查询目的地天气...',
      progress: [30, 50],
      duration: 2000
    },
    {
      name: '酒店推荐',
      icon: '🏨',
      message: '正在为您推荐合适的酒店...',
      progress: [50, 70],
      duration: 2500
    },
    {
      name: '行程生成',
      icon: '📋',
      message: '正在智能规划每日行程...',
      progress: [70, 90],
      duration: 3000
    },
    {
      name: '图片获取',
      icon: '🎨',
      message: '正在为景点配图...',
      progress: [90, 98],
      duration: 1500
    },
    {
      name: '完成',
      icon: '✅',
      message: '旅行计划生成完成！',
      progress: [98, 100],
      duration: 500
    }
  ]
};

// 执行进度动画
const animateProgress = async (startProgress: number, endProgress: number, duration: number, message: string) => {
  return new Promise<void>((resolve) => {
    const startTime = Date.now();
    const progressRange = endProgress - startProgress;
    
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // 使用缓动函数（easeOutCubic）
      const eased = 1 - Math.pow(1 - progress, 3);
      
      loadingProgress2.value = startProgress + progressRange * eased;
      loadingStatus2.value = message;
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        loadingProgress2.value = endProgress;
        resolve();
      }
    };
    
    requestAnimationFrame(animate);
  });
};

// 执行所有进度阶段
const runProgressPhases = async () => {
  for (const phase of progressConfig.phases) {
    const [start, end] = phase.progress;
    const message = `${phase.icon} ${phase.message}`;
    await animateProgress(start, end, phase.duration, message);
  }
};

// 提交表单（方案2）
const handleSubmit2 = async () => {
  loading2.value = true;
  loadingProgress2.value = 0;

  try {
    // 并行执行进度动画和API调用
    const [_, response] = await Promise.all([
      runProgressPhases(),
      generateTripPlan(formData.value)
    ]);
    
    message.success('旅行计划生成成功！', 2);
    
    setTimeout(() => {
      router.push({ 
        name: 'result', 
        params: { plan: JSON.stringify(response) }
      });
    }, 500);
    
  } catch (error) {
    console.error('生成计划失败:', error);
    loadingProgress2.value = 0;
    loadingStatus2.value = '❌ 生成失败，请重试';
    message.error({
      content: '生成旅行计划失败，请检查网络连接或稍后重试',
      duration: 3
    });
  } finally {
    setTimeout(() => {
      loading2.value = false;
    }, 1000);
  }
};


// ===================================
// 方案3：带详细步骤的进度显示
// ===================================

interface ProgressStep {
  id: string;
  label: string;
  icon: string;
  status: 'waiting' | 'processing' | 'completed' | 'error';
  progress: number;
}

const loading3 = ref(false);
const loadingProgress3 = ref(0);
const progressSteps3 = ref<ProgressStep[]>([
  { id: 'attractions', label: '搜索景点', icon: '🔍', status: 'waiting', progress: 0 },
  { id: 'weather', label: '查询天气', icon: '🌤️', status: 'waiting', progress: 0 },
  { id: 'hotels', label: '推荐酒店', icon: '🏨', status: 'waiting', progress: 0 },
  { id: 'planning', label: '生成行程', icon: '📋', status: 'waiting', progress: 0 },
  { id: 'images', label: '获取图片', icon: '🎨', status: 'waiting', progress: 0 }
]);

// 更新步骤状态
const updateStepStatus = async (stepId: string, status: 'processing' | 'completed' | 'error') => {
  const step = progressSteps3.value.find(s => s.id === stepId);
  if (step) {
    step.status = status;
    
    if (status === 'processing') {
      // 模拟步骤进度
      const duration = 2000;
      const startTime = Date.now();
      
      const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        step.progress = progress * 100;
        
        if (progress < 1 && step.status === 'processing') {
          requestAnimationFrame(animate);
        }
      };
      
      requestAnimationFrame(animate);
    } else if (status === 'completed') {
      step.progress = 100;
    }
  }
};

// 计算总进度
const calculateTotalProgress = () => {
  const totalSteps = progressSteps3.value.length;
  const completedSteps = progressSteps3.value.filter(s => s.status === 'completed').length;
  const currentStepProgress = progressSteps3.value.find(s => s.status === 'processing')?.progress || 0;
  
  return ((completedSteps + currentStepProgress / 100) / totalSteps) * 100;
};

// 提交表单（方案3）
const handleSubmit3 = async () => {
  loading3.value = true;
  
  // 重置所有步骤
  progressSteps3.value.forEach(step => {
    step.status = 'waiting';
    step.progress = 0;
  });

  try {
    // 依次执行步骤
    for (const step of progressSteps3.value) {
      await updateStepStatus(step.id, 'processing');
      loadingProgress3.value = calculateTotalProgress();
      
      // 模拟步骤执行时间
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      await updateStepStatus(step.id, 'completed');
      loadingProgress3.value = calculateTotalProgress();
    }
    
    // 实际API调用应该在这里
    const response = await generateTripPlan(formData.value);
    
    message.success('旅行计划生成成功！', 2);
    router.push({ 
      name: 'result', 
      params: { plan: JSON.stringify(response) }
    });
    
  } catch (error) {
    console.error('生成计划失败:', error);
    
    // 标记当前步骤为错误
    const currentStep = progressSteps3.value.find(s => s.status === 'processing');
    if (currentStep) {
      await updateStepStatus(currentStep.id, 'error');
    }
    
    message.error('生成旅行计划失败，请重试');
  } finally {
    setTimeout(() => {
      loading3.value = false;
    }, 1000);
  }
};


// ===================================
// 推荐使用：方案1（最平衡）
// ===================================

export {
  // 方案1：推荐
  handleSubmit,
  loading,
  loadingProgress,
  loadingStatus,
  
  // 方案2：更流畅的动画
  handleSubmit2,
  loading2,
  loadingProgress2,
  loadingStatus2,
  
  // 方案3：详细步骤显示
  handleSubmit3,
  loading3,
  loadingProgress3,
  progressSteps3
};
