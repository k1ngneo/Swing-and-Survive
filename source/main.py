__version__ = "0.1"
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.metrics import *
from kivy.properties import Clock


class MainWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ball_size = dp(50)
        with self.canvas:
            self.ball = Ellipse(pos=self.center, size=(self.ball_size, self.ball_size))
        Clock.schedule_interval(self.update, 0.005)

    def on_size(self, *args):
        self.ball.pos = (self.center_x - self.ball_size/2, self.center_y-self.ball_size/2)

    def update(self, dt):
        x, y = self.ball.pos
        self.ball.pos = (x+2, y)


class BallCrushApp(App):
    pass


BallCrushApp().run()
