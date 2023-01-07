from source.ball import Ball
from source.vector import Vec2D


class HostileBalls:
    hostile_balls = []

    def __init__(self, amount):
        i = 0
        while i < amount:
            new_ball = Ball(Vec2D(0, 0), .5)
            new_ball.set_color(1, 0, 0, 1)
            self.hostile_balls.append(new_ball)
            i += 1

    def set_position(self):
        pass

    def set_velocity(self):
        pass

    def add_ball(self):
        pass

    def remove_ball(self):
        pass
