"""
测试新的 API 接口
"""

import requests
import json
from datetime import datetime

def test_bazi_info():
    """测试八字基本信息接口"""
    url = "http://localhost:8000/8char/get-info"
    
    # 测试数据
    data = {
        "datetime": "2023-05-15 10:30:00",
        "gender": 1,
        "sect": 1,
        "realname": "张三"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("八字基本信息结果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

def test_bazi_prediction():
    """测试大运流年预测接口"""
    url = "http://localhost:8000/8char/get-prediction"
    
    # 测试数据
    data = {
        "datetime": "2023-05-15 10:30:00",
        "gender": 1,
        "sect": 1
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("大运流年预测结果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

def test_legacy_bazi():
    """测试兼容性接口"""
    url = "http://localhost:8000/bazi"
    
    # 测试数据
    data = {
        "name": "张三",
        "city": "北京",
        "gender": "男",
        "year": 2023,
        "month": 5,
        "day": 15,
        "hour": 10,
        "minute": 30
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("兼容性接口结果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    print("=== 测试新的八字 API ===")
    print("1. 测试八字基本信息接口...")
    test_bazi_info()
    
    print("\n2. 测试大运流年预测接口...")
    test_bazi_prediction()
    
    print("\n3. 测试兼容性接口...")
    test_legacy_bazi()