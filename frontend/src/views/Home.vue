<template>
  <div class="home-page">
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-copy">
          <div class="hero-kicker"><span class="kicker-mark"></span>智能旅行规划工作台</div>
          <h1 class="hero-title">智能旅行助手</h1>
          <p class="hero-subtitle">从目的地灵感，到每天走得通的旅行安排。</p>
          <div class="hero-capabilities">
            <span><img class="amap-capability-icon" src="/assets/amap-marker.png" alt="高德地图" /> 景点信息</span>
            <span><i class="weather-sun-icon" aria-hidden="true">☀</i> 逐日天气</span>
            <span><WalletOutlined /> 预算拆分</span>
          </div>
        </div>
        <div class="hero-advisor" aria-live="polite">
          <div class="hero-advisor-portrait">
            <img src="/assets/xiaolv-consultant.png" alt="小旅顾问" />
            <span class="advisor-mood">{{ advisorMood }}</span>
          </div>
          <div class="hero-advisor-message">
            <div class="advisor-presence"><span></span>小旅顾问在线</div>
            <p>{{ advisorMessage }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Form Section -->
    <div class="form-section">
      <div class="planning-layout">
      <a-card class="form-card" :loading="loading">
        <template #title>
          <span class="form-title">
            <EditOutlined />
            开始规划您的旅程
          </span>
        </template>

        <a-form
          :model="formData"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 18 }"
          @finish="handleSubmit"
        >
          <!-- 目的地城市 -->
          <a-form-item
            label="目的地城市"
            name="city"
            :rules="[{ required: true, message: '请输入目的地城市' }]"
          >
            <a-input
              v-model:value="formData.city"
              placeholder="例如: 北京、上海、杭州"
              size="large"
            >
              <template #prefix>
                <EnvironmentOutlined />
              </template>
            </a-input>
          </a-form-item>

          <!-- 日期范围 -->
          <a-form-item
            label="出行日期"
            name="start_date"
            :rules="[{ validator: validateDates }]"
          >
            <a-row :gutter="16">
              <a-col :span="12">
                <a-date-picker
                  v-model:value="formData.start_date"
                  placeholder="开始日期"
                  size="large"
                  style="width: 100%"
                  format="YYYY-MM-DD"
                  value-format="YYYY-MM-DD"
                />
              </a-col>
              <a-col :span="12">
                <a-date-picker
                  v-model:value="formData.end_date"
                  placeholder="结束日期"
                  size="large"
                  style="width: 100%"
                  format="YYYY-MM-DD"
                  value-format="YYYY-MM-DD"
                />
              </a-col>
            </a-row>
          </a-form-item>

          <!-- 旅行天数 -->
          <a-form-item
            label="旅行天数"
            name="days"
            :rules="[{ required: true, message: '请输入旅行天数' }]"
          >
            <a-input-number
              v-model:value="formData.days"
              :min="1"
              :max="30"
              size="large"
              style="width: 100%"
            >
              <template #addonAfter>天</template>
            </a-input-number>
          </a-form-item>

          <!-- 旅行偏好 -->
          <a-form-item label="旅行偏好" name="preferences">
            <a-select
              v-model:value="formData.preferences"
              size="large"
              placeholder="选择您的旅行偏好"
            >
              <a-select-option value="历史文化">
                <BookOutlined /> 历史文化
              </a-select-option>
              <a-select-option value="自然风光">
                <PictureOutlined /> 自然风光
              </a-select-option>
              <a-select-option value="美食探索">
                <CoffeeOutlined /> 美食探索
              </a-select-option>
              <a-select-option value="购物娱乐">
                <ShoppingOutlined /> 购物娱乐
              </a-select-option>
              <a-select-option value="休闲度假">
                <SmileOutlined /> 休闲度假
              </a-select-option>
            </a-select>
          </a-form-item>

          <!-- 预算 -->
          <a-form-item label="预算范围" name="budget">
            <a-input-number
              v-model:value="formData.budget"
              :min="0"
              :step="500"
              size="large"
              style="width: 100%"
            >
              <template #prefix>¥</template>
              <template #addonAfter>元</template>
            </a-input-number>
          </a-form-item>

          <!-- 交通方式 -->
          <a-form-item label="交通方式" name="transportation">
            <a-radio-group v-model:value="formData.transportation" size="large">
              <a-radio-button value="公共交通">
                <CarOutlined /> 公共交通
              </a-radio-button>
              <a-radio-button value="自驾">
                <CarOutlined /> 自驾
              </a-radio-button>
              <a-radio-button value="出租车/网约车">
                <TaxiOutlined /> 打车
              </a-radio-button>
            </a-radio-group>
          </a-form-item>

          <!-- 住宿类型 -->
          <a-form-item label="住宿类型" name="accommodation">
            <a-radio-group v-model:value="formData.accommodation" size="large">
              <a-radio-button value="经济型">
                <span class="hotel-symbol" aria-hidden="true">🏨</span> 经济型
              </a-radio-button>
              <a-radio-button value="舒适型">
                <span class="hotel-symbol" aria-hidden="true">🏨</span> 舒适型
              </a-radio-button>
              <a-radio-button value="豪华型">
                <span class="hotel-symbol" aria-hidden="true">🏨</span> 豪华型
              </a-radio-button>
            </a-radio-group>
          </a-form-item>

          <a-form-item label="额外要求" name="special_requirements" :help="'填写向导选项之外的要求'">
            <a-textarea
              v-model:value="formData.special_requirements"
              :maxlength="300"
              :rows="2"
              show-count
              placeholder="例如：想去襄阳唐城看夜景，避免排队太久"
            />
          </a-form-item>

          <!-- 提交按钮 -->
          <a-form-item :wrapper-col="{ span: 18, offset: 6 }">
            <a-space>
              <a-button
                type="primary"
                html-type="submit"
                size="large"
                :loading="loading"
              >
                <template #icon>
                  <RocketOutlined />
                </template>
                {{ loading ? '正在生成...' : '开始规划' }}
              </a-button>
              <a-button size="large" @click="handleReset">
                重置
              </a-button>
            </a-space>
          </a-form-item>
        </a-form>

        <!-- 不需要这里的加载进度了，使用全屏组件 -->
      </a-card>

      <aside class="assistant-panel">
        <div class="assistant-header">
          <img class="assistant-avatar" src="/assets/xiaolv-consultant.png" alt="小旅顾问" />
          <div class="assistant-identity">
            <strong>小旅顾问</strong>
            <span>你的专属旅行规划搭档</span>
          </div>
        </div>

        <div class="wizard-progress" aria-label="向导步骤">
          <button v-for="step in 3" :key="step" :class="{ current: wizardStep === step, complete: wizardStep > step || wizardComplete }" :disabled="step > wizardStep && !wizardComplete" :aria-label="`第${step}步`" @click="openWizardStep(step)">
            <span>{{ step }}</span><i v-if="step < 3" />
          </button>
        </div>

        <div v-if="!wizardComplete" class="wizard-body">
          <template v-if="wizardStep === 1">
            <span class="wizard-step-label">01 · 同行人群</span>
            <h3>这趟和谁一起出发？</h3>
            <p class="wizard-hint">我们会据此调整步行强度与休息建议。</p>
            <div class="wizard-options">
              <button v-for="option in travelerOptions" :key="option.value" :class="{ selected: formData.traveler_type === option.value }" :aria-pressed="formData.traveler_type === option.value" @click="formData.traveler_type = option.value">
                <span>{{ option.icon }}</span><strong>{{ option.label }}</strong><small>{{ option.detail }}</small>
              </button>
            </div>
          </template>
          <template v-else-if="wizardStep === 2">
            <span class="wizard-step-label">02 · 行程节奏</span>
            <h3>你喜欢怎样的节奏？</h3>
            <p class="wizard-hint">景点数量、转场和休息时间会跟着变化。</p>
            <div class="pace-options">
              <button v-for="option in paceOptions" :key="option.value" :class="{ selected: formData.travel_pace === option.value }" :aria-pressed="formData.travel_pace === option.value" @click="formData.travel_pace = option.value">
                <strong>{{ option.label }}</strong><small>{{ option.detail }}</small>
              </button>
            </div>
          </template>
          <template v-else>
            <span class="wizard-step-label">03 · 关注重点</span>
            <h3>有什么想优先考虑？</h3>
            <p class="wizard-hint">可多选，也可以在左侧补充自己的要求。</p>
            <div class="focus-options">
              <button v-for="option in focusOptions" :key="option" :class="{ selected: selectedFocuses.includes(option) }" :aria-pressed="selectedFocuses.includes(option)" @click="toggleFocus(option)">
                {{ option }}
              </button>
            </div>
          </template>
          <div class="wizard-actions">
            <a-button v-if="wizardStep > 1" @click="wizardStep--">上一步</a-button>
            <a-button type="primary" @click="advanceWizard">{{ wizardStep === 3 ? '完成偏好设置' : '继续' }}</a-button>
          </div>
        </div>

        <div v-else class="wizard-summary">
          <div class="summary-title"><span><CheckOutlined /></span><div><strong>偏好已整理</strong><small>这些条件将用于生成你的行程</small></div></div>
          <dl>
            <div><dt>同行人群</dt><dd>{{ formData.traveler_type || '未选择' }}</dd></div>
            <div><dt>行程节奏</dt><dd>{{ formData.travel_pace || '未选择' }}</dd></div>
            <div><dt>关注重点</dt><dd>{{ selectedFocuses.length ? selectedFocuses.join('、') : '暂无特别要求' }}</dd></div>
          </dl>
          <a-button block @click="wizardComplete = false; wizardStep = 1">修改偏好</a-button>
        </div>
      </aside>
      </div>
    </div>

    <div class="workflow-section">
      <div class="workflow-heading">
        <div>
          <span class="workflow-eyebrow">PLANNING FLOW</span>
          <h2>一份行程，四步协同完成</h2>
        </div>
        <span class="workflow-count">04 <small>AGENTS</small></span>
      </div>
      <div class="workflow-track">
        <div v-for="stage in agentStages" :key="stage.number" class="workflow-stage" :class="`tone-${stage.tone}`">
          <div class="workflow-stage-top">
            <span class="workflow-icon">
              <img v-if="stage.image" :src="stage.image" :alt="stage.imageAlt" />
              <i v-else-if="stage.symbol === 'sun'" class="weather-sun-icon" aria-hidden="true">☀</i>
              <span v-else-if="stage.symbol === 'hotel'" class="hotel-symbol" aria-hidden="true">🏨</span>
              <component v-else :is="stage.icon" />
            </span>
          </div>
          <div class="workflow-stage-label"><span class="workflow-number">{{ stage.number }}</span><strong>{{ stage.title }}</strong></div>
          <small>{{ stage.output }}</small>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import {
  EditOutlined,
  EnvironmentOutlined,
  BookOutlined,
  PictureOutlined,
  CoffeeOutlined,
  ShoppingOutlined,
  SmileOutlined,
  CarOutlined,
  RocketOutlined,
  CheckOutlined,
  WalletOutlined,
} from '@ant-design/icons-vue';
import { TripPlannerAPI } from '@/services';
import type { TripPlanRequest } from '@/types';

