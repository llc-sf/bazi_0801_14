import requests
import json

def test_bazi_api(sname: str, scity: str, sgender: str, syear: int, smonth: int, sday: int, shour: int) -> dict:
    """测试bazi API"""
    
    url = "http://113.45.75.106:8089/bazi"
    payload = {
        "name": sname,
        "city": scity, 
        "gender": sgender,
        "year": syear, 
        "month": smonth, 
        "day": sday, 
        "hour": shour
    }
    
    print(f"🔍 测试API: {url}")
    print(f"📤 请求数据: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10
        )
        
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📋 响应头: {dict(response.headers)}")
        
        # 打印原始响应内容
        raw_content = response.text
        print(f"📄 原始响应内容: '{raw_content}'")
        print(f"📏 响应长度: {len(raw_content)} 字符")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"✅ JSON解析成功:")
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return {"success": True, "result": result}
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                return {"success": False, "error": "JSON解析失败", "raw_content": raw_content}
        else:
            print(f"❌ API请求失败，状态码: {response.status_code}")
            return {"success": False, "error": f"HTTP {response.status_code}", "content": raw_content}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求异常: {e}")
        return {"success": False, "error": str(e)}

def test_multiple_cases():
    """测试多个案例"""
    
    test_cases = [
        {
            "name": "张三",
            "city": "北京",
            "gender": "男",
            "year": 2023,
            "month": 5,
            "day": 15,
            "hour": 10
        },
        {
            "name": "李四", 
            "city": "上海",
            "gender": "女",
            "year": 1990,
            "month": 8,
            "day": 20,
            "hour": 14
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"🧪 测试案例 {i}")
        print(f"{'='*60}")
        
        result = test_bazi_api(**case)
        
        if result.get("success"):
            print("✅ 测试成功")
        else:
            print("❌ 测试失败")
            print(f"错误信息: {result.get('error')}")

if __name__ == "__main__":
    test_multiple_cases()