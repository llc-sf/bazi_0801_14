#!/usr/bin/env python3
"""
测试 bazi-api 的客户端
"""

import requests
import json
import sys

def test_bazi_api():
    """测试八字API"""
    
    # 测试数据
    test_data = {
        "name": "999",
        "city": "北京", 
        "gender": "男",
        "year": 1992,
        "month": 9,
        "day": 9,
        "hour": 9,
        "minute": 0
    }
    
    print("🚀 开始测试 bazi-api")
    print(f"📤 请求数据: {test_data}")
    print("-" * 50)
    
    try:
        # 发送请求
        url = "http://113.45.75.106:8089/bazi"
        headers = {"Content-Type": "application/json"}
        
        print(f"🌐 请求URL: {url}")
        
        response = requests.post(
            url, 
            headers=headers, 
            json=test_data,
            timeout=30
        )
        
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📏 响应长度: {len(response.text)} 字节")
        print(f"🔤 Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code == 200:
            print("✅ HTTP 状态正常")
            
            # 检查原始响应
            print(f"📝 原始响应前200字符: {response.text[:200]}...")
            
            try:
                # 尝试解析JSON
                data = response.json()
                print("✅ JSON解析成功")
                print(f"📊 数据类型: {type(data)}")
                
                if isinstance(data, dict):
                    print(f"🔑 字典键数量: {len(data)}")
                    print(f"🗝️ 主要键: {list(data.keys())[:10]}")
                    
                    # 打印完整的JSON数据
                    print("📋 完整API响应数据:")
                    print(json.dumps(data, ensure_ascii=False, indent=2))
                    
                    print("\n" + "="*50)
                    print("🔍 关键字段检查:")
                    
                    # 检查关键字段
                    key_fields = ['realname', 'gender', 'timestamp', 'datetime', 'embryo']
                    for field in key_fields:
                        if field in data:
                            field_value = data[field]
                            print(f"  ✅ {field}: {type(field_value)} = {field_value}")
                        else:
                            print(f"  ❌ {field}: 缺失")
                    
                    # 特别检查 embryo 字段
                    if 'embryo' in data:
                        embryo = data['embryo']
                        print(f"\n🧬 embryo详细分析:")
                        print(f"  类型: {type(embryo)}")
                        print(f"  长度: {len(embryo) if hasattr(embryo, '__len__') else 'N/A'}")
                        print(f"  内容: {embryo}")
                        
                        # 检查每个元素的类型
                        if isinstance(embryo, list):
                            for i, item in enumerate(embryo):
                                print(f"    [{i}]: {type(item)} = {item}")
                                if isinstance(item, list):
                                    for j, subitem in enumerate(item):
                                        print(f"      [{i}][{j}]: {type(subitem)} = {subitem}")
                    
                    return data
                else:
                    print(f"❌ 数据不是字典类型: {type(data)}")
                    return None
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"🔍 尝试解析的内容: {response.text[:500]}...")
                return None
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"📝 错误内容: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误")
        return None
    except Exception as e:
        print(f"❌ 未知异常: {type(e).__name__}: {e}")
        return None

def test_simple_function():
    """模拟Dify中的函数调用"""
    print("\n" + "="*50)
    print("🧪 模拟Dify函数调用测试")
    print("="*50)
    
    def main(sname: str, scity: str, sgender: str, syear: int, smonth: int, sday: int, shour: int) -> str:
        try:
            r = requests.post(
                "http://113.45.75.106:8089/bazi",
                headers={"Content-Type": "application/json"},
                json={
                    "name": sname,
                    "city": scity, 
                    "gender": sgender,
                    "year": syear, 
                    "month": smonth, 
                    "day": sday, 
                    "hour": shour,
                    "minute": 0
                },
                timeout=10
            )
            
            if r.status_code == 200:
                # 返回JSON字符串
                return json.dumps(r.json(), ensure_ascii=False)
            else:
                return json.dumps({"error": f"HTTP {r.status_code}"}, ensure_ascii=False)
                
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    # 调用函数
    result = main("999", "北京", "男", 1992, 9, 9, 9)
    print(f"🎯 模拟Dify函数完整返回结果:")
    print(f"  类型: {type(result)}")
    print(f"  字符串长度: {len(result)}")
    print("  完整内容:")
    
    # 如果是JSON字符串，尝试格式化显示
    try:
        parsed = json.loads(result)
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
        print(f"\n✅ 成功解析为JSON，包含 {len(parsed) if isinstance(parsed, dict) else 'N/A'} 个字段")
    except json.JSONDecodeError:
        print(result)
        print("\n❌ 不是有效的JSON字符串")
    
    return result

if __name__ == "__main__":
    # 运行测试
    print("开始综合测试...")
    
    # 测试1: 直接API调用
    api_result = test_bazi_api()
    
    # 测试2: 模拟Dify函数
    func_result = test_simple_function()
    
    print("\n" + "="*50)
    print("📋 测试总结")
    print("="*50)
    print(f"API测试: {'✅ 成功' if api_result else '❌ 失败'}")
    
    # 检查字符串函数返回结果
    func_success = False
    if func_result:
        try:
            parsed_func = json.loads(func_result)
            func_success = isinstance(parsed_func, dict) and 'error' not in parsed_func
        except:
            func_success = False
    
    print(f"函数测试(字符串): {'✅ 成功' if func_success else '❌ 失败'}")
    
    if api_result and func_success:
        print("🎉 所有测试通过！API返回字符串格式正常。")
        print("💡 如果Dify中配置result为String类型，可以直接使用字符串返回。")
    else:
        print("⚠️ 测试发现问题，需要进一步调试。")