const router = useRouter();
const loading = ref(false);
const loadingProgress = ref(0);
const loadingStatus = ref('');
const wizardStep = ref(1);
const wizardComplete = ref(false);
const selectedFocuses = ref<string[]>([]);
const travelerOptions = [
  { value: '独自旅行', label: '独自旅行', detail: '自由探索与弹性安排', icon: '🧭' },
  { value: '伴侣或朋友同行', label: '伴侣 / 朋友', detail: '兼顾体验与社交', icon: '👥' },
  { value: '带老人出行', label: '带老人', detail: '减少步行，增加休息', icon: '🧓' },
  { value: '亲子家庭出行', label: '亲子家庭', detail: '互动体验与便利优先', icon: '👨‍👩‍👧' },
];
const paceOptions = [
  { value: '轻松慢游', label: '轻松慢游', detail: '每天少量重点，留出午休' },
  { value: '适中', label: '松紧适中', detail: '景点与休息时间平衡' },
  { value: '紧凑充实', label: '紧凑充实', detail: '提高游览密度，多看一些' },
];
const focusOptions = ['少爬山 / 少步行', '本地美食', '夜景夜市', '亲子互动', '午休留白', '无障碍优先'];
const agentStages = [
  { number: '01', title: '景点研究', output: '地点 · 坐标 · 门票', image: '/assets/amap-marker.png', imageAlt: '高德地图标记', tone: 'violet' },
  { number: '02', title: '天气判断', output: '逐日预报 · 室内备选', symbol: 'sun', tone: 'blue' },
  { number: '03', title: '住宿建议', output: '区域匹配 · 预算约束', symbol: 'hotel', tone: 'cyan' },
  { number: '04', title: '路线统筹', output: '游览顺序 · 交通衔接', icon: CheckOutlined, tone: 'purple' },
];

