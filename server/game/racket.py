class Racket:
    def __init__(self, canvas, rx: int, ry: int, length: int, color: str):
        self.canvas = canvas
        self.rx = rx
        self.ry = ry
        self.rx_last = rx
        self.rack_length = length
        self.racket_id = canvas.create_line(rx, ry, rx, ry + length, fill=color, width=5)

    def show(self, event=None):
        self.rx_last = self.rx
        self.canvas.coords(self.racket_id, self.rx, self.ry, self.rx, self.ry + self.rack_length)
        if event:
            self.rx = event.x if event.x < 300 else 300
            self.ry = event.y

