from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import *

from vector import Vec2D
from ball import Ball

class LineWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.width = 1.5
        self.color = (0.1, 0.1, 0.1, 1.0)

        with self.canvas:
            self.line = Line(pos=[], width=self.width)


class Player:
    def __init__(self):
        self.d_pos = Vec2D()
        self.control_ball = Ball(Vec2D(0.0, 0.0), 0.5)
        self.control_ball.set_color(0.1, 0.1, 0.1, 1.0)
        self.control_ball.body.mass = 10000000

        self.swing_range = 4.0
        self.swinging_ball = Ball(Vec2D(-4.0, 0.0), 1.0)
        self.swinging_ball.set_color(0.1, 0.1, 0.1, 1.0)
        self.swinging_ball.body.is_gravity_affected = True
        self.swinging_ball.body.is_drag_affected = True

        self.line_widget = LineWidget()



    def move(self, vector: Vec2D):
        self.d_pos = vector
        self.control_ball.body.pos += self.d_pos

    def update(self):
        from game_screen import GameData
        screen_size = Vec2D(Window.size[0], Window.size[1])
        line_pos1 = GameData.main_camera.world_to_clip(self.control_ball.body.pos) * screen_size
        line_pos2 = GameData.main_camera.world_to_clip(self.swinging_ball.body.pos) * screen_size
        self.line_widget.line.points.clear()
        self.line_widget.line.points.extend([line_pos1.x, line_pos1.y, line_pos2.x, line_pos2.y])
