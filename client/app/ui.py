from tkinter.messagebox import askyesno
import tkinter as tk

from .main import MainFrame
from client.config import WIDTH, HEIGHT


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tennis')
        self.iconbitmap('client/assets/racket.ico')
        self.geometry(f'{str(WIDTH)}x{str(HEIGHT + 20)}')
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

