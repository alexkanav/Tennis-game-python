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
        self.z = -1
        self.t_t = time()
        self.live_ball = time()
        self.ball_id = canvas.create_oval(x - self.r, y - self.r, x + self.r, y + self.r, fill=self.color)

    def move_ball(self, racket_1, racket_2, balls: list):
        racket = racket_1 if self.x < WIDTH // 2 else racket_2

        def racket_bounce(racket):
            # direction of ball movement
            ball_direction, edge = (1, WIDTH) if self.dx > 0 else (-1, 0)

            # direction of racket movement
            racket_direction = 1 if racket.rx <= racket.rx_last else -1

            if self.x * racket_direction <= racket.rx * racket_direction:
                self.z = racket_direction * ball_direction
            else:
                if self.z == racket_direction * ball_direction and (
                        racket.ry < self.y < racket.ry + racket.rack_length):
                    self.dx = (self.dx + ((racket.rx_last - racket.rx) * racket_direction) * ball_direction
                               if (racket.rx_last - racket.rx) * racket_direction < 10
                               else self.dx + 10)
                    self.dx = -self.dx
                    self.z = racket_direction * ball_direction * -1
                else:
                    self.z = racket_direction * ball_direction * -1

        def rebound_from_the_side():
            # from a vertical
            if (self.x + self.r + self.dx >= WIDTH or self.x - self.r + self.dx <= 0) \
                    and not (HEIGHT - GOAL_SIZE) / 2 < self.y < HEIGHT - (HEIGHT - GOAL_SIZE) / 2:
                self.dx = -self.dx

            # from a horizontal
            if self.y + self.r + self.dy >= HEIGHT or self.y - self.r + self.dy <= 0:
                self.dy = -self.dy

        def bounce_from_ball():
            for ball in balls:
                if ball is not self:
                    if ball.x - self.r < self.x < ball.x + self.r and ball.y - self.r < self.y < ball.y + self.r:
                        if time() - self.t_t > 0.5:
                            self.dx = -self.dx
                            self.dy = -self.dy
                        self.t_t = time()

        racket_bounce(racket)
        rebound_from_the_side()
        bounce_from_ball()
        self.x = int(self.x + self.dx)
        self.y = int(self.y + self.dy)

    def show_ball(self):
        self.canvas.coords(self.ball_id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
        self.dy += 0.2
        if self.dx != 0:
            self.dx -= 0.03 * self.dx / abs(self.dx)
        if self.dy != 0:
            self.dy -= 0.05 * self.dy / abs(self.dy)

    def goal(self):
        if (HEIGHT - GOAL_SIZE) / 2 < self.y < HEIGHT - (HEIGHT - GOAL_SIZE) / 2:
            if self.x + self.r >= WIDTH:
                return 1
            elif self.x - self.r <= 0:
                return 2

        return 0
