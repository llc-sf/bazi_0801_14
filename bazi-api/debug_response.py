import requests
import json

def debug_api_response():
    """详细调试API响应"""
    
    url = "http://113.45.75.106:8089/bazi"
    payload = {
        "name": "常温奶",
        "city": "郑州", 
        "gender": "男",
        "year": 1989, 
        "month": 5, 
        "day": 21, 
        "hour": 8,
        "minute": 0
    }
    
    print("🚀 发送请求到:", url)
    print("📤 请求数据:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("\n" + "="*50)
    
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        print(f"📊 HTTP状态码: {response.status_code}")
        print(f"📋 响应头:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        print(f"\n📏 响应体大小: {len(response.content)} 字节")
        print(f"📄 响应文本长度: {len(response.text)} 字符")
        
        # 检查原始响应
        print(f"\n🔍 原始响应内容 (前200字符):")
        print(repr(response.text[:200]))
        
        # 检查是否为空
        if not response.text:
            print("❌ 响应文本为空！")
            return
        
        if response.text.strip() == "":
            print("❌ 响应文本只包含空白字符！")
            return
            
        # 尝试JSON解析
        try:
            data = response.json()
            print(f"\n✅ JSON解析成功!")
            print(f"📊 数据类型: {type(data)}")
            
            if isinstance(data, dict):
                print(f"🔑 JSON键数量: {len(data)}")
                print(f"🔑 主要键: {list(data.keys())[:10]}")  # 显示前10个键
            
            # 美化输出部分数据
            print(f"\n📋 响应数据 (格式化前500字符):")
            formatted = json.dumps(data, ensure_ascii=False, indent=2)
            print(formatted[:500] + "..." if len(formatted) > 500 else formatted)
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print("🔍 响应可能不是有效的JSON格式")
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误")
    except Exception as e:
        print(f"❌ 其他错误: {e}")

if __name__ == "__main__":
    debug_api_response()