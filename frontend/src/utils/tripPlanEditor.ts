/**
 * 行程编辑功能 - 核心逻辑
 */

// ===================================
// 1. 状态管理
// ===================================

import { ref } from 'vue';
import { message } from 'ant-design-vue';
import type { TripPlan, Attraction, Meal } from '@/types';

// 编辑状态
const editMode = ref(false);
const originalPlan = ref<TripPlan | null>(null);

// 模态框状态
const editModalVisible = ref(false);
const editingAttraction = ref<Attraction>({} as Attraction);
const editingDayIndex = ref(0);
const editingAttractionIndex = ref(0);


// ===================================
// 2. 编辑模式切换
// ===================================

// 进入编辑模式
const toggleEditMode = (tripPlan: TripPlan) => {
  editMode.value = true;
  // 深拷贝保存原始计划（避免引用问题）
  originalPlan.value = JSON.parse(JSON.stringify(tripPlan));
  message.info('已进入编辑模式，可以调整景点顺序、删除景点或修改信息');
};

// 保存修改
const saveChanges = (tripPlan: TripPlan) => {
  void tripPlan;
  editMode.value = false;
  originalPlan.value = null;
  message.success('修改已保存！');
  
  // 可以在这里调用API保存到后端
  // await api.saveTripPlan(tripPlan);
};

// 取消编辑
const cancelEdit = (tripPlan: TripPlan) => {
  if (originalPlan.value) {
    // 恢复原始计划
    Object.assign(tripPlan, originalPlan.value);
    message.info('已取消编辑，恢复原始计划');
  }
  editMode.value = false;
  originalPlan.value = null;
};


// ===================================
// 3. 景点操作
// ===================================

// 移动景点（上移或下移）
const moveAttraction = (
  tripPlan: TripPlan,
  dayIndex: number,
  attractionIndex: number,
  direction: 'up' | 'down'
) => {
  const attractions = tripPlan.days[dayIndex].attractions;
  const newIndex = direction === 'up' ? attractionIndex - 1 : attractionIndex + 1;

  // 检查边界
  if (newIndex >= 0 && newIndex < attractions.length) {
    // ES6 解构赋值 - 优雅地交换数组元素
    [attractions[attractionIndex], attractions[newIndex]] = [
      attractions[newIndex],
      attractions[attractionIndex],
    ];
    
    const directionText = direction === 'up' ? '上移' : '下移';
    message.success(`景点已${directionText}`);
  }
};

// 删除景点
const deleteAttraction = (
  tripPlan: TripPlan,
  dayIndex: number,
  attractionIndex: number
) => {
  const attraction = tripPlan.days[dayIndex].attractions[attractionIndex];
  
  // 使用 splice 删除数组元素
  tripPlan.days[dayIndex].attractions.splice(attractionIndex, 1);
  
  message.success(`已删除景点: ${attraction.name}`);
  
  // 更新预算
  updateBudget(tripPlan);
};

// 添加景点
const addAttraction = (
  tripPlan: TripPlan,
  dayIndex: number,
  attraction: Attraction
) => {
  tripPlan.days[dayIndex].attractions.push(attraction);
  message.success(`已添加景点: ${attraction.name}`);
  
  // 更新预算
  updateBudget(tripPlan);
};

// 编辑景点信息
const updateAttraction = (
  tripPlan: TripPlan,
  dayIndex: number,
  attractionIndex: number,
  newData: Partial<Attraction>
) => {
  const attraction = tripPlan.days[dayIndex].attractions[attractionIndex];
  Object.assign(attraction, newData);
  message.success('景点信息已更新');
  
  // 更新预算
  updateBudget(tripPlan);
};


// ===================================
// 4. 餐饮操作
// ===================================

// 添加餐饮
const addMeal = (tripPlan: TripPlan, dayIndex: number, mealType: Meal['type'] = 'lunch') => {
  const newMeal: Meal = {
    type: mealType,
    name: '',
    address: '',
    description: '',
    estimated_cost: 0,
  };
  
  tripPlan.days[dayIndex].meals.push(newMeal);
  message.success('已添加餐饮项，请填写详细信息');
};

// 删除餐饮
const deleteMeal = (tripPlan: TripPlan, dayIndex: number, mealIndex: number) => {
  tripPlan.days[dayIndex].meals.splice(mealIndex, 1);
  message.success('已删除餐饮项');
  
  // 更新预算
  updateBudget(tripPlan);
};

// 更新餐饮信息
const updateMeal = (
  tripPlan: TripPlan,
  dayIndex: number,
  mealIndex: number,
  newData: Partial<Meal>
) => {
  const meal = tripPlan.days[dayIndex].meals[mealIndex];
  Object.assign(meal, newData);
  
  // 更新预算
  updateBudget(tripPlan);
};


// ===================================
// 5. 预算更新
// ===================================

