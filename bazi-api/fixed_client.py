import requests
import json

def main(sname: str, scity: str, sgender: str, syear: int, smonth: int, sday: int, shour: int, sminute: int = 0) -> dict:
    """
    修复后的客户端代码
    """
    
    url = "http://113.45.75.106:8089/bazi"
    payload = {
        "name": sname,
        "city": scity, 
        "gender": sgender,
        "year": syear, 
        "month": smonth, 
        "day": sday, 
        "hour": shour,
        "minute": sminute  # 添加缺失的minute参数
    }
    
    try:
        print(f"🚀 发送请求: {json.dumps(payload, ensure_ascii=False)}")
        
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10
        )
        
        print(f"📊 状态码: {response.status_code}")
        print(f"📏 响应长度: {len(response.text)}")
        
        # 检查状态码
        if response.status_code != 200:
            print(f"❌ HTTP错误: {response.status_code}")
            return {"error": f"HTTP {response.status_code}", "content": response.text}
        
        # 检查响应内容
        if not response.text:
            print("❌ 响应为空")
            return {"error": "空响应"}
        
        # 解析JSON
        try:
            result = response.json()
            print(f"✅ 成功获取数据，键数: {len(result) if isinstance(result, dict) else 'N/A'}")
            return {"success": True, "result": result}
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            return {"error": "JSON解析失败", "raw_content": response.text[:200]}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
        return {"error": str(e)}

# 测试函数
def test_fixed_client():
    """测试修复后的客户端"""
    result = main("常温奶", "郑州", "男", 1989, 5, 21, 8)
    
    print("\n" + "="*50)
    print("🧪 测试结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if result.get("success"):
        print("✅ 客户端测试成功！")
        bazi_data = result["result"]
        print(f"👤 姓名: {bazi_data.get('realname')}")
        print(f"🕐 时间: {bazi_data.get('datetime', {}).get('solar')}")
        print(f"🐲 生肖: {bazi_data.get('zodiac')}")
        print(f"⭐ 星座: {bazi_data.get('constellation')}")
    else:
        print("❌ 客户端测试失败")
        print(f"错误: {result.get('error')}")

if __name__ == "__main__":
    test_fixed_client()