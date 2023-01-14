from vector import Vec2D

class Player:
    def __init__(self):
        from ball import Ball
        self.control_ball = Ball(Vec2D(0.0, 0.0), 0.5)
        self.control_ball.set_color(0.1, 0.1, 0.1, 1.0)
        self.control_ball.body.mass = float('inf')

        self.swing_range = 3.0
        self.swinging_ball = Ball(Vec2D(-4.0, 0.0), 1.0)
        self.swinging_ball.set_color(0.1, 0.1, 0.1, 1.0)
        self.swinging_ball.body.is_gravity_affected = True

