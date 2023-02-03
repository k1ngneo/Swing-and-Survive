from ball import Ball
from vector import Vec2D
import math

class PhysicsEngine:

    GRAVITY_CONST = 70.0
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
            body.speed = body.vel.length()

            if body.speed > Ball.Body.MAX_SPEED:
                body.vel = body.vel.normalize() * Ball.Body.MAX_SPEED

        # keeping swinging ball in the range
        c_sw_pos = self.swing_ball.pos - self.control_ball.pos
        f_sw_pos = (self.swing_ball.pos + dt * self.swing_ball.vel) - (self.control_ball.pos + dt * self.player.d_pos)
        if f_sw_pos.length() >= self.swing_range:
            pull_dir = -1.0 * c_sw_pos.normalize()
            overshoot = c_sw_pos.length() - self.swing_range
            self.swing_ball.pos += overshoot * pull_dir

            cosine = (-1.0 * pull_dir).dot(self.swing_ball.vel.normalize())
            if cosine <= 0.5 * math.pi:
                vel_counter = cosine * self.swing_ball.vel.length()
                self.swing_ball.vel += vel_counter * pull_dir
                self.swing_ball.speed = self.swing_ball.vel.length()

            angular_vel = 1.0
            if c_sw_pos.x >= 0.0 and c_sw_pos.y >= 0.0:
                if self.swing_ball.vel.y < 0.0:
                    angular_vel = -1.0
            elif c_sw_pos.x < 0.0 and c_sw_pos.y >= 0.0:
                if self.swing_ball.vel.y > 0.0:
                    angular_vel = -1.0
            elif c_sw_pos.x < 0.0 and c_sw_pos.y < 0.0:
                if self.swing_ball.vel.y > 0.0:
                    angular_vel = -1.0
            elif c_sw_pos.x >= 0.0 and c_sw_pos.y < 0.0:
                if self.swing_ball.vel.y < 0.0:
                    angular_vel = -1.0

            angular_vel = self.swing_ball.speed * angular_vel
            angular_pos = math.acos(c_sw_pos.x / c_sw_pos.length())
            if c_sw_pos.y < 0.0:
                # maybe it should not be exactly PI
                angular_pos += math.pi

            angular_pos += self.swing_ball.speed * dt
            c_sw_pos.x = math.cos(angular_pos) * self.swing_range
            c_sw_pos.y = math.sin(angular_pos) * self.swing_range

            self.swing_ball.vel = self.control_ball.pos + c_sw_pos - self.swing_ball.pos

        for body in self.__bodies:
            if body.vel.length() > Ball.Body.MAX_SPEED:
                body.vel = body.vel.normalize() * Ball.Body.MAX_SPEED