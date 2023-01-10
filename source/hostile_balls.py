from ball import Ball
from vector import Vec2D
import game_screen
import random
import math


class HostileBalls:
    spawn_radius = math.sqrt(game_screen.GameScreen.main_camera.size ** 2 + (
                game_screen.GameScreen.main_camera.size * game_screen.GameScreen.main_camera.hw_ratio) ** 2) * 0.5 - 3

    def __init__(self, amount):
        self.hostile_balls = []
        i = 0
        while i < amount:
            new_ball = Ball(Vec2D(0, 0), .25)
            new_ball.set_color(1, 0, 0, 1)
            self.hostile_balls.append(new_ball)
            i += 1
        self.set_position()
        self.set_velocity()

    def set_position(self):
        balls_to_remove = set()
        cam = game_screen.GameScreen.main_camera
        for i in range(len(self.hostile_balls)):
            angle = random.uniform(0, 2 * math.pi)
            self.hostile_balls[i].body.pos = Vec2D(math.cos(angle) * self.spawn_radius + cam.pos.x,
                                                   math.sin(angle) * self.spawn_radius + cam.pos.y)
            # detect balls spawned on top of each other
            for j in range(i):
                len_between_vectors = self.hostile_balls[i].body.pos.dist(self.hostile_balls[j].body.pos)
                if len_between_vectors < self.hostile_balls[i].body.rad + self.hostile_balls[j].body.rad:
                    balls_to_remove.add(self.hostile_balls[i])
        # detect balls spawned on already existing balls
        for ball in self.hostile_balls:
            for k in range(len(game_screen.GameScreen.balls)):
                len_between_vectors = ball.body.pos.dist(game_screen.GameScreen.balls[k].body.pos)
                if len_between_vectors < ball.body.rad + game_screen.GameScreen.balls[k].body.rad:
                    balls_to_remove.add(ball)
        # remove balls
        for ball in balls_to_remove:
            if ball in self.hostile_balls:
                self.hostile_balls.remove(ball)

    def set_velocity(self):
        for ball in self.hostile_balls:
            ball.body.vel = -1 * ball.body.pos
