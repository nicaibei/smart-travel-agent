/**
 * 路由配置
 */
import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

// 路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: {
      title: '智能旅行助手 - 首页',
    },
  },
  {
    path: '/planner',
    name: 'TripPlanner',
    component: () => import('@/views/TripPlanner.vue'),
    meta: {
      title: '旅行规划',
    },
  },
  {
    path: '/plan',
    name: 'TripPlan',
    component: () => import('@/views/TripPlanResult.vue'),
    meta: {
      title: '旅行计划详情',
    },
  },
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// 路由守卫 - 设置页面标题
router.beforeEach((to, _from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title as string;
  }
  next();
});

export default router;