const advisorMessage = computed(() => {
  if (wizardComplete.value) return '偏好已经收好，接下来我会把它们融进每天的路线。';
  if (wizardStep.value === 1) {
    return formData.value.traveler_type
      ? `收到，这次是${formData.value.traveler_type}，我会照顾好大家的出行节奏。`
      : '先告诉我这次和谁同行，我会按大家的体力安排路线。';
  }
  if (wizardStep.value === 2) {
    return formData.value.travel_pace
      ? `记下了，${formData.value.travel_pace}的节奏会决定每天安排多少内容。`
      : '选一个你喜欢的节奏，景点密度和休息时间就有方向了。';
  }
  return selectedFocuses.value.length
    ? `已经记下 ${selectedFocuses.value.length} 个关注点，路线会更贴合你的想法。`
    : '挑几项你在意的细节，让这趟旅程更合心意。';
});

const advisorMood = computed(() => {
  if (wizardComplete.value) return '✓';
  return ['👋', '🚶', '✨'][wizardStep.value - 1] || '👋';
});

const formData = ref<TripPlanRequest>({
  city: '',
  start_date: '',
  end_date: '',
  days: 3,
  preferences: '历史文化',
  budget: 3000,
  transportation: '公共交通',
  accommodation: '经济型',
  special_requirements: '',
  traveler_type: '',
  travel_pace: '',
});

