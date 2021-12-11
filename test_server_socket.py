import socket

# Получаем свой локальный ip адрес
self_ip = socket.gethostbyname(socket.gethostname())

# Создание и настройка сокета
# Создаём сокет
sock = socket.socket()
# Задаём сокету хост (пустой, что мы можно было обращаться с любого интерфейса) и порт (от 0 до 65535)
sock.bind((self_ip, 9090))
# Задаём максимальное количество одновременных пользователей
sock.listen(1)
# Принимаем заявку на подключение. Сокет возвращает нам кортеж из сессии и адреса пользователя
conn, address = sock.accept()

print(f"connected with {address}")

# Употребляем все данные пользователя
while True:
    # Получаем данные по 1024 байт
    data = conn.recv(1024)
    if not data:
        break
    # Отправляем данные, но в увеличенном виде
    conn.send(data.upper())

# Закрываем лавочку
conn.close()
