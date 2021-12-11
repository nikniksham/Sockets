import socket

# Получаем свой локальный ip адрес
self_ip = socket.gethostbyname(socket.gethostname())

while True:
    sock = socket.socket()
    sock.connect((self_ip, 9090))
    sock.send(b"connect")
    data = str(sock.recv(1024))[2:-1]
    if data == "Success connect":
        break
    sock.close()

while True:
    data = str(sock.recv(1024))[2:-1]
    print(data)
#
# sock2 = socket.socket()
# sock2.connect((self_ip, 9090))
# sock2.send(b"connect")
# print(sock2.recv(1024))

# sock.send(b"close")
# print(sock.recv(1024))

# Получаем данные
# data = sock.recv(1024)
# Уходим довольные
# sock.close()

# print(data)