const toggleFocus = (focus: string) => {
  selectedFocuses.value = selectedFocuses.value.includes(focus)
    ? selectedFocuses.value.filter(item => item !== focus)
    : [...selectedFocuses.value, focus];
};

const advanceWizard = () => {
  if (wizardStep.value === 1 && !formData.value.traveler_type) {
    message.info('先选择同行人群');
    return;
  }
  if (wizardStep.value === 2 && !formData.value.travel_pace) {
    message.info('先选择喜欢的行程节奏');
    return;
  }
  if (wizardStep.value < 3) {
    wizardStep.value++;
    return;
  }
  wizardComplete.value = true;
};

const openWizardStep = (step: number) => {
  wizardStep.value = step;
  wizardComplete.value = false;
};

const validateDates = async () => {
  if (!formData.value.start_date || !formData.value.end_date) {
    throw new Error('请选择开始和结束日期');
  }
  if (formData.value.end_date < formData.value.start_date) {
    throw new Error('结束日期不能早于开始日期');
  }
};

// 模拟加载进度
const simulateProgress = () => {
  const steps = [
    { progress: 20, status: '正在搜索景点信息...' },
    { progress: 40, status: '正在查询天气数据...' },
    { progress: 60, status: '正在推荐酒店住宿...' },
    { progress: 80, status: '正在生成旅行计划...' },
    { progress: 100, status: '计划生成完成！' },
  ];

  let currentStep = 0;
  const interval = setInterval(() => {
    if (currentStep < steps.length) {
      loadingProgress.value = steps[currentStep].progress;
      loadingStatus.value = steps[currentStep].status;
      currentStep++;
    } else {
      clearInterval(interval);
    }
  }, 2000);

  return interval;
};

// 提交表单
const handleSubmit = async () => {
  // 日期控件是两个独立字段，提交前再校验一次，避免浏览器自动填充绕过表单规则。
  if (!formData.value.start_date || !formData.value.end_date) {
    message.error('请选择开始和结束日期');
    return;
  }
  if (formData.value.end_date < formData.value.start_date) {
    message.error('结束日期不能早于开始日期');
    return;
  }
  loading.value = true;
  loadingProgress.value = 0;
  loadingStatus.value = '开始生成旅行计划...';

  const progressInterval = simulateProgress();

  try {
    const request = {
      ...formData.value,
      special_requirements: [formData.value.special_requirements, ...selectedFocuses.value].filter(Boolean).join('；'),
    };
    const response = await TripPlannerAPI.createTripPlan(request);

    clearInterval(progressInterval);

    if (response.error) {
      message.error(response.error);
    } else if (response.data) {
      message.success('旅行计划生成成功！');
      sessionStorage.setItem('trip-plan', JSON.stringify(response.data));
      localStorage.setItem('trip-plan', JSON.stringify(response.data));
      router.push({
        name: 'TripPlan',
      });
    }
  } catch (error) {
    clearInterval(progressInterval);
    message.error('生成旅行计划失败，请重试');
    console.error(error);
  } finally {
    loading.value = false;
  }
};

