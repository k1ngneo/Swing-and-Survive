import math
from itertools import combinations

from ball import Ball
from vector import Vec2D


class PhysicsEngine:
    GRAVITY_CONST = 0.01
    GRAVITY_DIR = Vec2D(0.0, -1.0)

    def __init__(self):
        self.__bodies = []
        self.__forces = []

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
            body.pos += dt * body.vel

    def calculate_forces(self):
        self.__forces = [Vec2D] * len(self.__bodies)
        for i in range(len(self.__bodies)):
            self.__forces[i] = Vec2D(0.0, 0.0)

        # gravity
        for i in range(len(self.__bodies)):
            if self.__bodies[i].is_gravity_affected is True:
                self.__forces[i] += PhysicsEngine.GRAVITY_CONST * PhysicsEngine.GRAVITY_DIR

    def update_velocities(self, dt: float):
        for i in range(len(self.__bodies)):
            self.__bodies[i].vel += (self.__forces[i] * (1.0 / self.__bodies[i].mass)) * dt

    def handle_collisions(self):
        def change_velocities(body1, body2):
            distance_vect = body1.pos - body2.pos
            distance_vect_mag = distance_vect.length()
            min_distance = body1.rad + body2.rad
            distance_correction = (min_distance - distance_vect_mag) / 2.0

            correction_vector = distance_vect.normalize() * distance_correction * 1.00001
            body2.pos -= correction_vector
            body1.pos += correction_vector
            assert min_distance - (body1.pos - body2.pos).length() <= 0

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
                change_velocities(i, j)
