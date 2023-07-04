import math
import os
from itertools import combinations

from kivy.core.audio import SoundLoader

from ball import Ball
from vector import Vec2D

sound_path = os.path.join(os.getcwd(), 'source', 'assets', 'sounds', 'game_ball_tap.mp3')


class PhysicsEngine:
    GRAVITY_CONST = 100.0
    GRAVITY_DIR = Vec2D(0.0, -1.0)

    def __init__(self, scene):
        self.__bodies = []
        self.scene = scene
        self.player = scene.data.player
        self.control_ball = None
        self.sound = SoundLoader.load(sound_path)
        if scene.data.player:
            self.control_ball = scene.data.player.control_ball.body
            self.swing_ball = scene.data.player.swinging_ball.body
            self.swing_range = scene.data.player.swing_range

    def add_body(self, new_body: Ball.Body):
        self.__bodies.append(new_body)

    def remove_body(self, body: Ball.Body):
        self.__bodies.remove(body)

    def update(self, dt: float):
        self.calculate_forces()
        self.update_velocities(dt)
        self.handle_collisions()
        self.advance_bodies(dt)

    def advance_bodies(self, dt: float):
        for body in self.__bodies:
            if body is not self.control_ball:
                body.pos += dt * body.vel
            if body.is_drag_affected:
                body.vel -= body.vel * dt * 0.7

    def calculate_forces(self):
        # gravity
        for body in self.__bodies:
            body.force = Vec2D(0.0, 0.0)
            if body.is_gravity_affected is True:
                body.force += PhysicsEngine.GRAVITY_CONST * PhysicsEngine.GRAVITY_DIR
        if self.player:
            # swing ball - string pull force
            if self.swing_ball.pos.dist(self.control_ball.pos) >= self.swing_range:
                swing_to_control = self.control_ball.pos - self.swing_ball.pos
                pull_dir = swing_to_control.normalize()
                string_tensity_sq = math.pow(swing_to_control.length() - self.swing_range, 2)
                pull_force_s = PhysicsEngine.GRAVITY_CONST * (1.0 + string_tensity_sq)
                pull_force = pull_dir * pull_force_s
                self.swing_ball.force += pull_force

    def update_velocities(self, dt: float):
        for body in self.__bodies:
            body.vel += (body.force*(1.0/body.mass)) * dt

            if body.vel.length() > Ball.Body.MAX_SPEED:
                body.vel = body.vel.normalize() * Ball.Body.MAX_SPEED

    def handle_collisions(self):
        def change_velocities(body1, body2):
            distance_vect = body1.pos - body2.pos
            distance_vect_mag = distance_vect.length()
            min_distance = body1.rad + body2.rad
            distance_correction = (min_distance - distance_vect_mag) / 2.0

            correction_vector = distance_vect.normalize() * distance_correction * 1.00001
            body2.pos -= correction_vector
            body1.pos += correction_vector

            theta = math.acos(distance_vect.normalize().x)
            if distance_vect.y < 0:
                theta += (math.pi - theta) * 2
            sine = math.sin(theta)
            cosine = math.cos(theta)

            vTemp = [Vec2D(), Vec2D()]
            vTemp[0].x = cosine * body1.vel.x + sine * body1.vel.y
            vTemp[0].y = cosine * body1.vel.y - sine * body1.vel.x
            vTemp[1].x = cosine * body2.vel.x + sine * body2.vel.y
            vTemp[1].y = cosine * body2.vel.y - sine * body2.vel.x

            vFinal = [Vec2D(), Vec2D()]
            vFinal[0].x = ((body1.mass - body2.mass) * vTemp[0].x + 2 * body2.mass * vTemp[1].x) / (body1.mass + body2.mass)
            vFinal[0].y = vTemp[0].y
            vFinal[1].x = ((body2.mass - body1.mass) * vTemp[1].x + 2 * body1.mass * vTemp[0].x) / (body1.mass + body2.mass)
            vFinal[1].y = vTemp[1].y

            body1.vel.x = cosine * vFinal[0].x - sine * vFinal[0].y
            body1.vel.y = cosine * vFinal[0].y + sine * vFinal[0].x
            body2.vel.x = cosine * vFinal[1].x - sine * vFinal[1].y
            body2.vel.y = cosine * vFinal[1].y + sine * vFinal[1].x

        pairs = combinations(self.__bodies, 2)
        for i, j in pairs:
            if i.overlaps(j):
                self.sound.play()
                if self.player:
                    self.sound.play()
                    if i is self.control_ball or j is self.control_ball:
                        if not (i is self.swing_ball or j is self.swing_ball):
                            self.scene.on_player_hit()
                    if i is self.swing_ball or j is self.swing_ball:
                        self.scene.data.score += 10.0

                change_velocities(i, j)

    def clear(self):
        self.__bodies.clear()
        self.player = None
        self.control_ball = None
        self.swing_ball = None