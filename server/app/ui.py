import os
from tkinter.messagebox import askyesno

from server import tk
from .main import MainFrame
from .menu import Menu
from server.config import WIDTH, HEIGHT


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap('server/assets/racket.ico')
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
