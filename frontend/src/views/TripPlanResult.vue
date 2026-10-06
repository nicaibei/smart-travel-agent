<template>
  <div class="trip-plan-page">
    <a-page-header
      title="旅行计划"
      :sub-title="`${tripPlan.city} · ${tripPlan.days.length}天`"
      @back="handleBack"
    >
      <template #extra>
        <a-button @click="handleExport">
          <template #icon>
            <DownloadOutlined />
          </template>
          导出PDF
        </a-button>
        <a-button type="primary" @click="handleShare">
          <template #icon>
            <ShareAltOutlined />
          </template>
          分享
        </a-button>
      </template>
    </a-page-header>

    <div id="trip-plan-content" class="plan-content">
      <section class="trip-overview">
        <div>
          <span class="eyebrow">YOUR ITINERARY</span>
          <h1>{{ tripPlan.city }}旅行计划</h1>
          <p>{{ tripPlan.start_date }} 至 {{ tripPlan.end_date }} · {{ tripPlan.days.length }} 天</p>
        </div>
        <div class="overview-metrics">
          <div><strong>{{ totalAttractions }}</strong><span>个景点</span></div>
          <div v-if="tripPlan.budget"><strong>¥{{ tripPlan.budget.total }}</strong><span>预计花费</span></div>
          <div v-if="tripPlan.budget?.planned_budget"><strong>¥{{ tripPlan.budget.remaining }}</strong><span>预算结余</span></div>
        </div>
      </section>

      <section class="itinerary-section">
        <div class="section-heading">
          <div><span class="eyebrow">DAY BY DAY</span><h2>每日安排</h2></div>
          <div class="day-controls">
            <a-button aria-label="前一天" :disabled="selectedDayIndex <= 0" @click="selectedDayIndex--">‹</a-button>
            <a-button aria-label="后一天" :disabled="selectedDayIndex >= tripPlan.days.length - 1" @click="selectedDayIndex++">›</a-button>
          </div>
        </div>

        <nav class="day-switcher" aria-label="选择出行日期">
          <button
            v-for="(day, index) in tripPlan.days"
            :key="day.date"
            class="day-tab"
            :class="{ active: selectedDayIndex === index }"
            :aria-pressed="selectedDayIndex === index"
            @click="selectedDayIndex = index"
          >
            <span>DAY {{ String(index + 1).padStart(2, '0') }}</span>
            <strong>{{ formatShortDate(day.date) }}</strong>
            <small>{{ day.attractions?.length || 0 }} 个安排</small>
          </button>
        </nav>

        <article v-if="activeDay" class="day-panel">
          <div class="day-intro">
            <div><span class="eyebrow">{{ activeDay.date }}</span><h3>第 {{ selectedDayIndex + 1 }} 天</h3></div>
            <p>{{ activeDay.description }}</p>
          </div>
          <div class="route-summary">
            <div class="route-summary-heading"><span class="route-summary-icon">↗</span><div><strong>今日路线概览</strong><small>按推荐顺序串联主要停留点，实际可根据现场情况调整</small></div></div>
            <div class="route-flow">
              <template v-for="(step, index) in routeSummary(activeDay)" :key="`${step.label}-${index}`">
                <span class="route-step" :class="`route-${step.kind}`"><b>{{ step.icon }}</b>{{ step.label }}</span>
                <span v-if="index < routeSummary(activeDay).length - 1" class="route-arrow">→</span>
              </template>
            </div>
          </div>
          <a-row :gutter="24">
            <a-col :xs="24" :lg="16">
              <div class="schedule-list">
                <div v-for="(item, itemIndex) in activeDay.attractions" :key="`${item.name}-${itemIndex}`" class="schedule-item">
                  <div class="schedule-time"><span>{{ scheduleTime(itemIndex) }}</span><i /></div>
                  <div class="attraction-card">
                    <img v-if="item.image_url" :src="item.image_url" :alt="item.name" class="attraction-image" />
                    <div v-else class="attraction-image image-placeholder" aria-label="暂无景点实拍图"><span>暂无景点实拍图</span></div>
                    <div class="attraction-copy">
                      <div class="attraction-title"><span class="sequence">{{ String(itemIndex + 1).padStart(2, '0') }}</span><h4>{{ item.name }}</h4><button class="wish-button" :class="{ active: annotationFor(activeDay.date, item.name).wish }" type="button" :aria-label="annotationFor(activeDay.date, item.name).wish ? '取消想去' : '标记想去'" @click="toggleWish(activeDay.date, item.name)">{{ annotationFor(activeDay.date, item.name).wish ? '★' : '☆' }}</button></div>
                      <p>{{ item.description }}</p>
                      <div class="attraction-meta"><span><EnvironmentOutlined /> {{ item.address }}</span><span><ClockCircleOutlined /> {{ item.visit_duration }} 分钟</span><span v-if="item.ticket_price"><DollarOutlined /> ¥{{ item.ticket_price }}</span></div>
                      <div class="attraction-notes">
                        <input v-model="annotationFor(activeDay.date, item.name).tag" class="tag-input" placeholder="添加标签，如：亲子 / 必去" @change="saveAnnotations" />
                        <textarea v-model="annotationFor(activeDay.date, item.name).note" rows="1" placeholder="写下你的备注或想法..." @change="saveAnnotations" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </a-col>
            <a-col :xs="24" :lg="8">
              <aside class="day-sidebar">
                <div class="side-block">
                  <h4><CoffeeOutlined /> 用餐建议</h4>
                  <div v-for="meal in activeDay.meals" :key="`${meal.type}-${meal.name}`" class="meal-row">
                    <a-tag :color="getMealColor(meal.type)">{{ getMealLabel(meal.type) }}</a-tag>
                    <div><strong>{{ meal.name }}</strong><small>{{ meal.description || meal.address }}</small></div>
                    <b v-if="meal.estimated_cost">¥{{ meal.estimated_cost }}</b>
                  </div>
                </div>
                <div class="side-block">
                  <h4><CarOutlined /> 当日信息</h4>
                  <p><span>交通</span><strong>{{ activeDay.transportation }}</strong></p>
                  <p><span>住宿</span><strong>{{ activeDay.accommodation }}</strong></p>
                  <p v-if="activeWeather"><span>天气</span><strong>{{ activeWeather.day_weather }} · {{ activeWeather.day_temp }}° / {{ activeWeather.night_temp }}°</strong></p>
                </div>
                <div v-if="activeDay.hotel" class="side-block hotel-block">
                  <h4><HomeOutlined /> 住宿推荐</h4>
                  <strong>{{ activeDay.hotel.name }}</strong>
                  <small>{{ activeDay.hotel.address }}</small>
                  <small v-if="activeDay.hotel.price_range">{{ activeDay.hotel.price_range }}</small>
                </div>
              </aside>
            </a-col>
          </a-row>
        </article>
      </section>

      <TripMap :trip-plan="tripPlan" />

      <a-card v-if="tripPlan.weather_info?.length" title="天气预报" :bordered="false" class="weather-card">
        <a-row :gutter="16">
          <a-col v-for="weather in tripPlan.weather_info" :key="weather.date" :xs="12" :md="8" :lg="6">
            <div class="weather-item">
              <div class="weather-date">{{ weather.date }}</div>
              <div class="weather-desc">{{ weather.day_weather }} / {{ weather.night_weather }}</div>
              <div class="weather-temp">{{ weather.day_temp }}°C / {{ weather.night_temp }}°C</div>
            </div>
          </a-col>
        </a-row>
      </a-card>

      <!-- 预算明细 -->
      <a-card v-if="tripPlan.budget" title="预算明细" :bordered="false">
        <a-row :gutter="16">
          <a-col :span="6">
            <a-statistic
              title="景点门票"
              :value="tripPlan.budget.total_attractions"
              prefix="¥"
            />
          </a-col>
          <a-col :span="6">
            <a-statistic
              title="酒店住宿"
              :value="tripPlan.budget.total_hotels"
              prefix="¥"
            />
          </a-col>
          <a-col :span="6">
            <a-statistic
              title="餐饮费用"
              :value="tripPlan.budget.total_meals"
              prefix="¥"
            />
          </a-col>
          <a-col :span="6">
            <a-statistic
              title="交通费用"
              :value="tripPlan.budget.total_transportation"
              prefix="¥"
            />
          </a-col>
        </a-row>
        <a-divider />
        <a-statistic
          title="总计"
          :value="tripPlan.budget.total"
          prefix="¥"
          :value-style="{ color: '#3f8600', fontSize: '32px' }"
        />
        <a-alert
          v-if="tripPlan.budget.planned_budget"
          class="budget-note"
          type="info"
          :message="`已按 ¥${tripPlan.budget.planned_budget} 预算规划，预计使用 ¥${tripPlan.budget.total}，预留 ¥${tripPlan.budget.remaining} 机动金`"
          show-icon
        />
      </a-card>

      <!-- 旅行建议 -->
      <a-card title="旅行建议" :bordered="false">
        <a-alert :message="tripPlan.overall_suggestions" type="info" show-icon />
      </a-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { exportPDFWithPreparation } from '@/utils/exportUtils';
