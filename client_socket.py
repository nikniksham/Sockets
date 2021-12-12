import socket

# Получаем свой локальный ip адрес
self_ip = socket.gethostbyname(socket.gethostname())
nickname = b"Nikolausus"

while True:
    sock = socket.socket()
    sock.connect((self_ip, 9090))
    sock.send(nickname)
    data = str(sock.recv(1024))[2:-1]
    if data == "Success connect":
        break
    sock.close()

while True:
    data = str(sock.recv(1024))[2:-1]
    if data == "Check connect":
        continue
    print(data)

sock.close()
