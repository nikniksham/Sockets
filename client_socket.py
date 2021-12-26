import socket
from threading import Thread
import time

# Получаем свой локальный ip адрес
self_ip = socket.gethostbyname(socket.gethostname())


class Client:
    def __init__(self, nickname, server, port):
        self.nickname = nickname
        self.server = server
        self.port = port
        self.is_connected = False
        self.socket = None

    def connection_monitoring(self):
        while True:
            if not self.socket:
                try:
                    sock = socket.socket()
                    sock.connect((self_ip, 9090))
                    sock.send(self.to_bytes(self.nickname))
                    data = self.to_text(sock.recv(1024))
                except:
                    continue
                if data == "Success connection":
                    print("Connected")
                    self.socket = sock
            time.sleep(1)
            # else:
            #     try:
            #         self.socket.send(b"Check connection")
            #     except:
            #         self.socket = None
            #     time.sleep(5)

    def to_bytes(self, message):
        return bytes(message, encoding="utf-8")

    def to_text(self, message):
        return str(message)[2:-1]

    def getting_from_the_server(self):
        while True:
            if self.socket:
                try:
                    data = self.to_text(self.socket.recv(1024))
                    if data != "Check connection":
                        print(data)
                except:
                    print("Lost connection")
                    self.socket = None

    def sending_to_the_server(self, message):
        try:
            self.socket.send(self.to_bytes(message))
        except:
            print("Lost connection")
            self.socket = None

    def game_process(self):
        while True:
            if self.socket:
                Thread(target=self.sending_to_the_server("Aaaa, ATAKA!!!"))
            time.sleep(1)

    def run(self):
        Thread(target=self.connection_monitoring).start()
        Thread(target=self.getting_from_the_server).start()
        Thread(target=self.game_process).start()


client = Client("Nickolausus", self_ip, 9090)
client.run()