import TripMap from '@/components/TripMap.vue';
import {
  DownloadOutlined,
  ShareAltOutlined,
  EnvironmentOutlined,
  DollarOutlined,
  ClockCircleOutlined,
  CoffeeOutlined,
  HomeOutlined,
  CarOutlined,
} from '@ant-design/icons-vue';
import type { TripPlan } from '@/types';

const router = useRouter();
const selectedDayIndex = ref(0);
type AttractionAnnotation = { wish: boolean; tag: string; note: string };
const annotationStorageKey = 'trip-attraction-annotations';
const annotations = ref<Record<string, AttractionAnnotation>>({});
try {
  annotations.value = JSON.parse(localStorage.getItem(annotationStorageKey) || '{}');
} catch {
  annotations.value = {};
}

const annotationKey = (date: string, name: string) => `${date}|${name}`;
const annotationFor = (date: string, name: string): AttractionAnnotation => {
  const key = annotationKey(date, name);
  if (!annotations.value[key]) {
    annotations.value[key] = { wish: false, tag: '', note: '' };
  }
  return annotations.value[key];
};
const saveAnnotations = () => {
  localStorage.setItem(annotationStorageKey, JSON.stringify(annotations.value));
};
const toggleWish = (date: string, name: string) => {
  const annotation = annotationFor(date, name);
  annotation.wish = !annotation.wish;
  saveAnnotations();
  message.success(annotation.wish ? `已标记“${name}”为想去` : `已取消“${name}”标记`);
};
// 从路由参数获取旅行计划
const tripPlan = computed<TripPlan>(() => {
  try {
    const stored = sessionStorage.getItem('trip-plan') || localStorage.getItem('trip-plan');
    return stored ? JSON.parse(stored) : {
      city: '', start_date: '', end_date: '', days: [], weather_info: [], overall_suggestions: ''
    };
  } catch {
    return {} as TripPlan;
  }
});

