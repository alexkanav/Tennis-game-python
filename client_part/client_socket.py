import socket


class ClientSocket:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = socket.socket()


    def connect(self):
        self.sock.connect((self.host, self.port))

    def send(self, data: str):
        self.sock.send(data.encode())

    def receive(self) -> str:
        return self.sock.recv(1024).decode()

    def close(self):
        self.sock.close()
