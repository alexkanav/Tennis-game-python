from random import choice
from time import time

from server_part.config import WIDTH, HEIGHT, GOAL_SIZE, BALL_RADIUS


class Ball:
    def __init__(self, canvas, dx: int, dy: int, x: int, y: int):
        self.canvas = canvas
        self.color = choice(['blue', 'green', 'red', 'brown', 'yellow'])
        self.x = x
        self.y = y
        self.r = BALL_RADIUS
        self.dx = dx
        self.dy = dy
        self.z = 0
        self.t_t = time()
        self.live_ball = time()
        self.ball_id = canvas.create_oval(x - self.r, y - self.r, x + self.r, y + self.r, fill=self.color)

    def move_ball(self, racket_1, racket_2, balls: list):
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
                    if time() - self.t_t > 0.5:
                        self.dx = -self.dx
                        self.dy = -self.dy
                    self.t_t = time()
            self.dy -= 0.2

    def show_ball(self):
        self.canvas.coords(self.ball_id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
        if self.dx != 0:
            self.dx -= 0.03 * self.dx / abs(self.dx)
        if self.dy != 0:
            self.dy -= 0.05 * self.dy / abs(self.dy)

    def goal(self, racket_1, racket_2):
        if self.x + self.r >= WIDTH and not racket_2.ry <= self.y <= racket_2.ry + racket_2.rack_length:
            if (HEIGHT - GOAL_SIZE) / 2 < self.y < HEIGHT - (HEIGHT - GOAL_SIZE) / 2:
                return 1
        elif self.x - self.r <= 0 and not racket_1.ry <= self.y <= racket_1.ry + racket_1.rack_length:
            if (HEIGHT - GOAL_SIZE) / 2 < self.y < HEIGHT - (HEIGHT - GOAL_SIZE) / 2:
                return 2
        return 0

