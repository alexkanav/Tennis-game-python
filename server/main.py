import os
import threading
import tkinter as tk
from tkinter.messagebox import askyesno
from random import randint, choice
import time

from server_config import *
from server_socket import SocketServer


class Ball:
    def __init__(self, canvas, dx: int, dy: int, x: int, y: int, radius: int = BALL_RADIUS):
        self.canvas = canvas
        self.color = choice(['blue', 'green', 'red', 'brown', 'yellow'])
        self.x = x
        self.y = y
        self.r = radius
        self.z = 0
        self.dx = dx
        self.dy = dy
        self.ball_id = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=self.color)
        self.live_ball = time.time()
        self.t_t = time.time()

    def move_ball(self, racket_1, racket_2, balls: list) -> None:
        racket = racket_1 if self.x < WIDTH // 2 else racket_2
        rx, ry, rx_last, rack_length = racket.rx, racket.ry, racket.rx_last, racket.rack_length

        if self.dx > 0:  # the ball moves to the right
            if rx <= rx_last:  # the racket moves to the left
                if self.x <= rx:  # the ball is to the left of the racket
                    self.z = 1
                else:
                    if self.z == 1 and (ry < self.y < ry + rack_length):
                        self.dx = self.dx + (rx_last - rx) if (rx_last - rx) < 10 else self.dx + 10
                        self.dx = -self.dx
                        self.z = 0
                    else:
                        self.z = 0
                    if self.x + self.r + self.dx >= WIDTH and not (HEIGHT - GOAL_SIZE) / 2 < self.y < HEIGHT - (
                            HEIGHT - GOAL_SIZE) / 2:
                        self.dx = -self.dx
            else:  # the racket moves to the right
                if self.x >= rx:  # the ball is to the right of the racket
                    self.z = 0
                else:
                    if self.z == 0 and (ry < self.y < ry + rack_length):
                        self.dx = self.dx + (rx - rx_last) if (rx - rx_last) < 10 else self.dx + 10
                        self.z = 1
                    else:
                        self.z = 1
                    if self.x + self.r + self.dx >= WIDTH and not (HEIGHT - GOAL_SIZE) / 2 < self.y < HEIGHT - (
                            HEIGHT - GOAL_SIZE) / 2:
                        self.dx = -self.dx
        else:  # the ball moves to the left
            if rx >= rx_last:  # the racket moves to the right
                if self.x >= rx:  # the ball is to the right of the racket
                    self.z = 1
                else:
                    if self.z == 1 and (ry < self.y < ry + rack_length):
                        self.dx = self.dx - (rx - rx_last) if (rx - rx_last) < 10 else self.dx - 10
                        self.dx = -self.dx
                        self.z = 0
                    else:
                        self.z = 0
                    if self.x - self.r + self.dx <= 0 and not (HEIGHT - GOAL_SIZE) / 2 < self.y < HEIGHT - (
                            HEIGHT - GOAL_SIZE) / 2:
                        self.dx = -self.dx
            else:  # the racket moves to the right
                if self.x >= rx:  # the ball is to the right of the racket
                    self.z = 0
                else:
                    if self.z == 0 and (ry < self.y < ry + rack_length):
                        self.dx = self.dx + (rx_last - rx) if (rx_last - rx) < 10 else self.dx + 10
                        self.z = 1
                    else:
                        self.z = 1
                    if self.x + self.r + self.dx >= WIDTH and not (HEIGHT - GOAL_SIZE) / 2 < self.y < HEIGHT - (
                            HEIGHT - GOAL_SIZE) / 2:
                        self.dx = -self.dx
        if self.y + self.r - self.dy >= HEIGHT or self.y - self.r - self.dy <= 0:
            self.dy = -self.dy
        self.x = int(self.x + self.dx)
        self.y = int(self.y - self.dy)
        for rebound in balls:  # rebound_from_ball
            if rebound is not self:
                if (rebound.x - self.r < self.x < rebound.x + self.r) and (
                        rebound.y - self.r < self.y < rebound.y + self.r):
                    if time.time() - self.t_t > 0.5:
                        self.dx = -self.dx
                        self.dy = -self.dy
                    self.t_t = time.time()
            self.dy -= 0.2

    def show_ball(self):
        self.canvas.coords(self.ball_id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
        if self.dx != 0 and self.dy != 0:
            self.dx -= 0.03 * self.dx / abs(self.dx)
            self.dy -= 0.05 * self.dy / abs(self.dy)

    def goal(self, racket_1, racket_2) -> int:
        if self.x + self.r >= WIDTH and (HEIGHT - GOAL_SIZE) / 2 < self.y < HEIGHT - (HEIGHT - GOAL_SIZE) / 2 and not (
                racket_2.ry <= self.y <= racket_2.ry + racket_2.rack_length):
            return 1

        elif self.x - self.r <= 0 and (HEIGHT - GOAL_SIZE) / 2 < self.y < HEIGHT - (HEIGHT - GOAL_SIZE) / 2 and not (
                racket_1.ry <= self.y <= racket_1.ry + racket_1.rack_length):
            return 2

        else:
            return 0


class Racket:
    def __init__(self, canvas, rx: int, ry: int, rack_length: int, color: str):
        self.canvas = canvas
        self.rx = rx
        self.ry = ry
        self.rx_last = rx
        self.rack_length = rack_length
        self.racket_id = canvas.create_line(rx, ry, rx, ry + rack_length, fill=color, width=5)

    def show(self, event=None):
        self.rx_last = self.rx
        self.canvas.coords(self.racket_id, self.rx, self.ry, self.rx, self.ry + self.rack_length)
        if event:
            self.rx = event.x if event.x < 300 else 300
            self.ry = event.y


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

    def restart(self):
        self.add_ball()

    def add_ball(self):
        dx = randint(-10, 10) * 4
        dy = randint(-10, 10)
        self.balls.append(Ball(self, dx, dy, WIDTH // 2, HEIGHT // 2))

    def balls_move(self) -> int:
        goal = 0
        for ball in self.balls:
            ball.move_ball(self.racket_1, self.racket_2, self.balls)
            ball.show_ball()
            goal = ball.goal(self.racket_1, self.racket_2)
            if time.time() - ball.live_ball > 10 or goal:
                self.delete(ball.ball_id)
                self.balls.remove(ball)
        return goal

    def new_coord_rack_2(self, x: str, y: str):
        self.racket_2.rx = int(x)
        self.racket_2.ry = int(y)

    def rackets_show(self):
        self.bind('<Motion>', self.racket_1.show)
        self.racket_2.show()


class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='brown')

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
        self.rand = randint(5, 30)
        self.event_stop = threading.Event()
        self.run = False

    def new_game(self):
        self.score_1 = 0
        self.score_2 = 0
        self.game_field.restart()
        t1 = threading.Thread(target=self.handle_client)
        t1.start()

    def handle_client(self):
        self.server = SocketServer(HOST, PORT)
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


class Menu(tk.Menu):
    def __init__(self, master, game):
        super().__init__(master)

        self.game = game
        self.master.title("Tennis")
        self.file_menu = tk.Menu(self)
        self.file_menu.add_command(label="Save", command=self.master.save)
        self.file_menu.add_command(label="Load", command=self.master.load)
        self.add_cascade(label="File", menu=self.file_menu)
        self.game_menu = tk.Menu(self)
        self.game_menu.add_command(label="Pause", command=self.master.pause)
        self.game_menu.add_command(label="Start", command=self.master.start)
        self.game_menu.add_command(label="New", command=self.master.new_game)
        self.add_cascade(label="Game", menu=self.game_menu)


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap('racket.ico')
        self.geometry(f'{str(WIDTH)}x{str(HEIGHT + 40)}')
        self.save_dir = os.path.join(os.path.split(__file__)[0], 'save')
        self.main_frame = MainFrame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=1)
        self.menu = Menu(self.master, self)
        self.config(menu=self.menu)
        self.protocol("WM_DELETE_WINDOW", self.dialog_box)
        self.bind("<Control-s>", self.stop)

    def dialog_box(self):
        if askyesno(title="Quit", message="Do you want to quit?"):
            self.main_frame.exit()
            self.destroy()

    def new_game(self):
        self.main_frame.new_game()
        print('new game')

    def save(self):
        pass

    def load(self):
        pass

    def pause(self):
        print('pause')
        self.main_frame.run = False

    def start(self):
        self.main_frame.run = True

    def stop(self, event):
        pass

    def tick(self):
        if self.main_frame.run:
            self.main_frame.game()
        self.after(30, self.tick)


if __name__ == '__main__':
    app = GameApp()
    app.new_game()
    app.tick()
    app.mainloop()