// 计算总景点数
const totalAttractions = computed(() => {
  return tripPlan.value.days?.reduce((sum, day) => {
    return sum + (day.attractions?.length || 0);
  }, 0) || 0;
});

const activeDay = computed(() => tripPlan.value.days?.[selectedDayIndex.value]);
const activeWeather = computed(() => tripPlan.value.weather_info?.find(item => item.date === activeDay.value?.date));
const formatShortDate = (date: string) => date.slice(5).replace('-', '/');
const scheduleTime = (index: number) => ['09:00', '13:30', '16:30', '19:00'][index] || '弹性安排';
type RouteStep = { label: string; kind: 'start' | 'attraction' | 'meal' | 'hotel'; icon: string };
const routeSummary = (day: NonNullable<TripPlan['days']>[number]): RouteStep[] => {
  const steps: RouteStep[] = [{ label: '住宿出发', kind: 'start', icon: '出' }];
  day.attractions?.forEach((attraction) => {
    steps.push({ label: attraction.name, kind: 'attraction', icon: '景' });
  });
  const meal = day.meals?.find(item => item.type === 'dinner') || day.meals?.find(item => item.type === 'lunch');
  if (meal) steps.push({ label: meal.name, kind: 'meal', icon: '餐' });
  if (day.hotel?.name || day.accommodation) {
    steps.push({ label: day.hotel?.name || day.accommodation, kind: 'hotel', icon: '住' });
  }
  return steps;
};

// 返回首页
const handleBack = () => {
  router.push('/');
};

// 导出PDF
const handleExport = () => {
  void exportPDFWithPreparation('trip-plan-content', tripPlan.value);
};

// 分享
const handleShare = () => {
  const url = window.location.href;
  if (navigator.share) {
    void navigator.share({ title: `${tripPlan.value.city}旅行计划`, url });
  } else if (navigator.clipboard) {
    void navigator.clipboard.writeText(url).then(() => message.success('分享链接已复制'));
  } else {
    message.info('请复制当前页面地址分享');
  }
};

// 餐饮类型颜色
const getMealColor = (type: string) => {
  const colors: Record<string, string> = {
    breakfast: 'orange',
    lunch: 'green',
    dinner: 'blue',
    snack: 'purple',
  };
  return colors[type] || 'default';
};

