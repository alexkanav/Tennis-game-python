import tkinter as tk
from client.config import HEIGHT, WIDTH, GOAL_SIZE, BALL_RADIUS
from .racket import Racket


class GameField(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, background='yellow')
        self.pack(expand=1, fill='both')
        self.create_line(5, 0, 5, (HEIGHT - GOAL_SIZE) // 2, width=8, fill='blue')
        self.create_line(5, HEIGHT - (HEIGHT - GOAL_SIZE) // 2, 5, HEIGHT, width=8, fill='blue')
        self.create_line(WIDTH - 5, 0, WIDTH - 5, (HEIGHT - GOAL_SIZE) // 2, width=8, fill='blue')
        self.create_line(WIDTH - 5, HEIGHT - (HEIGHT - GOAL_SIZE) // 2, WIDTH - 5, HEIGHT, width=8, fill='blue')
        self.racket_1 = Racket(self, 'black', 100, 200)
        self.racket_2 = Racket(self, 'red', 700, 300)
        self.balls_on_the_field = []

    def show_rackets(self):
        self.racket_1.show()
        self.racket_2.show()

    def show_balls(self, balls: list[tuple[str, int, int]]):
        for ball in self.balls_on_the_field:
            self.delete(ball)
        self.balls_on_the_field.clear()

        for ball in balls:
            self.balls_on_the_field.append(
                self.create_oval(ball[1] - BALL_RADIUS, ball[2] - BALL_RADIUS, ball[1] + BALL_RADIUS,
                                 ball[2] + BALL_RADIUS, fill=ball[0]))



