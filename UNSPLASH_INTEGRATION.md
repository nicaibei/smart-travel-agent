# Unsplash 图片服务集成文档

## 📸 功能说明

Unsplash 服务自动为旅行计划中的每个景点获取高质量图片。

## 🔧 技术实现

### 1. 服务文件
`backend/app/services/unsplash_service.py`

### 2. 核心功能

```python
class UnsplashService:
    def search_photos(query: str, per_page: int) -> List[Dict]
        """搜索多张图片"""
        
    def get_photo_url(query: str) -> Optional[str]
        """获取单张图片URL"""
```

### 3. API 集成

在 `api/trip.py` 中自动为景点配图：

```python
# 为每个景点获取图片
for day in trip_plan.days:
    for attraction in day.attractions:
        if not attraction.image_url:
            image_url = unsplash_service.get_photo_url(
                f"{attraction.name} {trip_plan.city}"
            )
            attraction.image_url = image_url
```

## 🎯 使用流程

1. **用户请求旅行计划** → API接收请求
2. **多Agent生成计划** → 包含景点列表
3. **Unsplash自动配图** → 为每个景点搜索图片
4. **返回完整计划** → 景点信息包含图片URL

## 📋 返回数据格式

```json
{
  "days": [
    {
      "attractions": [
        {
          "name": "故宫",
          "image_url": "https://images.unsplash.com/photo-...",
          "description": "中国明清两代的皇家宫殿",
          ...
        }
      ]
    }
  ]
}
```

## 🧪 测试

### 运行测试脚本
```bash
python test_unsplash.py
```

### 测试内容
- ✅ 搜索多张图片
- ✅ 获取单张图片URL
- ✅ 处理搜索失败情况

## 📝 配置要求

### .env 文件
```env
UNSPLASH_ACCESS_KEY=你的Access_Key
UNSPLASH_SECRET_KEY=你的Secret_Key
```

### 获取 API Key
1. 访问 https://unsplash.com/developers
2. 注册并创建应用
3. 复制 Access Key 到 .env 文件

## 🎨 图片信息

每个图片包含：
- **url**: 普通尺寸图片URL
- **thumbnail**: 缩略图URL
- **description**: 图片描述
- **photographer**: 摄影师姓名
- **photographer_url**: 摄影师主页

## ⚠️ 注意事项

1. **使用限制**: 免费版每小时50次请求
2. **署名要求**: 使用图片需要标注摄影师信息
3. **网络超时**: 设置了10秒超时时间
4. **错误处理**: 获取失败不影响主流程

## 🚀 性能优化建议

1. **缓存机制**: 缓存常见景点的图片URL
2. **并行请求**: 使用异步请求提高速度
3. **降级策略**: 准备默认图片备用
4. **批量请求**: 一次请求获取多张图片

## 📈 后续改进

- [ ] 实现图片缓存
- [ ] 支持异步请求
- [ ] 添加默认图片
- [ ] 优化搜索关键词
- [ ] 支持多语言搜索
