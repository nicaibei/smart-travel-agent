/**
 * API 服务 - 旅行计划相关
 */
import type { TripPlan, TripPlanRequest } from '@/types';

// API 基础URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * API 响应类型
 */
interface ApiResponse<T> {
  data?: T;
  error?: string;
}

/**
 * 旅行计划 API 服务
 */
export class TripPlannerAPI {
  /**
   * 创建旅行计划
   */
  static async createTripPlan(request: TripPlanRequest): Promise<ApiResponse<TripPlan>> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/trip/plan`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || '请求失败');
      }

      const data: TripPlan = await response.json();
      return { data };
    } catch (error) {
      console.error('创建旅行计划失败:', error);
      return {
        error: error instanceof Error ? error.message : '未知错误',
      };
    }
  }

  /**
   * 健康检查
   */
  static async healthCheck(): Promise<ApiResponse<any>> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/trip/health`);

      if (!response.ok) {
        throw new Error('健康检查失败');
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      console.error('健康检查失败:', error);
      return {
        error: error instanceof Error ? error.message : '未知错误',
      };
    }
  }

  /**
   * 获取根路径信息
   */
  static async getRoot(): Promise<ApiResponse<any>> {
    try {
      const response = await fetch(`${API_BASE_URL}/`);

      if (!response.ok) {
        throw new Error('获取根信息失败');
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      console.error('获取根信息失败:', error);
      return {
        error: error instanceof Error ? error.message : '未知错误',
      };
    }
  }
}

/**
 * 导出默认实例
 */
export default TripPlannerAPI;
