from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.core.window import Window


class BallWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__pos = (0.5, 0.5)
        self.radius = 0.05
        self.color = (0.1, 0.1, 0.1, 1.0)

        with self.canvas:
            self.ellipse = Ellipse(pos=(0.0, 0.0), size=(0.0, 0.0))

    def set_pos(self, new_pos):
        self.__pos = new_pos
        self.update()

    def get_pos(self):
        return self.__pos

    def update(self):
        pos = (self.pos[0] * Window.size[0], self.pos[1] * Window.size[1])
        diameter = 2.0 * self.radius * Window.size[0]
        ball_size = (diameter, diameter)
        self.ellipse.pos = (pos[0] - 0.5 * ball_size[0], pos[1] - 0.5 * ball_size[1])
        self.ellipse.size = ball_size