// 餐饮类型标签
const getMealLabel = (type: string) => {
  const labels: Record<string, string> = {
    breakfast: '早餐',
    lunch: '午餐',
    dinner: '晚餐',
    snack: '小吃',
  };
  return labels[type] || type;
};
</script>

<style scoped>
.trip-plan-page {
  min-height: 100vh;
  background: #f4f6f7;
}

.plan-content {
  max-width: 1320px;
  margin: 0 auto;
  padding: 8px 28px 48px;
}

.trip-overview {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  padding: 22px 0 26px;
  border-bottom: 1px solid #dfe4e6;
}

.eyebrow { color: #168477; font-size: 11px; font-weight: 700; letter-spacing: 1px; }
.trip-overview h1, .section-heading h2, .day-intro h3 { margin: 5px 0; color: #1d2c2b; font-weight: 650; }
.trip-overview h1 { font-size: 28px; }
.trip-overview p { margin: 0; color: #687573; }
.overview-metrics { display: flex; gap: 28px; }
.overview-metrics div { display: grid; gap: 3px; }
.overview-metrics strong { color: #233634; font-size: 20px; }
.overview-metrics span { color: #7b8785; font-size: 12px; }
.itinerary-section { padding: 24px 0 8px; }
.section-heading { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.section-heading h2 { font-size: 21px; }
.day-controls { display: flex; gap: 8px; }
.day-controls :deep(.ant-btn) { width: 34px; height: 34px; padding: 0; font-size: 21px; }
.day-switcher { display: flex; gap: 8px; overflow-x: auto; padding: 2px 0 12px; scrollbar-width: thin; }
.day-tab { flex: 0 0 148px; display: grid; gap: 4px; padding: 12px 14px; border: 1px solid #dce4e2; border-radius: 6px; background: #fff; color: #43514f; text-align: left; cursor: pointer; transition: border-color .15s, background .15s; }
.day-tab span { color: #75827f; font-size: 10px; font-weight: 700; }
.day-tab strong { font-size: 15px; }
.day-tab small { color: #7b8785; font-size: 11px; }
.day-tab.active { border-color: #168477; background: #e9f4f1; color: #126b61; }
.day-tab.active span, .day-tab.active small { color: #357f75; }
.day-panel { padding: 20px; border: 1px solid #e1e7e5; border-radius: 7px; background: #fff; }
.day-intro { display: flex; align-items: flex-start; justify-content: space-between; gap: 20px; padding-bottom: 18px; border-bottom: 1px solid #edf0ef; }
.day-intro h3 { font-size: 20px; }
.day-intro p { max-width: 700px; margin: 9px 0 0; color: #64716f; line-height: 1.7; }
.route-summary { margin: 18px 0 2px; padding: 14px 16px; border: 1px solid #dfeae6; border-radius: 6px; background: #f8fbfa; }
.route-summary-heading { display: flex; align-items: center; gap: 9px; color: #245e56; }
.route-summary-icon { display: grid; place-items: center; width: 24px; height: 24px; border-radius: 50%; background: #dcefe9; color: #168477; font-weight: 700; }
.route-summary-heading strong, .route-summary-heading small { display: block; }
.route-summary-heading strong { font-size: 13px; }
.route-summary-heading small { margin-top: 3px; color: #7a8985; font-size: 11px; font-weight: 400; }
.route-flow { display: flex; align-items: center; gap: 7px; margin-top: 13px; overflow-x: auto; padding-bottom: 2px; }
.route-step { display: inline-flex; align-items: center; gap: 5px; flex: 0 0 auto; max-width: 180px; padding: 6px 9px; border: 1px solid #dce7e3; border-radius: 4px; background: #fff; color: #42534f; font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.route-step b { display: inline-grid; place-items: center; width: 18px; height: 18px; border-radius: 50%; background: #e7f3f0; color: #168477; font-size: 10px; }
.route-meal b { background: #fff0d9; color: #bd7414; }
.route-hotel b { background: #e9e5fb; color: #6853a8; }
.route-arrow { flex: 0 0 auto; color: #9ba9a5; font-size: 15px; }
.schedule-list { padding-top: 18px; }
.schedule-item { display: grid; grid-template-columns: 78px minmax(0, 1fr); gap: 10px; }
.schedule-time { display: flex; flex-direction: column; align-items: center; color: #168477; font-size: 12px; font-weight: 700; }
.schedule-time i { width: 1px; flex: 1; min-height: 18px; margin-top: 7px; background: #d9e5e2; }
.schedule-item:last-child .schedule-time i { display: none; }
.attraction-card { display: grid; grid-template-columns: minmax(130px, 190px) minmax(0, 1fr); gap: 14px; padding: 0 0 20px; }
.attraction-image { width: 100%; height: 116px; border-radius: 5px; object-fit: cover; background: #edf1f0; }
.image-placeholder { display: grid; place-items: center; color: #899694; font-size: 12px; border: 1px dashed #cfd9d6; background: #f5f8f7; }
.attraction-copy { min-width: 0; }
.attraction-title { display: flex; align-items: center; gap: 9px; }
.attraction-title h4 { margin: 0; color: #253533; font-size: 16px; }
.wish-button { margin-left: auto; padding: 0 4px; border: 0; background: transparent; color: #9aa7a4; font-size: 22px; line-height: 1; cursor: pointer; }
.wish-button:hover, .wish-button.active { color: #f0a43a; }
.sequence { color: #168477; font-size: 11px; font-weight: 700; }
.attraction-copy p { margin: 7px 0; color: #63716f; font-size: 13px; line-height: 1.55; }
.attraction-meta { display: flex; flex-wrap: wrap; gap: 8px 14px; color: #7b8785; font-size: 11px; }
.attraction-notes { display: grid; grid-template-columns: 150px minmax(0, 1fr); gap: 8px; margin-top: 10px; }
.attraction-notes input, .attraction-notes textarea { width: 100%; box-sizing: border-box; border: 1px solid #e0e8e5; border-radius: 4px; background: #fbfdfc; color: #40504c; font: inherit; font-size: 12px; padding: 7px 8px; outline: none; resize: vertical; }
.attraction-notes input:focus, .attraction-notes textarea:focus { border-color: #168477; box-shadow: 0 0 0 2px rgba(22, 132, 119, .1); }
.day-sidebar { display: grid; gap: 12px; padding-top: 18px; }
.side-block { padding: 14px; border: 1px solid #e7ecea; border-radius: 5px; background: #fbfcfc; }
.side-block h4 { display: flex; align-items: center; gap: 8px; margin: 0 0 12px; color: #334440; font-size: 14px; }
.meal-row { display: grid; grid-template-columns: auto minmax(0, 1fr) auto; align-items: start; gap: 8px; padding: 8px 0; border-top: 1px solid #edf0ef; }
.meal-row:first-of-type { border-top: 0; }
.meal-row strong, .meal-row small, .hotel-block strong, .hotel-block small { display: block; }
.meal-row strong, .hotel-block strong { color: #394744; font-size: 12px; }
.meal-row small, .hotel-block small { margin-top: 3px; color: #7b8785; font-size: 11px; line-height: 1.45; }
.meal-row b { color: #596764; font-size: 11px; white-space: nowrap; }
.side-block > p { display: flex; justify-content: space-between; gap: 12px; margin: 8px 0 0; font-size: 12px; }
.side-block > p span { color: #7b8785; }
.side-block > p strong { color: #394744; text-align: right; }
.weather-card { margin-top: 20px; }
:deep(.ant-page-header) { max-width: 1320px; margin: 0 auto; padding: 14px 28px; }
:deep(.ant-card) { border-radius: 6px; }
.weather-item {
  padding: 12px;
  border: 1px solid #e6ebea;
  border-radius: 5px;
  background: #fbfcfc;
}

.weather-date {
  font-weight: 500;
  margin-bottom: 8px;
}

.weather-desc { color: #596764; margin-bottom: 4px; }

.weather-temp {
  font-size: 16px;
  font-weight: 500;
  color: #1890ff;
}

.budget-note { margin-top: 16px; }

@media (max-width: 760px) {
  .plan-content { padding: 4px 16px 32px; }
  :deep(.ant-page-header) { padding: 10px 16px; }
  .trip-overview { display: block; }
  .overview-metrics { gap: 18px; margin-top: 18px; }
  .overview-metrics strong { font-size: 17px; }
  .day-panel { padding: 14px; }
  .day-intro { display: block; }
  .day-intro p { margin-top: 8px; }
  .route-summary { padding: 12px; }
  .route-flow { align-items: flex-start; flex-direction: column; gap: 5px; }
  .route-arrow { transform: rotate(90deg); margin-left: 8px; }
  .schedule-item { grid-template-columns: 58px minmax(0, 1fr); gap: 4px; }
  .attraction-card { grid-template-columns: 1fr; gap: 8px; }
  .attraction-image { height: 180px; }
  .attraction-notes { grid-template-columns: 1fr; }
  .day-sidebar { padding-top: 4px; }
}
</style>
