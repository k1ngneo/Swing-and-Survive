from source.ball import Ball
from source.vector import Vec2D
from source.scene_data import SceneData
import random
import math


class HostileBallsSpawner:
    spawn_radius = math.sqrt(SceneData.main_camera.size ** 2 + (
                SceneData.main_camera.size * SceneData.main_camera.hw_ratio) ** 2) * 0.5 + 1

    def __init__(self, scene, amount, balls_speed=4):
        self.hostile_balls = []
        self.cam = SceneData.main_camera
        self.balls_speed = balls_speed
        self.scene = scene
        i = 0
        while i < amount:
            new_ball = Ball(Vec2D(0, 0), .5)
            new_ball.set_color(.29, 0.05, 0.11, 1)
            self.hostile_balls.append(new_ball)
            i += 1
        self.set_position()
        self.set_velocity()

    def set_position(self):
        balls_to_remove = set()
        for i in range(len(self.hostile_balls)):
            angle = random.uniform(0, 2 * math.pi)
            self.hostile_balls[i].body.pos = Vec2D(math.cos(angle) * self.spawn_radius + self.cam.pos.x,
                                                   math.sin(angle) * self.spawn_radius + self.cam.pos.y)
            # detect balls spawned on top of each other
            for j in range(i):
                len_between_vectors = self.hostile_balls[i].body.pos.dist(self.hostile_balls[j].body.pos)
                if len_between_vectors < self.hostile_balls[i].body.rad + self.hostile_balls[j].body.rad:
                    balls_to_remove.add(self.hostile_balls[i])
        # detect balls spawned on already existing balls
        for ball in self.hostile_balls:
            for k in range(len(self.scene.data.balls)):
                len_between_vectors = ball.body.pos.dist(self.scene.data.balls[k].body.pos)
                if len_between_vectors < ball.body.rad + self.scene.data.balls[k].body.rad:
                    balls_to_remove.add(ball)
        # remove balls
        for ball in balls_to_remove:
            if ball in self.hostile_balls:
                self.hostile_balls.remove(ball)

    def set_velocity(self):
        for ball in self.hostile_balls:
            destination_height = random.uniform(self.cam.size * self.cam.hw_ratio * -0.25, self.cam.size * self.cam.hw_ratio * 0.25)
            destination_pos = Vec2D(self.cam.pos.x, destination_height)
            ball.body.vel = Vec2D(destination_pos.x - ball.body.pos.x, destination_pos.y - ball.body.pos.y).normalize()
            ball.body.vel *= self.balls_speed
