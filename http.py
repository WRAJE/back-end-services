import socket
with socket.socket() as s:  # 创建 socket 对象，使用 with 确保自动关闭
    host = "0.0.0.0"  # 代表所有 IPv4 地址
    port = 8089  # 设置端口
    s.bind((host, port))  # 绑定端口（代表接受来自host和port的请求）
    s.listen(5)  # 等待客户端连接
    while True:
        conn, addr = s.accept()  # 建立客户端连接
        with conn:  # 使用 with 确保连接自动关闭
            print('连接地址：', addr)
            request = conn.recv(4096).decode("utf-8", errors="ignore")
            # 简单解析请求行
            first_line = request.split("\r\n", 1)[0]
            method, path, _ = first_line.split(" ", 2)
            body = f"<h1>Hello</h1><p>Method={method}, Path={path}</p>"
            resp = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(body.encode())}\r\n"
                "Connection: close\r\n\r\n"
                f"{body}"
            )
            conn.sendall(resp.encode('utf-8'))  # 发送欢迎信息
            # conn.close()  # 已删除，with 语句会自动关闭连接