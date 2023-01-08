from source.ball import Ball
from source.vector import Vec2D


class HostileBalls:

    def __init__(self, amount):
        self.hostile_balls = []
        i = 0
        while i < amount:
            new_ball = Ball(Vec2D(0, 0), .25)
            new_ball.set_color(1, 1, 0, 1)
            self.hostile_balls.append(new_ball)
            i += 1
        self.set_position()
        self.set_velocity()

    def set_position(self):
        import random
        from game_screen import GameScreen
        cam = GameScreen.main_camera
        for ball in self.hostile_balls:
            side_choices = [-1, 1]
            height_choice = random.uniform(cam.size * cam.hw_ratio * 0.5, -cam.size * cam.hw_ratio * 0.5)
            x_side_choice = random.choice(side_choices)
            y_side_choice = random.choice(side_choices)
            ball.body.pos = Vec2D(cam.size * 0.5 * x_side_choice, height_choice * 0.5 * y_side_choice)

    def set_velocity(self):
        for ball in self.hostile_balls:
            ball.body.vel = Vec2D(0.3, 0.3)

    def despawn_balls(self):
        pass
