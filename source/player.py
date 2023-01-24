from vector import Vec2D

class Player:
    def __init__(self):
        from ball import Ball
        self.d_pos = Vec2D()
        self.control_ball = Ball(Vec2D(0.0, 0.0), 0.5)
        self.control_ball.set_color(0.1, 0.1, 0.1, 1.0)
        self.control_ball.body.mass = float('inf')

        self.swing_range = 5.0
        self.swinging_ball = Ball(Vec2D(-4.0, 0.0), 1.0)
        self.swinging_ball.set_color(0.1, 0.1, 0.1, 1.0)
        self.swinging_ball.body.is_gravity_affected = True
        self.swinging_ball.body.is_drag_affected = True

    def move(self, vector: Vec2D):
        self.d_pos = vector
        self.control_ball.body.pos += self.d_pos