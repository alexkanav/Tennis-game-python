from client.config import RACKET_LENGTH


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
