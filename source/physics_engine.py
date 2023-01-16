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
        """Detect and handle any collisions between the balls"""
        def change_velocities(body1, body2):
            # m1, m2 = ball_body_1.mass, ball_body_2.mass
            # M = m1 + m2
            # r1, r2 = ball_body_1.rad, ball_body_2.rad
            # v1, v2 = ball_body_1.vel.length(), ball_body_2.vel.length()
            # #u1 = (v1 - 2 * m2 / M) * Vec2D(v1 - v2, ball_body_1.pos - ball_body_2.pos) * (1 / (ball_body_1.pos - ball_body_2.pos).length()) * (ball_body_1.pos - ball_body_2.pos)
            # #u2 = (v2 - 2 * m1 / M) * Vec2D(v2 - v1, ball_body_2.pos - ball_body_1.pos) * (1 / (ball_body_2.pos - ball_body_1.pos).length()) * (ball_body_2.pos - ball_body_1.pos)
            # u1 = (v1 * (m1 - m2) + 2 * m2 * v2) / m1 + m2
            # u2 = ()
            # ball_body_1.vel = u1
            # ball_body_2.vel = u2
            distanceVect = body1.pos - body2.pos
            distanceVectMag = distanceVect.length()
            minDistance = body1.rad + body2.rad
            distanceCorrection = (minDistance - distanceVectMag) / 2.0

            correctionVector = distanceVect.normalize() * distanceCorrection
            body2.pos += correctionVector
            body1.pos -= correctionVector

            theta = math.acos(distanceVect.x)
            if distanceVect.y < 0:
                theta += math.pi

            sine = math.sin(theta)
            cosine = math.cos(theta)

            bTemp = [Vec2D(), Vec2D()]

            bTemp[1].x = cosine * distanceVect.x + sine * distanceVect.y
            bTemp[1].y = cosine * distanceVect.y - sine * distanceVect.x

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

            bTemp[0].x += vFinal[0].x
            bTemp[1].x += vFinal[1].x

            bFinal = [Vec2D(), Vec2D()]

            bFinal[0].x = cosine * bTemp[0].x - sine * bTemp[0].y
            bFinal[0].y = cosine * bTemp[0].y + sine * bTemp[0].x
            bFinal[1].x = cosine * bTemp[1].x - sine * bTemp[1].y
            bFinal[1].y = cosine * bTemp[1].y + sine * bTemp[1].x

            # body2.pos.x = body1.pos.x + bFinal[1].x
            # body2.pos.y = body1.pos.y + bFinal[1].y
            #
            # body1.pos += bFinal[0]

            body1.vel.x = cosine * vFinal[0].x - sine * vFinal[0].y
            body1.vel.y = cosine * vFinal[0].y + sine * vFinal[0].x
            body2.vel.x = cosine * vFinal[1].x - sine * vFinal[1].y
            body2.vel.y = cosine * vFinal[1].y + sine * vFinal[1].x

        pairs = combinations(self.__bodies, 2)
        for i, j in pairs:
            if i.overlaps(j):
                change_velocities(i, j)
