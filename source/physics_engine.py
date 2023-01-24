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
                body.vel -= body.vel * dt * 0.99999

    def calculate_forces(self, dt: float):
        # gravity
        for body in self.__bodies:
            body.force = Vec2D(0.0, 0.0)
            if body.is_gravity_affected is True:
                body.force += PhysicsEngine.GRAVITY_CONST * PhysicsEngine.GRAVITY_DIR

        # swing ball - string pull force
        # swing ball relative pos to control ball
        #sw_pos = self.swing_ball.pos - self.control_ball.pos
        #pull_dir = -1.0 * sw_pos.normalize()
        #pull_force = self.player.d_pos * self.swing_ball.mass / math.pow(dt, 2)
        #self.player.d_pos = 0.0

        #overshoot = sw_pos.length() - self.swing_range

        # if overshoot >= 0.0:
        #     self.swing_ball.pos += overshoot * pull_dir
        #     pull_force = pull_dir * pull_force
        #     self.swing_ball.force += pull_force


    def update_velocities(self, dt: float):
        for body in self.__bodies:
            body.vel += (body.force*(1.0/body.mass)) * dt

            c_sw_pos = self.swing_ball.pos - self.control_ball.pos
            f_sw_pos = (self.swing_ball.pos + dt * self.swing_ball.vel) - (self.control_ball.pos + dt * self.player.d_pos)
            if f_sw_pos.length() >= self.swing_range:
                pull_dir = -1.0 * c_sw_pos.normalize()
                overshoot = c_sw_pos.length() - self.swing_range
                self.swing_ball.pos += overshoot * pull_dir

                vel_counter = (-1.0 * pull_dir).dot(self.swing_ball.vel.normalize()) * self.swing_ball.vel.length()
                self.swing_ball.vel += vel_counter * pull_dir

            if body.vel.length() > Ball.Body.MAX_SPEED:
                body.vel = body.vel.normalize() * Ball.Body.MAX_SPEED