const updateBudget = (tripPlan: TripPlan) => {
  if (!tripPlan.budget) {
    tripPlan.budget = {
      total_attractions: 0,
      total_hotels: 0,
      total_meals: 0,
      total_transportation: 0,
      total: 0,
    };
  }

  // 计算景点门票总额
  let attractionsTotal = 0;
  tripPlan.days.forEach(day => {
    day.attractions.forEach(attraction => {
      attractionsTotal += attraction.ticket_price || 0;
    });
  });
  tripPlan.budget.total_attractions = attractionsTotal;

  // 计算餐饮总额
  let mealsTotal = 0;
  tripPlan.days.forEach(day => {
    day.meals.forEach(meal => {
      mealsTotal += meal.estimated_cost || 0;
    });
  });
  tripPlan.budget.total_meals = mealsTotal;

  // 计算总额
  tripPlan.budget.total =
    tripPlan.budget.total_attractions +
    tripPlan.budget.total_hotels +
    tripPlan.budget.total_meals +
    tripPlan.budget.total_transportation;

  console.log('预算已更新:', tripPlan.budget);
};


// ===================================
// 6. 批量操作
// ===================================

// 批量删除景点
const batchDeleteAttractions = (
  tripPlan: TripPlan,
  deletions: Array<{ dayIndex: number; attractionIndex: number }>
) => {
  // 从后往前删除，避免索引变化问题
  deletions
    .sort((a, b) => b.attractionIndex - a.attractionIndex)
    .forEach(({ dayIndex, attractionIndex }) => {
      tripPlan.days[dayIndex].attractions.splice(attractionIndex, 1);
    });
  
  message.success(`已删除 ${deletions.length} 个景点`);
  updateBudget(tripPlan);
};

// 复制某天的行程到另一天
const copyDayPlan = (
  tripPlan: TripPlan,
  fromDayIndex: number,
  toDayIndex: number
) => {
  const fromDay = tripPlan.days[fromDayIndex];
  const toDay = tripPlan.days[toDayIndex];
  
  // 深拷贝景点和餐饮
  toDay.attractions = JSON.parse(JSON.stringify(fromDay.attractions));
  toDay.meals = JSON.parse(JSON.stringify(fromDay.meals));
  toDay.description = fromDay.description;
  
  message.success(`已复制第 ${fromDayIndex + 1} 天的行程到第 ${toDayIndex + 1} 天`);
};


// ===================================
// 7. 验证和检查
// ===================================

// 验证行程是否合理
const validatePlan = (tripPlan: TripPlan): { valid: boolean; errors: string[] } => {
  const errors: string[] = [];

  tripPlan.days.forEach((day, index) => {
    // 检查是否有景点
    if (day.attractions.length === 0) {
      errors.push(`第 ${index + 1} 天没有安排景点`);
    }

    // 检查是否有餐饮
    if (day.meals.length === 0) {
      errors.push(`第 ${index + 1} 天没有安排餐饮`);
    }

    // 检查游览时间是否合理（总时长不超过8小时）
    const totalDuration = day.attractions.reduce(
      (sum, attr) => sum + (attr.visit_duration || 0),
      0
    );
    if (totalDuration > 480) {
      errors.push(`第 ${index + 1} 天游览时间过长（${Math.round(totalDuration / 60)}小时），建议减少景点`);
    }
  });

  return {
    valid: errors.length === 0,
    errors,
  };
};


// ===================================
// 8. 导出功能
// ===================================

export {
  // 状态
  editMode,
  originalPlan,
  editModalVisible,
  editingAttraction,
  editingDayIndex,
  editingAttractionIndex,
  
  // 编辑模式
  toggleEditMode,
  saveChanges,
  cancelEdit,
  
  // 景点操作
  moveAttraction,
  deleteAttraction,
  addAttraction,
  updateAttraction,
  
  // 餐饮操作
  addMeal,
  deleteMeal,
  updateMeal,
  
  // 预算
  updateBudget,
  
  // 批量操作
  batchDeleteAttractions,
  copyDayPlan,
  
  // 验证
  validatePlan,
};


// ===================================
// 使用示例
// ===================================

/*
在组件中使用：

<script setup lang="ts">
import { ref } from 'vue';
import {
  editMode,
  toggleEditMode,
  saveChanges,
  cancelEdit,
  moveAttraction,
  deleteAttraction,
} from '@/utils/tripPlanEditor';

const tripPlan = ref<TripPlan>({ ... });

// 进入编辑模式
const handleEdit = () => {
  toggleEditMode(tripPlan.value);
};

// 保存修改
const handleSave = () => {
  saveChanges(tripPlan.value);
};

// 取消编辑
const handleCancel = () => {
  cancelEdit(tripPlan.value);
};

// 移动景点
const handleMoveAttraction = (dayIndex: number, attrIndex: number, direction: 'up' | 'down') => {
  moveAttraction(tripPlan.value, dayIndex, attrIndex, direction);
};
</script>
*/
