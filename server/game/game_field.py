from random import randint
from time import time
import tkinter as tk

from server.game.racket import Racket
from server.game.ball import Ball
from server.config import WIDTH, HEIGHT, GOAL_SIZE, RACKET_LENGTH


class GameField(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, background='yellow')

        self.create_line(5, 0, 5, (HEIGHT - GOAL_SIZE) // 2, width=8, fill='blue')
        self.create_line(5, HEIGHT - (HEIGHT - GOAL_SIZE) // 2, 5, HEIGHT, width=8, fill='blue')
        self.create_line(WIDTH - 5, 0, WIDTH - 5, (HEIGHT - GOAL_SIZE) // 2, width=8, fill='blue')
        self.create_line(WIDTH - 5, HEIGHT - (HEIGHT - GOAL_SIZE) // 2, WIDTH - 5, HEIGHT, width=8, fill='blue')
        self.racket_1 = Racket(self, 100, 200, RACKET_LENGTH, 'black')
        self.racket_2 = Racket(self, 700, 300, RACKET_LENGTH, 'red')
        self.balls = []

    def add_ball(self):
        dx = randint(-10, 10) * 4
        dy = randint(-10, 10)
        self.balls.append(Ball(self, dx, dy, WIDTH // 2, HEIGHT // 2))

    def balls_move(self) -> int:
        goal = 0
        for ball in self.balls:
            ball.move_ball(self.racket_1, self.racket_2, self.balls)
            ball.show_ball()
            goal = ball.goal()
            if time() - ball.live_ball > 10 or goal:
                self.delete(ball.ball_id)
                self.balls.remove(ball)
        return goal

    def new_coord_rack_2(self, x: str, y: str):
        self.racket_2.rx = int(x)
        self.racket_2.ry = int(y)

    def rackets_show(self):
        self.bind('<Motion>', self.racket_1.show)
        self.racket_2.show()

