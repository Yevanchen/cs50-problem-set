#!/usr/bin/env python3
"""
简单的HTTP服务器演示
演示不同的HTTP状态码和响应
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

class DemoHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """处理GET请求"""
        print(f"收到GET请求: {self.path}")
        
        if self.path == "/" or self.path == "/index":
            # 200 OK 响应
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html_content = """
            <!DOCTYPE html>
            <html lang="zh-CN">
            <head>
                <meta charset="UTF-8">
                <title>HTTP 演示服务器</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .status-code { color: #007acc; font-weight: bold; }
                    .example { background: #f5f5f5; padding: 10px; margin: 10px 0; }
                </style>
            </head>
            <body>
                <h1>HTTP 协议演示服务器</h1>
                <p>欢迎来到HTTP演示服务器！这里你可以测试不同的HTTP状态码。</p>
                
                <h2>可以测试的路径：</h2>
                <ul>
                    <li><a href="/">/</a> - <span class="status-code">200 OK</span> 主页</li>
                    <li><a href="/redirect">/redirect</a> - <span class="status-code">301 Moved Permanently</span> 永久重定向</li>
                    <li><a href="/found">/found</a> - <span class="status-code">302 Found</span> 临时重定向</li>
                    <li><a href="/notfound">/notfound</a> - <span class="status-code">404 Not Found</span> 页面未找到</li>
                    <li><a href="/error">/error</a> - <span class="status-code">500 Internal Server Error</span> 服务器错误</li>
                    <li><a href="/teapot">/teapot</a> - <span class="status-code">418 I'm a teapot</span> 我是茶壶</li>
                    <li><a href="/unauthorized">/unauthorized</a> - <span class="status-code">401 Unauthorized</span> 未授权</li>
                    <li><a href="/forbidden">/forbidden</a> - <span class="status-code">403 Forbidden</span> 禁止访问</li>
                    <li><a href="/headers">/headers</a> - 查看请求头信息</li>
                </ul>
                
                <h2>当前请求信息：</h2>
                <div class="example">
                    <p><strong>请求方法:</strong> GET</p>
                    <p><strong>请求路径:</strong> {}</p>
                    <p><strong>HTTP版本:</strong> {}</p>
                </div>
            </body>
            </html>
            """.format(self.path, self.request_version)
            
            self.wfile.write(html_content.encode('utf-8'))
            
        elif self.path == "/redirect":
            # 301 永久重定向
            self.send_response(301)
            self.send_header('Location', '/')
            self.end_headers()
            
        elif self.path == "/found":
            # 302 临时重定向
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
            
        elif self.path == "/notfound":
            # 404 Not Found
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html_content = """
            <!DOCTYPE html>
            <html>
            <head><title>404 - 页面未找到</title></head>
            <body>
                <h1>404 - 页面未找到</h1>
                <p>抱歉，您请求的页面不存在。</p>
                <a href="/">返回主页</a>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
            
        elif self.path == "/error":
            # 500 Internal Server Error
            self.send_response(500)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html_content = """
            <!DOCTYPE html>
            <html>
            <head><title>500 - 服务器内部错误</title></head>
            <body>
                <h1>500 - 服务器内部错误</h1>
                <p>服务器遇到了一个错误，无法完成您的请求。</p>
                <p>这通常是开发者的错误！</p>
                <a href="/">返回主页</a>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
            
        elif self.path == "/teapot":
            # 418 I'm a teapot (RFC 2324 愚人节RFC)
            self.send_response(418)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html_content = """
            <!DOCTYPE html>
            <html>
            <head><title>418 - 我是茶壶</title></head>
            <body>
                <h1>418 - I'm a teapot</h1>
                <p>我是一个茶壶，不能冲咖啡。☕️</p>
                <p>这是一个有趣的HTTP状态码，来自1998年愚人节RFC。</p>
                <a href="/">返回主页</a>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
            
        elif self.path == "/unauthorized":
            # 401 Unauthorized
            self.send_response(401)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('WWW-Authenticate', 'Basic realm="Demo"')
            self.end_headers()
            
            html_content = """
            <!DOCTYPE html>
            <html>
            <head><title>401 - 未授权</title></head>
            <body>
                <h1>401 - 未授权</h1>
                <p>您需要提供有效的凭据才能访问此资源。</p>
                <a href="/">返回主页</a>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
            
        elif self.path == "/forbidden":
            # 403 Forbidden
            self.send_response(403)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html_content = """
            <!DOCTYPE html>
            <html>
            <head><title>403 - 禁止访问</title></head>
            <body>
                <h1>403 - 禁止访问</h1>
                <p>您没有权限访问此资源。</p>
                <a href="/">返回主页</a>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
            
        elif self.path == "/headers":
            # 显示请求头信息
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            headers_info = ""
            for header, value in self.headers.items():
                headers_info += f"<tr><td><strong>{header}:</strong></td><td>{value}</td></tr>"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head><title>请求头信息</title></head>
            <body>
                <h1>HTTP 请求头信息</h1>
                <table border="1" style="border-collapse: collapse;">
                    <tr><th>请求头</th><th>值</th></tr>
                    {headers_info}
                </table>
                <h2>请求详情:</h2>
                <p><strong>方法:</strong> {self.command}</p>
                <p><strong>路径:</strong> {self.path}</p>
                <p><strong>HTTP版本:</strong> {self.request_version}</p>
                <p><strong>客户端地址:</strong> {self.client_address[0]}:{self.client_address[1]}</p>
                <a href="/">返回主页</a>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
            
        else:
            # 默认404响应
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html_content = """
            <!DOCTYPE html>
            <html>
            <head><title>404 - 页面未找到</title></head>
            <body>
                <h1>404 - 页面未找到</h1>
                <p>请求的路径不存在。</p>
                <a href="/">返回主页</a>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
    
    def do_POST(self):
        """处理POST请求"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        print(f"收到POST请求: {self.path}")
        print(f"POST数据: {post_data.decode('utf-8', errors='ignore')}")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        
        response_data = {
            "message": "POST请求处理成功",
            "path": self.path,
            "method": "POST",
            "data_received": post_data.decode('utf-8', errors='ignore'),
            "content_length": content_length
        }
        
        self.wfile.write(json.dumps(response_data, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_server(port=8080):
    """启动HTTP服务器"""
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, DemoHTTPRequestHandler)
    
    print(f"HTTP演示服务器启动在 http://localhost:\{port\}/")
    print("按 Ctrl+C 停止服务器")
    print("\n可以测试的URL:")
    print(f"  http://localhost:\{port\}/")
    print(f"  http://localhost:\{port\}/redirect")
    print(f"  http://localhost:\{port\}/notfound")
    print(f"  http://localhost:\{port\}/error")
    print(f"  http://localhost:\{port\}/teapot")
    print(f"  http://localhost:\{port\}/headers")
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
