from ball import Ball
from vector import Vec2D

class PhysicsEngine:
    def __init__(self):
        self.__bodies = []
        self.__forces = []

    def add_body(self, new_body: Ball.Body):
        self.__bodies.append(new_body)

    def advance_bodies(self, dt: float):
        for body in self.__bodies:
            body.pos += dt * body.vel

    def calculate_forces(self, dt: float):
        self.__forces = [Vec2D] * len(self.__bodies)

        for i in range(len(self.__bodies)):
            pass