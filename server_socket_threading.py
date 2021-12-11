import socket
import time
from threading import Thread


class Socket(Thread):
    def __init__(self, port, ip_address, max_users):
        super().__init__()
        self.port = port
        self.ip_address = ip_address
        self.max_users = max_users
        self.sock = socket.socket()
        self.sock.bind((self.ip_address, self.port))
        self.sock.listen(self.max_users)
        self.users = []
        self.queue = []  # Доделать

    def user_master(self, check_time):
        print("Success create user master")
        while True:
            conn, address = self.sock.accept()
            if len(self.users) >= self.max_users:
                time.sleep(check_time + 1)
            if len(self.users) < self.max_users:
                self.users.append([address, conn])
                print(f"Users {len(self.users)}/{self.max_users}")
                conn.send(b"Success connect")
                Thread(target=self.check_user_connect, args=(address, conn, check_time)).start()

    def check_user_connect(self, address, conn, check_time):
        while True:
            try:
                conn.send(b"Check connect")
            except:
                if [address, conn] in self.users:
                    self.users.remove([address, conn])
                print(f"Connection timed out with {address[0]}:{address[1]}")
                print(f"Users {len(self.users)}/{self.max_users}")
                break
            time.sleep(check_time)

    def run(self):
        Thread(target=self.user_master, args=(5,)).start()
        while True:
            for conn, address in [(conn, address) for address, conn in self.users]:
                data = None
                try:
                    data = str(conn.recv(1024))[2:-1]
                except:
                    print(f"Bad connection with {address}")
                if data:
                    print(f"Message from {address[0]}:{address[1]} - {data}")
                    # Какие то данные какие то сравнения


class Server:
    def __init__(self):
        self.users = {}
        self.sockets = []

    def create_socket(self, port, ip_address, max_users=2):
        if port not in self.users:  # Проверяем, что сокета с таким портом не существует
            sock = Socket(port, ip_address, max_users)
            self.sockets.append(sock)
            sock.run()

            return {"success": "Port success started"}
        else:
            return {"error": "This port is already in use"}  # Просим так больше не делать


self_ip = socket.gethostbyname(socket.gethostname())

server = Server()
server.create_socket(9090, self_ip)