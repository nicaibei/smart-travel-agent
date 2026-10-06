/**
 * 旅行计划表单页面
 */
<template>
  <div class="trip-planner">
    <h1>智能旅行助手</h1>
    
    <!-- 表单区域 -->
    <div class="form-container">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>目的地城市：</label>
          <input 
            v-model="form.city" 
            type="text" 
            placeholder="例如: 北京"
            required 
          />
        </div>

        <div class="form-group">
          <label>开始日期：</label>
          <input 
            v-model="form.start_date" 
            type="date" 
            required 
          />
        </div>

        <div class="form-group">
          <label>结束日期：</label>
          <input 
            v-model="form.end_date" 
            type="date" 
            required 
          />
        </div>

        <div class="form-group">
          <label>旅行天数：</label>
          <input 
            v-model.number="form.days" 
            type="number" 
            min="1" 
            max="30"
            required 
          />
        </div>

        <div class="form-group">
          <label>旅行偏好：</label>
          <input 
            v-model="form.preferences" 
            type="text" 
            placeholder="例如: 历史文化, 自然风光"
          />
        </div>

        <div class="form-group">
          <label>预算（元）：</label>
          <input 
            v-model.number="form.budget" 
            type="number" 
            min="0"
            placeholder="例如: 3000"
          />
        </div>

        <div class="form-group">
          <label>交通方式：</label>
          <select v-model="form.transportation">
            <option value="公共交通">公共交通</option>
            <option value="自驾">自驾</option>
            <option value="出租车/网约车">出租车/网约车</option>
          </select>
        </div>

        <div class="form-group">
          <label>住宿类型：</label>
          <select v-model="form.accommodation">
            <option value="经济型">经济型</option>
            <option value="舒适型">舒适型</option>
            <option value="豪华型">豪华型</option>
          </select>
        </div>

        <button 
          type="submit" 
          :disabled="loading"
          class="submit-btn"
        >
          {{ loading ? '生成中...' : '生成旅行计划' }}
        </button>
      </form>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>正在生成旅行计划，请稍候...</p>
    </div>

    <!-- 错误信息 -->
    <div v-if="error" class="error">
      <p>❌ {{ error }}</p>
      <button @click="error = null">关闭</button>
    </div>

    <!-- 结果展示 -->
    <div v-if="tripPlan" class="result">
      <h2>{{ tripPlan.city }} 旅行计划</h2>
      
      <div class="plan-overview">
        <p><strong>日期：</strong>{{ tripPlan.start_date }} 至 {{ tripPlan.end_date }}</p>
        <p><strong>天数：</strong>{{ tripPlan.days.length }} 天</p>
      </div>

      <!-- 天气信息 -->
      <div v-if="tripPlan.weather_info && tripPlan.weather_info.length" class="weather-section">
        <h3>天气预报</h3>
        <div class="weather-list">
          <div 
            v-for="weather in tripPlan.weather_info" 
            :key="weather.date"
            class="weather-item"
          >
            <div>{{ weather.date }}</div>
            <div>🌤️ {{ weather.day_weather }}</div>
            <div>🌡️ {{ weather.day_temp }}°C / {{ weather.night_temp }}°C</div>
          </div>
        </div>
      </div>

      <!-- 每日行程 -->
      <div class="days-section">
        <h3>每日行程</h3>
        <div 
          v-for="(day, index) in tripPlan.days" 
          :key="index"
          class="day-plan"
        >
          <h4>第 {{ index + 1 }} 天 - {{ day.date }}</h4>
          <p class="day-description">{{ day.description }}</p>
          
          <!-- 景点列表 -->
          <div v-if="day.attractions && day.attractions.length" class="attractions">
            <h5>📍 景点安排</h5>
            <div 
              v-for="(attraction, idx) in day.attractions" 
              :key="idx"
              class="attraction-item"
            >
              <img 
                v-if="attraction.image_url" 
                :src="attraction.image_url" 
                :alt="attraction.name"
                class="attraction-image"
              />
              <div v-else class="attraction-image image-placeholder">暂无景点实拍图</div>
              <div class="attraction-info">
                <h6>{{ attraction.name }}</h6>
                <p>📍 {{ attraction.address }}</p>
                <p>{{ attraction.description }}</p>
                <p>⏱️ 建议游览时间: {{ attraction.visit_duration }} 分钟</p>
                <p v-if="attraction.ticket_price">
                  💰 门票: ¥{{ attraction.ticket_price }}
                </p>
              </div>
            </div>
          </div>

          <!-- 餐饮安排 -->
          <div v-if="day.meals && day.meals.length" class="meals">
            <h5>🍽️ 餐饮安排</h5>
            <div 
              v-for="(meal, idx) in day.meals" 
              :key="idx"
              class="meal-item"
            >
              <span class="meal-type">{{ getMealTypeLabel(meal.type) }}</span>
              <span class="meal-name">{{ meal.name }}</span>
              <span v-if="meal.estimated_cost" class="meal-cost">
                ¥{{ meal.estimated_cost }}
              </span>
            </div>
          </div>

          <!-- 住宿信息 -->
          <div v-if="day.hotel" class="hotel">
            <h5>🏨 住宿安排</h5>
            <div class="hotel-info">
              <p><strong>{{ day.hotel.name }}</strong></p>
              <p>📍 {{ day.hotel.address }}</p>
              <p v-if="day.hotel.estimated_cost">
                💰 预估费用: ¥{{ day.hotel.estimated_cost }} / 晚
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- 预算汇总 -->
      <div v-if="tripPlan.budget" class="budget-section">
        <h3>💰 预算汇总</h3>
        <div class="budget-details">
          <p>景点门票: ¥{{ tripPlan.budget.total_attractions }}</p>
          <p>酒店住宿: ¥{{ tripPlan.budget.total_hotels }}</p>
          <p>餐饮费用: ¥{{ tripPlan.budget.total_meals }}</p>
          <p>交通费用: ¥{{ tripPlan.budget.total_transportation }}</p>
          <p class="total">总计: ¥{{ tripPlan.budget.total }}</p>
        </div>
      </div>

      <!-- 总体建议 -->
      <div class="suggestions-section">
        <h3>💡 旅行建议</h3>
        <p>{{ tripPlan.overall_suggestions }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { TripPlan, TripPlanRequest } from '@/types';
import { TripPlannerAPI } from '@/services';

// 表单数据
const form = ref<TripPlanRequest>({
  city: '',
  start_date: '',
  end_date: '',
  days: 3,
  preferences: '',
  budget: 3000,
  transportation: '公共交通',
  accommodation: '经济型',
});

// 状态
const loading = ref(false);
const error = ref<string | null>(null);
const tripPlan = ref<TripPlan | null>(null);

// 提交表单
const handleSubmit = async () => {
  loading.value = true;
  error.value = null;
  tripPlan.value = null;

  try {
    const response = await TripPlannerAPI.createTripPlan(form.value);

    if (response.error) {
      error.value = response.error;
    } else if (response.data) {
      tripPlan.value = response.data;
    }
  } catch (err) {
    error.value = '生成旅行计划失败，请重试';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

// 获取餐饮类型标签
const getMealTypeLabel = (type: string): string => {
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
.trip-planner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.form-container {
  background: #f9f9f9;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
}

.submit-btn:hover:not(:disabled) {
  background: #45a049;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 40px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  background: #ffebee;
  color: #c62828;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.result {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.day-plan {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.attraction-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: white;
  border-radius: 4px;
  margin-bottom: 10px;
}

.attraction-image {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
}

.budget-details .total {
  font-size: 18px;
  font-weight: bold;
  color: #4CAF50;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 2px solid #ddd;
}
</style>
