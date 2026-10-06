<!--
  行程编辑功能示例 - 精简版
  可以直接集成到 TripPlanResult.vue 中
-->

<!-- ===================================
     模板部分 - 添加到现有组件
     =================================== -->

<!-- 1. 在页面头部添加编辑按钮 -->
<template>
  <div class="trip-plan-page">
    <a-page-header
      title="旅行计划"
      :sub-title="`${tripPlan.city} · ${tripPlan.days.length}天`"
      @back="handleBack"
    >
      <template #extra>
        <!-- 编辑模式切换 -->
        <a-button 
          v-if="!editMode" 
          type="primary" 
          @click="toggleEditMode"
        >
          <template #icon><EditOutlined /></template>
          编辑行程
        </a-button>
        
        <template v-else>
          <a-button type="primary" @click="saveChanges">
            <template #icon><SaveOutlined /></template>
            保存修改
          </a-button>
          <a-button @click="cancelEdit">
            <template #icon><CloseOutlined /></template>
            取消
          </a-button>
        </template>

        <a-button @click="handleExport">
          <template #icon><DownloadOutlined /></template>
          导出
        </a-button>
      </template>
    </a-page-header>

    <!-- 编辑模式提示 -->
    <a-alert
      v-if="editMode"
      message="编辑模式"
      description="您可以调整景点顺序、删除景点、修改信息"
      type="info"
      show-icon
      closable
      style="margin: 16px 24px;"
    />

    <!-- 2. 景点列表添加编辑功能 -->
    <div class="attractions-section">
      <h4><PushpinOutlined /> 景点安排</h4>
      
      <div
        v-for="(attraction, index) in day.attractions"
        :key="index"
        class="attraction-card"
        :class="{ 'edit-mode': editMode }"
      >
        <!-- 景点序号 -->
        <div class="attraction-index">{{ index + 1 }}</div>

        <!-- 景点内容 -->
        <div class="attraction-content">
          <h5>{{ attraction.name }}</h5>
          <p>{{ attraction.description }}</p>
          <div>⏱️ {{ attraction.visit_duration }} 分钟</div>
          <div>💰 ¥{{ attraction.ticket_price }}</div>
        </div>

        <!-- 编辑按钮组（仅编辑模式显示） -->
        <div v-if="editMode" class="edit-buttons">
          <!-- 上移 -->
          <a-tooltip title="上移">
            <a-button
              size="small"
              :disabled="index === 0"
              @click="handleMoveUp(dayIndex, index)"
            >
              <template #icon><ArrowUpOutlined /></template>
            </a-button>
          </a-tooltip>

          <!-- 下移 -->
          <a-tooltip title="下移">
            <a-button
              size="small"
              :disabled="index === day.attractions.length - 1"
              @click="handleMoveDown(dayIndex, index)"
            >
              <template #icon><ArrowDownOutlined /></template>
            </a-button>
          </a-tooltip>

          <!-- 删除 -->
          <a-popconfirm
            title="确定要删除这个景点吗？"
            ok-text="确定"
            cancel-text="取消"
            @confirm="handleDelete(dayIndex, index)"
          >
            <a-button size="small" danger>
              <template #icon><DeleteOutlined /></template>
            </a-button>
          </a-popconfirm>
        </div>
      </div>
    </div>
  </div>
</template>


<!-- ===================================
     Script部分 - 添加到现有组件的script
     =================================== -->

<script setup lang="ts">
import { ref } from 'vue';
import { message } from 'ant-design-vue';
import {
  EditOutlined,
  SaveOutlined,
  CloseOutlined,
  DownloadOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  DeleteOutlined,
  PushpinOutlined,
} from '@ant-design/icons-vue';
import type { TripPlan } from '@/types';

// 假设 tripPlan 是从路由或props获取的
const tripPlan = ref<TripPlan>({ /* ... */ });

// 编辑状态
const editMode = ref(false);
const originalPlan = ref<TripPlan | null>(null);

// 进入编辑模式
const toggleEditMode = () => {
  editMode.value = true;
  // 深拷贝保存原始数据
  originalPlan.value = JSON.parse(JSON.stringify(tripPlan.value));
  message.info('已进入编辑模式');
};

// 保存修改
const saveChanges = () => {
  editMode.value = false;
  originalPlan.value = null;
  message.success('修改已保存！');
  // 可以在这里调用API保存
};

