import threading
import time

from client import tk
from client.game.game_field import GameField
from client.client_socket import ClientSocket
from client.config import HOST, PORT


class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='#9a7654')

        self.score_1 = 0
        self.score_2 = 0
        self.score_label = tk.Label(
            self,
            text=f'connecting to server',
            font=("Times New Roman", 12)
        )
        self.score_label.pack()
        self.game_field = GameField(self)
        self.game_field.pack(fill=tk.BOTH, expand=1)
        self.connected = False
        self.conn = ClientSocket(HOST, PORT)
        self.game_running = True

    def start_game(self):
        t1 = threading.Thread(target=self.connect_to_server)
        t1.start()

    def connect_to_server(self):
        while self.game_running:
            try:
                self.conn.connect()
                self.score_label.config(text='0 : 0')
                self.connected = True
                break
            except Exception as e:
                print(e)
                for i in range(5):
                    self.score_label.config(text=f'connecting{" ." * i}')
                    time.sleep(.5)

    def game(self):
        if self.connected:
            self.game_field.bind('<Motion>', self.game_field.racket_1.move)
            self.conn.send(f'{str(self.game_field.racket_1.x)}/{str(self.game_field.racket_1.y)}')
            received_data = self.conn.receive()
            if received_data[0] == 'g':
                score = received_data[1:].split(':')
                self.score_label.config(text=f'{score[0]} : {score[1]}')
            else:
                rack_coord, balls_coord = received_data.split(':')
                self.game_field.racket_2.x, self.game_field.racket_2.y = map(int, rack_coord.split('/'))
                self.game_field.show_rackets()
                self.game_field.show_balls(eval(balls_coord))

    def close_connection(self):
        self.conn.close()
        self.game_running = False
