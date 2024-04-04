from socket import socket,AF_INET ,SOCK_STREAM #
# AF_INET 用于Internet之间的进程通信，
# SOCK_STREAM  # 表示的是用TCP协议编程

# (1)创建socket对象
server_socket=socket(AF_INET,SOCK_STREAM)
# (2)绑定IP地址和端口
ip='127.0.0.1' # 等同于local
port=8888 # 端口的范围
server_socket.bind((ip,port))

# (3)使用listen()开始监听
server_socket.listen(5)

print('服务器已启动')

# (4)等待客户端的连接
client_socket,client_addr=server_socket.accept() # 系列解包赋值

# (5)接收来自客户端的数据
data=client_socket.recv(1024)
print('客户端发送过来的数据为:',data.decode('utf-8')) # 要求客户端发送过来的数据是使用utf-8进行编码的

# (6)关闭socket
server_socket.close()



