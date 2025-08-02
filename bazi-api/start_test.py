"""
启动 API 服务器并进行测试
"""

import subprocess
import time
import threading
import requests
import json

def start_server():
    """启动 API 服务器"""
    print("正在启动 API 服务器...")
    subprocess.run(["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])

def test_api():
    """等待服务器启动后测试 API"""
    print("等待服务器启动...")
    time.sleep(3)
    
    # 测试数据
    test_data = {
        "datetime": "2023-05-15 10:30:00",
        "gender": 1,
        "sect": 1,
        "realname": "张三"
    }
    
    try:
        # 测试新接口
        response = requests.post("http://localhost:8000/8char/get-info", json=test_data)
        if response.status_code == 200:
            result = response.json()
            print("✓ API 测试成功!")
            print(f"八字: {result['data']['top']['year']}{result['data']['bottom']['year']} {result['data']['top']['month']}{result['data']['bottom']['month']} {result['data']['top']['day']}{result['data']['bottom']['day']} {result['data']['top']['time']}{result['data']['bottom']['time']}")
            print(f"十神: {result['data']['gods']}")
            print(f"农历: {result['data']['datetime']['lunar']}")
        else:
            print(f"✗ API 测试失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ 测试请求失败: {e}")

if __name__ == "__main__":
    # 在后台线程中启动服务器
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # 测试 API
    test_api()
    
    print("\n服务器正在运行，按 Ctrl+C 停止...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n服务器已停止")