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
        self.control_ball = Ball(Vec2D(0.0, 0.0), 0.5)
        self.control_ball.set_color(0.1, 0.1, 0.1, 1.0)
        self.control_ball.body.mass = 20

        self.swing_range = 4.0
        self.swinging_ball = Ball(Vec2D(-4.0, 0.0), 1.0)
        self.swinging_ball.set_color(0.1, 0.1, 0.1, 1.0)
        self.swinging_ball.body.is_gravity_affected = True
        self.swinging_ball.body.is_drag_affected = True

        self.line_widget = LineWidget()

    def move(self, delta_pos: Vec2D, dt=1):
        self.control_ball.body.pos += delta_pos
        self.control_ball.body.vel = delta_pos / dt

    def update(self):
        from scene_data import SceneData
        screen_size = Vec2D(Window.size[0], Window.size[1])
        line_pos1 = SceneData.main_camera.world_to_clip(self.control_ball.body.pos) * screen_size
        line_pos2 = SceneData.main_camera.world_to_clip(self.swinging_ball.body.pos) * screen_size
        self.line_widget.line.points.clear()
        self.line_widget.line.points.extend([line_pos1.x, line_pos1.y, line_pos2.x, line_pos2.y])
