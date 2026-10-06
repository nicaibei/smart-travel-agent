"""测试脚本 - 测试Unsplash服务"""
from app.services import get_unsplash_service


def test_unsplash_service():
    """测试Unsplash图片服务"""
    
    print("=" * 60)
    print("🧪 测试 Unsplash 图片服务")
    print("=" * 60)
    
    unsplash = get_unsplash_service()
    
    # 测试1: 搜索多张图片
    print("\n📸 测试1: 搜索'北京故宫'的图片 (3张)")
    photos = unsplash.search_photos("北京故宫", per_page=3)
    
    if photos:
        print(f"✅ 找到 {len(photos)} 张图片:")
        for i, photo in enumerate(photos, 1):
            print(f"\n图片 {i}:")
            print(f"  - URL: {photo['url'][:60]}...")
            print(f"  - 缩略图: {photo['thumbnail'][:60]}...")
            print(f"  - 描述: {photo.get('description', '无')}")
            print(f"  - 摄影师: {photo['photographer']}")
    else:
        print("❌ 未找到图片")
    
    # 测试2: 获取单张图片URL
    print("\n" + "=" * 60)
    print("📸 测试2: 获取'长城'的单张图片")
    url = unsplash.get_photo_url("长城 中国")
    
    if url:
        print(f"✅ 图片URL: {url}")
    else:
        print("❌ 未找到图片")
    
    # 测试3: 搜索不存在的内容
    print("\n" + "=" * 60)
    print("📸 测试3: 搜索'xyzabc123notexist'")
    photos = unsplash.search_photos("xyzabc123notexist", per_page=1)
    
    if photos:
        print(f"✅ 找到 {len(photos)} 张图片")
    else:
        print("✅ 正确返回空列表")
    
    print("\n" + "=" * 60)
    print("✅ Unsplash服务测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_unsplash_service()
