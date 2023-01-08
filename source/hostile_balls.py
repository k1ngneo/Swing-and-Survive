from source.ball import Ball
from source.vector import Vec2D
import game_screen


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
        cam = game_screen.GameScreen.main_camera
        for ball in self.hostile_balls:
            side_choice = [-1, 1]
            random_x_side = random.choice(side_choice)
            random_height = random.uniform(cam.pos.y - 0.5 * cam.size * cam.hw_ratio,
                                           cam.pos.y + 0.5 * cam.size * cam.hw_ratio)
            ball.body.pos = Vec2D(cam.pos.x + 0.5 * cam.size * random_x_side, random_height)

    def set_velocity(self):
        for ball in self.hostile_balls:
            ball.body.vel = Vec2D(0.3, 0.3)

    def despawn_balls(self):
        cam = game_screen.GameScreen.main_camera
        for ball in self.hostile_balls:
            left_border = cam.pos.x - 0.5 * cam.size
            right_border = cam.pos.x + 0.5 * cam.size
            top_border = cam.pos.y + 0.5 * cam.size * cam.hw_ratio
            bottom_border = cam.pos.y - 0.5 * cam.size * cam.hw_ratio

            if ball.body.pos.x < left_border or ball.body.pos.x > right_border:
                despawn_ball()
            elif ball.body.pos.y < bottom_border or ball.body.pos.y > top_border:
                despawn_ball()
