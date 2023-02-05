from ball import Ball
from vector import Vec2D
import math

class PhysicsEngine:

    GRAVITY_CONST = 50.0
    GRAVITY_DIR = Vec2D(0.0, -1.0)

    def __init__(self):
        from game_screen import GameScreen
        self.__bodies = []

        self.player = GameScreen.player
        self.control_ball = GameScreen.player.control_ball.body
        self.swing_ball = GameScreen.player.swinging_ball.body
        self.swing_range = GameScreen.player.swing_range

    def add_body(self, new_body: Ball.Body):
        self.__bodies.append(new_body)

    def update(self, dt: float):
        #dt = 0.01
        self.calculate_forces(dt)
        self.update_velocities(dt)
        self.advance_bodies(dt)

    def advance_bodies(self, dt: float):
        for body in self.__bodies:
            body.pos += dt * body.vel
            if body.is_drag_affected:
                body.vel -= body.vel * dt * 0.5

    def calculate_forces(self, dt: float):
        # gravity
        for body in self.__bodies:
            body.force = Vec2D(0.0, 0.0)
            if body.is_gravity_affected is True:
                body.force += PhysicsEngine.GRAVITY_CONST * PhysicsEngine.GRAVITY_DIR

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
