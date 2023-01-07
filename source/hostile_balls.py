from source.ball import Ball
from source.vector import Vec2D


class HostileBalls:

    def __init__(self, amount):
        self.hostile_balls = []
        i = 0
        while i < amount:
            new_ball = Ball(Vec2D(0, 0), .5)
            new_ball.set_color(1, 1, 0, 1)
            self.hostile_balls.append(new_ball)
            i += 1
        self.set_velocity()

    def set_position(self):
        pass

    def set_velocity(self):
        for ball in self.hostile_balls:
            ball.body.vel = Vec2D(2, 5)

    def add_ball(self):
        pass

    def remove_ball(self):
        pass
