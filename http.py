import socket

HOST = "0.0.0.0"
PORT = 8089

class Http:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
    
    def getRoot(self, path):
        """处理根路径请求，子类应重写此方法"""
        body = f"<h1>Hello</h1><p>Path={path}</p>"
        self.response(body)
    
    def get404(self, path):
        """处理404错误，子类应重写此方法"""
        body = f"<h1>404 Not Found</h1><p>Path={path}</p>"
        self.response(body, status="404 Not Found")
    
    def response(self, body, status="200 OK", content_type="text/html; charset=utf-8"):
        """发送HTTP响应"""
        resp = (
            f"HTTP/1.1 {status}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            "Connection: close\r\n\r\n"
            f"{body}"
        )
        self.conn.sendall(resp.encode('utf-8'))
    
    def handle_request(self):
        """处理HTTP请求 - 现在使用已解析的method和path"""
        try:
            # 根据路径调用相应的处理方法
            if self.path == "/" or self.path == "":
                self.getRoot(self.path)
            else:
                # 这里可以扩展为更复杂的路由逻辑
                self.get404(self.path)
        except Exception as e:
            # 如果解析出错，返回400错误
            body = f"<h1>400 Bad Request</h1><p>Error: {e}</p>"
            self.response(body, status="400 Bad Request")
    
    def start_server(self):
        """启动HTTP服务器"""
        # 使用 with 语法确保 socket 被自动关闭
        with socket.socket() as s:  # 创建 socket 对象
            s.bind((self.host, self.port))  # 绑定端口（代表接受来自host和port的请求）
            
            s.listen(5)  # 等待客户端连接
            print(f'服务器启动在 {self.host}:{self.port}')
            
            while True:
                conn, addr = s.accept()  # 建立客户端连接
                with conn:
                    print('连接地址：', addr)
                    self.conn = conn
                    request = conn.recv(4096).decode("utf-8", errors="ignore")
                    # 简单解析请求行
                    first_line = request.split("\r\n", 1)[0]
                    method, path, _ = first_line.split(" ", 2)
                    self.method = method
                    self.path = path
                    
                    # 处理请求
                    self.handle_request()