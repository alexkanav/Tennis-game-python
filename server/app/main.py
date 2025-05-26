import threading
from random import randint
import time

from server import tk
from server.game.game_field import GameField
from server.server_socket import ServerSocket
from server.config import HOST, PORT, LIMIT_SCORE


class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='#9a7654')

        self.score_1 = 0
        self.score_2 = 0
        self.goal = False
        self.score_label = tk.Label(
            self,
            text='Waiting for client to connect',
            font=("Times New Roman", 12)
        )
        self.score_label.pack()
        self.game_field = GameField(self)
        self.game_field.pack(fill=tk.BOTH, expand=1)
        self.interval = 0
        self.rand = randint(2, 30)
        self.event_stop = threading.Event()
        self.run = False
        self.new_score = True
        self.server = ServerSocket(HOST, PORT)

    def new_game(self):
        self.score_1 = 0
        self.score_2 = 0
        self.new_score = True
        self.score_label.config(text=f'{self.score_1} : {self.score_2}')
        for ball in self.game_field.balls:
            self.game_field.delete(ball.ball_id)
            self.game_field.balls.remove(ball)
        if threading.active_count() == 1:
            t1 = threading.Thread(target=self.handle_client)
            t1.start()

    def handle_client(self):
        print(self.server.connection())
        self.run = True
        self.score_label.config(text=f'{self.score_1} : {self.score_2}')

        while True:
            if self.event_stop.is_set():
                break

            self.game_field.racket_2.rx, self.game_field.racket_2.ry = map(int, self.server.receive().split('/'))
            if self.goal:
                self.server.send(f'g{self.score_1}:{self.score_2}')
                self.goal = False
            elif self.new_score:
                self.server.send(f'g{self.score_1}:{self.score_2}')
                self.new_score = False
            else:
                balls_coord = [(ball.color, ball.x, ball.y) for ball in self.game_field.balls]
                self.server.send(
                    f'{str(self.game_field.racket_1.rx)}/{str(self.game_field.racket_1.ry)}:{str(balls_coord)}')

    def game(self):
        self.interval += 0.1
        if self.interval >= self.rand:
            self.game_field.add_ball()
            self.interval = 0
            self.rand = randint(10, 30)
        if score := self.game_field.balls_move():
            match score:
                case 1:
                    self.score_1 += 1
                case 2:
                    self.score_2 += 1
            self.score_label.config(text=f'{self.score_1} : {self.score_2}')
            self.goal = True
            time.sleep(1)
            if self.score_1 == LIMIT_SCORE or self.score_2 == LIMIT_SCORE:
                print('game over')
                self.run = False
                self.score_label.config(
                    text=f'Winner Player {1 if self.score_1 > self.score_2 else 2}  ---> Score {self.score_1}:{self.score_2}')
        self.game_field.rackets_show()

    def exit(self):
        self.server.close()
        self.event_stop.set()