// 重置表单
const handleReset = () => {
  wizardStep.value = 1;
  wizardComplete.value = false;
  selectedFocuses.value = [];
  formData.value = {
    city: '',
    start_date: '',
    end_date: '',
    days: 3,
    preferences: '历史文化',
    budget: 3000,
    transportation: '公共交通',
    accommodation: '经济型',
    special_requirements: '',
    traveler_type: '',
    travel_pace: '',
  };
};
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #f5f6fb;
}

.hero-section {
  padding: 38px 24px 62px;
  background: #20294f;
  color: white;
}

.hero-content {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(280px, 0.62fr);
  align-items: center;
  gap: 34px;
  max-width: 1050px;
  margin: 0 auto;
}

.hero-copy { min-width: 0; }
.hero-advisor { display: flex; align-items: center; gap: 18px; min-width: 0; padding-left: 28px; border-left: 1px solid rgba(219, 224, 255, 0.24); }
.hero-advisor-portrait { position: relative; width: 144px; height: 144px; flex: 0 0 144px; overflow: hidden; border: 4px solid rgba(255, 255, 255, 0.92); border-radius: 24px; background: #fff; box-shadow: 0 14px 32px rgba(9, 14, 45, 0.34); animation: advisor-float 4s ease-in-out infinite; }
.hero-advisor-portrait img { display: block; width: 100%; height: 100%; object-fit: cover; }
.advisor-mood { position: absolute; right: 3px; bottom: 3px; display: grid; place-items: center; width: 25px; height: 25px; border: 2px solid #fff; border-radius: 50%; background: #8275e5; color: #fff; font-size: 13px; line-height: 1; }
.hero-advisor-message { min-width: 0; }
.advisor-presence { display: flex; align-items: center; gap: 8px; color: #fff; font-size: 14px; font-weight: 650; }
.advisor-presence span { width: 7px; height: 7px; border-radius: 50%; background: #62e0cc; box-shadow: 0 0 0 3px rgba(98, 224, 204, 0.14); }
.hero-advisor-message p { max-width: 220px; margin: 9px 0 0; color: #d5d9f0; font-size: 13px; line-height: 1.7; }
@keyframes advisor-float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }

.hero-kicker { display: flex; align-items: center; gap: 9px; color: #c5c8e1; font-size: 12px; font-weight: 650; }
.kicker-mark { width: 7px; height: 7px; border-radius: 2px; background: #a99afa; box-shadow: 0 0 0 4px rgba(169, 154, 250, 0.14); }

.hero-title {
  display: block;
  margin: 14px 0 6px;
  font-size: 38px;
  font-weight: 650;
  color: white;
}

.hero-subtitle {
  margin: 0;
  color: #e6e8f4;
  font-size: 16px;
}

.hero-capabilities { display: flex; gap: 9px; margin-top: 21px; color: #e0e4f7; font-size: 11px; }
.hero-capabilities span { display: flex; align-items: center; gap: 7px; padding: 7px 10px; border: 1px solid rgba(224, 228, 247, 0.18); border-radius: 4px; background: rgba(255, 255, 255, 0.045); }
.hero-capabilities :deep(.anticon) { color: #c9bdff; }
.amap-capability-icon { width: 14px; height: 19px; object-fit: contain; }
.weather-sun-icon { display: inline-block; border: 0; background: transparent; color: #f7bd3c; font-size: 20px; font-style: normal; line-height: 1; }
.hotel-symbol { display: inline-block; font-size: 14px; font-style: normal; line-height: 1; vertical-align: -1px; }

:deep(.ant-form-item-label > label) { color: #414968; font-weight: 550; }
:deep(.ant-input), :deep(.ant-input-number), :deep(.ant-select-selector), :deep(.ant-picker) { border-radius: 5px !important; }
:deep(.ant-radio-button-wrapper) { border-radius: 4px; }
:deep(.ant-btn-primary) { background: #596ee0; border-color: #596ee0; box-shadow: none; }
:deep(.ant-btn-primary:hover) { background: #495dc9; border-color: #495dc9; }
:deep(.ant-form-item) { margin-bottom: 18px; }

.requirements-field { width: 100%; }
.suggestion-row { display: flex; flex-wrap: wrap; align-items: center; gap: 7px; margin-top: 9px; }
.suggestion-row > span { margin-right: 2px; color: #7b8785; font-size: 11px; }
.suggestion-row :deep(.ant-btn) { height: 25px; padding: 0 9px; border-color: #e1e3ef; border-radius: 14px; color: #565e7d; font-size: 11px; }
.suggestion-row :deep(.ant-btn:hover) { border-color: #7869d8; color: #6252bd; }

.workflow-section { max-width: 1160px; margin: 0 auto; padding: 12px 24px 48px; }
.workflow-heading { display: flex; align-items: end; justify-content: space-between; padding-bottom: 18px; border-bottom: 1px solid #e2e5f0; }
.workflow-eyebrow { color: #7266cf; font-size: 10px; font-weight: 750; }
.workflow-heading h2 { margin: 5px 0 0; color: #303653; font-size: 21px; font-weight: 650; }
.workflow-count { display: flex; align-items: baseline; gap: 7px; color: #6458c7; font-size: 22px; font-weight: 700; }
.workflow-count small { color: #898da4; font-size: 9px; font-weight: 700; }
.workflow-track { position: relative; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0; padding-top: 24px; }
.workflow-track::before { position: absolute; top: 45px; right: 12.5%; left: 12.5%; height: 1px; background: #dfe2ef; content: ''; }
.workflow-stage { position: relative; z-index: 1; display: grid; justify-items: center; gap: 7px; min-width: 0; padding: 0 14px; text-align: center; }
.workflow-stage-top { display: flex; align-items: center; justify-content: center; width: 100%; margin-bottom: 4px; }
.workflow-icon { display: grid; place-items: center; width: 42px; height: 42px; border: 5px solid #f5f6fb; border-radius: 50%; color: #6157bd; background: #eae8ff; font-size: 16px; }
.workflow-icon img { display: block; width: 16px; height: 22px; object-fit: contain; }
.workflow-icon .weather-sun-icon { font-size: 22px; }
.workflow-icon .hotel-symbol { font-size: 20px; }
.workflow-number { color: #a2a6b9; font-size: 10px; font-weight: 700; }
.workflow-stage-label { display: flex; align-items: baseline; gap: 7px; }
.workflow-stage-label strong { color: #343956; font-size: 13px; font-weight: 650; }
.workflow-stage > small { color: #7c8199; font-size: 11px; line-height: 1.5; }
.tone-blue .workflow-icon { color: #406db8; background: #e5efff; }
.tone-cyan .workflow-icon { color: #318b9b; background: #e2f5f6; }
.tone-purple .workflow-icon { color: #7a5bb6; background: #f0e8ff; }

@media (max-width: 700px) {
  .hero-section { padding: 26px 18px 48px; }
  .hero-content { grid-template-columns: minmax(0, 1fr); gap: 20px; }
  .hero-advisor { gap: 12px; padding: 0; border-left: 0; }
  .hero-advisor-portrait { width: 70px; height: 70px; flex-basis: 70px; border-radius: 13px; }
  .hero-advisor-message p { max-width: 310px; margin-top: 4px; }
  .hero-title { font-size: 27px; }
  .hero-capabilities { flex-wrap: wrap; gap: 10px 16px; }
  .form-section { margin-top: -28px; }
  .form-section .planning-layout { grid-template-columns: minmax(0, 1fr); gap: 14px; }
  .form-section .assistant-panel { position: static; }
  .form-section :deep(.ant-form-item-label), .form-section :deep(.ant-form-item-control) { flex: 0 0 100%; max-width: 100%; }
  .form-section :deep(.ant-form-item-label) { padding: 0 0 5px; text-align: left; }
  .form-section :deep(.ant-form-item-control) { margin-left: 0; }
}

@media (prefers-reduced-motion: reduce) {
  .hero-advisor-portrait { animation: none; }
}

.form-section {
  max-width: 1200px;
  margin: -30px auto 28px;
  padding: 0 20px;
}

.planning-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.75fr) minmax(290px, 0.85fr);
  align-items: start;
  gap: 18px;
}

.form-card {
  min-width: 0;
  border: 1px solid #e2e5f0;
  border-radius: 7px;
  box-shadow: 0 10px 28px rgba(28, 55, 50, 0.08);
}

.assistant-panel { position: sticky; top: 18px; overflow: hidden; min-width: 0; border: 1px solid #e0e3f0; border-radius: 7px; background: #fff; box-shadow: 0 10px 28px rgba(43, 49, 91, 0.08); }
.assistant-header { display: flex; align-items: center; gap: 11px; padding: 16px; border-bottom: 1px solid #e8e9f2; background: #f8f8fd; }
.assistant-avatar { display: block; width: 52px; height: 52px; flex: 0 0 52px; border: 1px solid #dfe4f5; border-radius: 10px; background: #fff; object-fit: cover; }
.assistant-identity { display: grid; gap: 4px; }
.assistant-identity strong { color: #343956; font-size: 14px; }
.assistant-identity span { color: #7b7f98; font-size: 11px; }
.wizard-progress { display: flex; align-items: center; padding: 17px 20px 0; }
.wizard-progress button { display: flex; align-items: center; flex: 1; padding: 0; border: 0; background: transparent; cursor: pointer; }
.wizard-progress button:last-child { flex: 0 0 auto; }
.wizard-progress button span { display: grid; place-items: center; width: 25px; height: 25px; flex: 0 0 25px; border: 1px solid #d9dceb; border-radius: 50%; background: #fff; color: #7b7f98; font-size: 11px; }
.wizard-progress button i { height: 1px; flex: 1; margin: 0 8px; background: #e1e3ef; }
.wizard-progress button.current span { border-color: #665bd1; background: #665bd1; color: #fff; }
.wizard-progress button.complete span { border-color: #8f82df; background: #eeeaff; color: #5f51bf; }
.wizard-progress button.complete i { background: #bcb4ed; }
.wizard-body { padding: 17px 18px 18px; }
.wizard-step-label { color: #665bd1; font-size: 10px; font-weight: 700; letter-spacing: .6px; }
.wizard-body h3 { margin: 6px 0 4px; color: #303653; font-size: 17px; font-weight: 650; }
.wizard-hint { margin: 0 0 15px; color: #7d8298; font-size: 11px; line-height: 1.5; }
.wizard-options { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
.wizard-options button, .pace-options button { min-width: 0; padding: 10px; border: 1px solid #e1e3ef; border-radius: 5px; background: #fff; text-align: left; cursor: pointer; transition: border-color .15s, background .15s; }
.wizard-options button { display: grid; gap: 4px; }
.wizard-options strong, .pace-options strong { color: #444b6b; font-size: 12px; }
.wizard-options small, .pace-options small { color: #858aa0; font-size: 10px; line-height: 1.4; }
.wizard-options button.selected, .pace-options button.selected { border-color: #7668d8; background: #f5f3ff; box-shadow: inset 0 0 0 1px #7668d8; }
.pace-options { display: grid; gap: 8px; }
.pace-options button { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.pace-options small { text-align: right; }
.focus-options { display: flex; flex-wrap: wrap; gap: 8px; }
.focus-options button { padding: 7px 10px; border: 1px solid #e1e3ef; border-radius: 16px; background: #fff; color: #565e7d; font: inherit; font-size: 11px; cursor: pointer; }
.focus-options button.selected { border-color: #7668d8; background: #f1efff; color: #5e51bc; }
.wizard-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 18px; padding-top: 13px; border-top: 1px solid #ececf4; }
.wizard-actions :deep(.ant-btn) { height: 32px; border-radius: 5px; font-size: 12px; }
.wizard-summary { padding: 18px; }
.summary-title { display: flex; align-items: center; gap: 9px; }
.summary-title > span { display: grid; place-items: center; width: 27px; height: 27px; border-radius: 50%; background: #eeebff; color: #665bd1; }
.summary-title strong, .summary-title small { display: block; }
.summary-title strong { color: #343956; font-size: 13px; }
.summary-title small { margin-top: 3px; color: #7b7f98; font-size: 10px; }
.wizard-summary dl { display: grid; gap: 11px; margin: 18px 0; padding: 14px 0; border-top: 1px solid #ececf4; border-bottom: 1px solid #ececf4; }
.wizard-summary dl div { display: grid; grid-template-columns: 70px minmax(0, 1fr); gap: 8px; }
.wizard-summary dt { color: #81869d; font-size: 11px; }
.wizard-summary dd { margin: 0; color: #444b6b; font-size: 11px; font-weight: 600; overflow-wrap: anywhere; }
.wizard-summary :deep(.ant-btn) { border-radius: 5px; color: #5e58a6; }

.form-title {
  font-size: 20px;
  font-weight: 600;
}

</style>
