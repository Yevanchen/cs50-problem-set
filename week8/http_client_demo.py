#!/usr/bin/env python3
"""
HTTP客户端演示
演示如何发送不同类型的HTTP请求
"""

import requests
import json

def demo_http_requests():
    """演示各种HTTP请求"""
    base_url = "http://localhost:8080"
    
    print("=" * 60)
    print("HTTP 客户端演示")
    print("=" * 60)
    
    # 测试GET请求 - 200 OK
    print("\n1. 测试 GET 请求 (200 OK):")
    try:
        response = requests.get(f"{base_url}/")
        print(f"状态码: {response.status_code}")
        print(f"状态文本: {response.reason}")
        print(f"响应头Content-Type: {response.headers.get('Content-Type')}")
        print(f"响应内容长度: {len(response.text)} 字符")
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器。请确保服务器正在运行。")
        return
    
    # 测试重定向 - 301
    print("\n2. 测试 301 重定向:")
    try:
        response = requests.get(f"{base_url}/redirect", allow_redirects=False)
        print(f"状态码: {response.status_code}")
        print(f"状态文本: {response.reason}")
        print(f"重定向位置: {response.headers.get('Location')}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试404错误
    print("\n3. 测试 404 Not Found:")
    try:
        response = requests.get(f"{base_url}/notfound")
        print(f"状态码: {response.status_code}")
        print(f"状态文本: {response.reason}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试500错误
    print("\n4. 测试 500 Internal Server Error:")
    try:
        response = requests.get(f"{base_url}/error")
        print(f"状态码: {response.status_code}")
        print(f"状态文本: {response.reason}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试418茶壶
    print("\n5. 测试 418 I'm a teapot:")
    try:
        response = requests.get(f"{base_url}/teapot")
        print(f"状态码: {response.status_code}")
        print(f"状态文本: {response.reason}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试POST请求
    print("\n6. 测试 POST 请求:")
    try:
        post_data = {
            "用户名": "张三",
            "邮箱": "zhangsan@example.com",
            "消息": "这是一个测试POST请求"
        }
        response = requests.post(f"{base_url}/api/test", 
                               json=post_data,
                               headers={'Content-Type': 'application/json'})
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 显示请求头
    print("\n7. 查看请求头信息:")
    try:
        response = requests.get(f"{base_url}/headers")
        print(f"状态码: {response.status_code}")
        print("服务器收到的请求头信息已在网页中显示")
    except Exception as e:
        print(f"错误: {e}")

def demo_curl_commands():
    """演示等效的curl命令"""
    print("\n" + "=" * 60)
    print("等效的 curl 命令示例:")
    print("=" * 60)
    
    commands = [
        "# 基本GET请求\ncurl http://localhost:8080/",
        "# 只获取响应头\ncurl -I http://localhost:8080/",
        "# 显示详细信息\ncurl -v http://localhost:8080/",
        "# 测试重定向（不自动跟随）\ncurl -I http://localhost:8080/redirect",
        "# 测试404\ncurl -I http://localhost:8080/notfound",
        "# POST请求发送JSON数据\ncurl -X POST http://localhost:8080/api/test \\\n     -H 'Content-Type: application/json' \\\n     -d '{\"用户名\": \"张三\", \"消息\": \"测试\"}'",
        "# 添加自定义请求头\ncurl -H 'User-Agent: MyApp/1.0' http://localhost:8080/headers"
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"\n{i}. {cmd}")

if __name__ == "__main__":
    demo_http_requests()
    demo_curl_commands()
