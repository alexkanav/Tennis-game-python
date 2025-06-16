import tkinter as tk


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

