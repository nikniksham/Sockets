import asyncio
import socket
import concurrent.futures


class Server:
    def __init__(self):
        self.users = {}
        self.sockets = []

    async def create_socket(self, port, ip_address, max_users=2):
        if port not in self.users:  # Проверяем, что сокета с таким портом не существует
            # Создаём сокет
            sock = socket.socket()
            # Задаём сокету кортеж из ip и порта
            sock.bind((ip_address, port))
            # Говорим, что у сокета может быть максимум только два пользователя, что бы никто не пристраивался сзади
            sock.listen(max_users)

            # Создаём список пользователей для сессии с новым портом
            self.users[port] = []

            # Добавляем сокет в список сокетов
            self.sockets.append(sock)

            await asyncio.create_task(self.start_socket(sock, port, max_users))
            return {"success": "Port success started"}
        else:
            return {"error": "This port is already in use"}  # Просим так больше не делать

    async def check_connect(self, port, address, conn, check_time):
        while True:
            try:
                conn.send(b"\x05")
            except:
                if conn in self.users[port]:
                    self.users[port].remove([address, conn])
                print(f"Connection timed out with {address[0]}:{address[1]}")
                break
            # time.sleep(check_time)
            await asyncio.sleep(check_time)

    async def start_socket(self, sock, port, max_users):
        # loop = asyncio.get_running_loop()
        while len(self.users[port]) != max_users or True:
            conn, address = sock.accept()
            print(conn, address)
            self.users[port].append([address, conn])
            # await self.check_connect(port, address, conn, 5)
            # asyncio.run(self.check_connect(port, address, conn, 5))
            # task = asyncio.futures(self.check_connect(port, address, conn, 5))
            # await asyncio.wait(task)
            await asyncio.create_task(self.check_connect(port, address, conn, 5))
            print(f"Connected with {address[0]}:{address[1]}")
            # await asyncio.create_task(self.check_connect(port, address, conn, 5))
            print(1)
                # print(conn)
            # print()
        print(2)
        conn2, address2 = sock.accept()
        print(3)
        while True:
            data = str(conn.recv(1024))[2:-1]
            if data != "":
                print(data)
            if data == "close":
                conn.send(b"Success close")
                break
            elif data == "connect":
                conn.send(b"Success connect")
        conn.close()


self_ip = socket.gethostbyname(socket.gethostname())

server = Server()
asyncio.run(server.create_socket(9090, self_ip))