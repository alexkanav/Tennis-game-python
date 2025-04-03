import tkinter as tk
from tkinter.messagebox import askyesno
import time
import threading

from client_config import *
from client_socket import ClientSocket


class Racket:
    def __init__(self, canvas, color: str, x: int, y: int, length: int = RACKET_LENGTH):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.length = length
        self.racket_id = canvas.create_line(x, y, x, y + length, fill=color, width=5)

    def move(self, event):
        self.y = event.y
        self.x = event.x if event.x > 500 else 500

    def show(self):
        self.canvas.coords(self.racket_id, self.x, self.y, self.x, self.y + self.length)


class GameField(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, background='yellow')
        self.pack(expand=1, fill='both')
        self.create_line(5, 0, 5, (HIGHT - GOAL_SIZE) // 2, width=8, fill='blue')
        self.create_line(5, HIGHT - (HIGHT - GOAL_SIZE) // 2, 5, HIGHT, width=8, fill='blue')
        self.create_line(WIDTH - 5, 0, WIDTH - 5, (HIGHT - GOAL_SIZE) // 2, width=8, fill='blue')
        self.create_line(WIDTH - 5, HIGHT - (HIGHT - GOAL_SIZE) // 2, WIDTH - 5, HIGHT, width=8, fill='blue')
        self.racket_1 = Racket(self, 'black', 100, 200)
        self.racket_2 = Racket(self, 'red', 700, 300)
        self.balls_on_the_field = []

    def show_rackets(self):
        self.racket_1.show()
        self.racket_2.show()

    def show_balls(self, balls: list[tuple]):
        for ball in self.balls_on_the_field:
            self.delete(ball)
        self.balls_on_the_field.clear()

        for ball in balls:
            self.balls_on_the_field.append(
                self.create_oval(ball[1] - BALL_RADIUS, ball[2] - BALL_RADIUS, ball[1] + BALL_RADIUS,
                                 ball[2] + BALL_RADIUS, fill=ball[0]))


class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='brown')

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
                self.score_label.config(text=f'{self.score_1} : {self.score_2}')
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
            rack_coord, balls_coord = self.conn.receive().split(':')
            self.game_field.racket_2.x, self.game_field.racket_2.y = map(int, rack_coord.split('/'))
            self.game_field.show_rackets()
            self.game_field.show_balls(eval(balls_coord))

    def close_connection(self):
        self.conn.close()
        self.game_running = False


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tennis')
        self.iconbitmap('racket.ico')
        self.geometry(f'{str(WIDTH)}x{str(HIGHT + 20)}')
        self.main_frame = MainFrame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=1)
        self.protocol("WM_DELETE_WINDOW", self.dialog_box)


    def start(self):
        self.main_frame.start_game()

    def tick(self):
        self.main_frame.game()
        self.after(30, self.tick)

    def dialog_box(self):
        if askyesno(title="Quit", message="Do you want to quit?"):
            self.main_frame.close_connection()
            self.destroy()


if __name__ == '__main__':
    app = GameApp()
    app.start()
    app.tick()
    app.mainloop()
