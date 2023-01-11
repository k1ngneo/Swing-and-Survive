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
