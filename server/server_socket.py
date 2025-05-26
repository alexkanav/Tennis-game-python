import socket


class ServerSocket:
    def __init__(self, host: str, port: int, num_conns: int = 1):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(num_conns)

    def connection(self) -> str:
        self.conn, self.addr = self.sock.accept()
        return f'connected: {self.addr}'

    def receive(self) -> str:
        return self.conn.recv(1024).decode()

    def send(self, data: str):
        self.conn.send(data.encode())

    def close(self):
        self.sock.close()
