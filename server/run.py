from .app.ui import GameApp


if __name__ == '__main__':
    app = GameApp()
    app.new_game()
    app.tick()
    app.mainloop()
