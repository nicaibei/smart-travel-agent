/**
 * 位置信息
 */
export interface Location {
  longitude: number;
  latitude: number;
}

/**
 * 景点信息
 */
export interface Attraction {
  name: string;
  address: string;
  location: Location;
  visit_duration: number;
  description: string;
  category?: string;
  rating?: number;
  image_url?: string;
  ticket_price: number;
}

/**
 * 餐饮信息
 */
export interface Meal {
  type: 'breakfast' | 'lunch' | 'dinner' | 'snack';
  name: string;
  address?: string;
  location?: Location;
  description?: string;
  estimated_cost: number;
}

/**
 * 酒店信息
 */
export interface Hotel {
  name: string;
  address: string;
  location?: Location;
  price_range: string;
  rating: string;
  distance: string;
  type: string;
  estimated_cost: number;
}

/**
 * 预算信息
 */
export interface Budget {
  total_attractions: number;
  total_hotels: number;
  total_meals: number;
  total_transportation: number;
  total: number;
  planned_budget?: number;
  remaining?: number;
}

/**
 * 单日行程
 */
export interface DayPlan {
  date: string;
  day_index: number;
  description: string;
  transportation: string;
  accommodation: string;
  hotel?: Hotel;
  attractions: Attraction[];
  meals: Meal[];
}

/**
 * 天气信息
 */
export interface WeatherInfo {
  date: string;
  day_weather: string;
  night_weather: string;
  day_temp: number;
  night_temp: number;
  wind_direction: string;
  wind_power: string;
}

/**
 * 旅行计划
 */
export interface TripPlan {
  city: string;
  start_date: string;
  end_date: string;
  days: DayPlan[];
  weather_info: WeatherInfo[];
  overall_suggestions: string;
  budget?: Budget;
}

/**
 * 旅行计划请求
 */
export interface TripPlanRequest {
  city: string;
  start_date: string;
  end_date: string;
  days: number;
  preferences?: string;
  budget?: number;
  transportation?: string;
  accommodation?: string;
  special_requirements?: string;
  traveler_type?: string;
  travel_pace?: string;
}
