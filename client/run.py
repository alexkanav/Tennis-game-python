from .app import GameApp


if __name__ == '__main__':
    app = GameApp()
    app.start()
    app.tick()
    app.mainloop()
