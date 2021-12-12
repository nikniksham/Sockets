import socket
import time
from threading import Thread


class Socket(Thread):
    def __init__(self, port, ip_address, max_users, check_time):
        super().__init__()
        self.port = port
        self.ip_address = ip_address
        self.max_users = max_users
        self.sock = socket.socket()
        self.sock.bind((self.ip_address, self.port))
        self.sock.listen(self.max_users)
        self.check_time = check_time
        self.users = {}
        self.queue = []  # Доделать

    def user_master(self):
        print("Success create user master")
        Thread(target=self.user_queue).start()
        while True:
            conn, address = self.sock.accept()
            self.queue.append([conn, address])

    def user_queue(self):
        while True:
            users = [[conn, address] for conn, address in self.queue]
            for conn, address in users:
                if len(self.users) < self.max_users:
                    self.users[address] = conn
                    print(f"Users {len(self.users)}/{self.max_users}")
                    conn.send(b"Success connect")
                    self.queue.remove([conn, address])
                    Thread(target=self.check_user_connect, args=(address, conn)).start()
            time.sleep(1)

    def check_user_connect(self, address, conn):
        while True:
            try:
                conn.send(b"Check connect")
            except:
                if address in self.users:
                    del self.users[address]
                print(f"Connection timed out with {address[0]}:{address[1]}")
                print(f"Users {len(self.users)}/{self.max_users}")
                break
            time.sleep(self.check_time)

    def run(self):
        Thread(target=self.user_master).start()
        while True:
            try:
                users = [[address, conn] for address, conn in self.users.items()]
            except:
                continue
            for address, conn in users:
                data = None
                try:
                    data = str(conn.recv(1024))[2:-1]
                except:
                    print(f"Bad connection with {address}")
                    time.sleep(1)
                if data:
                    print(f"Message from {address[0]}:{address[1]} - {data}")
                    # Какие то данные какие то сравнения


class Server:
    def __init__(self):
        self.ports = []
        self.sockets = []

    def create_socket(self, port, ip_address, max_users=2):
        if port not in self.ports:  # Проверяем, что сокета с таким портом не существует
            sock = Socket(port, ip_address, max_users, 5)
            self.sockets.append(sock)
            self.ports.append(port)
            Thread(target=sock.run).start()

            return {"success": "Port success started"}
        else:
            return {"error": "This port is already in use"}  # Просим так больше не делать


self_ip = socket.gethostbyname(socket.gethostname())

print(self_ip)

server = Server()
print(server.create_socket(9090, self_ip))
# print(server.create_socket(9091, self_ip))