// 取消编辑
const cancelEdit = () => {
  if (originalPlan.value) {
    // 恢复原始数据
    tripPlan.value = originalPlan.value;
  }
  editMode.value = false;
  message.info('已取消编辑');
};

// 上移景点
const handleMoveUp = (dayIndex: number, attractionIndex: number) => {
  const attractions = tripPlan.value.days[dayIndex].attractions;
  const newIndex = attractionIndex - 1;
  
  // ES6解构赋值交换元素
  [attractions[attractionIndex], attractions[newIndex]] = 
    [attractions[newIndex], attractions[attractionIndex]];
  
  message.success('景点已上移');
};

// 下移景点
const handleMoveDown = (dayIndex: number, attractionIndex: number) => {
  const attractions = tripPlan.value.days[dayIndex].attractions;
  const newIndex = attractionIndex + 1;
  
  [attractions[attractionIndex], attractions[newIndex]] = 
    [attractions[newIndex], attractions[attractionIndex]];
  
  message.success('景点已下移');
};

// 删除景点
const handleDelete = (dayIndex: number, attractionIndex: number) => {
  const attraction = tripPlan.value.days[dayIndex].attractions[attractionIndex];
  
  // 使用splice删除
  tripPlan.value.days[dayIndex].attractions.splice(attractionIndex, 1);
  
  message.success(`已删除景点: ${attraction.name}`);
  
  // 更新预算
  updateBudget();
};

// 更新预算
const updateBudget = () => {
  if (!tripPlan.value.budget) return;

  // 重新计算景点门票总额
  let attractionsTotal = 0;
  tripPlan.value.days.forEach(day => {
    day.attractions.forEach(attr => {
      attractionsTotal += attr.ticket_price || 0;
    });
  });
  
  tripPlan.value.budget.total_attractions = attractionsTotal;
  
  // 重新计算总额
  tripPlan.value.budget.total =
    tripPlan.value.budget.total_attractions +
    tripPlan.value.budget.total_hotels +
    tripPlan.value.budget.total_meals +
    tripPlan.value.budget.total_transportation;
};
</script>


<!-- ===================================
     样式部分 - 添加到现有组件的style
     =================================== -->

<style scoped>
.attraction-card {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: white;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  margin-bottom: 16px;
  transition: all 0.3s;
}

/* 编辑模式下高亮 */
.attraction-card.edit-mode {
  border-color: #1890ff;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.1);
}

.attraction-index {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #1890ff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.attraction-content {
  flex: 1;
}

.attraction-content h5 {
  margin: 0 0 8px 0;
  font-size: 16px;
}

/* 编辑按钮组 */
.edit-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex-shrink: 0;
}

/* 编辑按钮悬停效果 */
.edit-buttons button:hover {
  transform: scale(1.05);
}
</style>


<!-- ===================================
     完整集成示例
     =================================== -->

<!--
要将编辑功能集成到现有的 TripPlanResult.vue 中：

1. 导入必要的图标和工具函数
2. 添加 editMode 和 originalPlan 状态
3. 在页面头部添加编辑按钮
4. 在景点列表中添加编辑按钮（仅编辑模式显示）
5. 实现移动、删除等操作函数
6. 添加相应的CSS样式

关键代码位置：
- 按钮组：在 a-page-header 的 extra 插槽中
- 编辑UI：在每个景点的 attraction-card 中
- 状态管理：使用 ref 管理 editMode 和 originalPlan
- 深拷贝：JSON.parse(JSON.stringify(...))
- 数组交换：[a, b] = [b, a]
- 数组删除：splice(index, 1)
-->


<!-- ===================================
     使用说明
     =================================== -->

<!--
1. 复制上面的模板代码到 TripPlanResult.vue 对应位置
2. 确保导入了所有必要的图标组件
3. 添加 editMode 相关的状态管理代码
4. 实现各个操作函数（move, delete等）
5. 测试功能：进入编辑模式 → 调整景点 → 保存/取消

注意事项：
- 编辑模式使用深拷贝保存原始数据
- 取消时恢复原始数据
- 保存时可以调用API持久化
- 删除景点后记得更新预算
- 移动时检查边界（第一个不能上移，最后一个不能下移）
-->
