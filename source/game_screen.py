from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import *
from kivy.uix.screenmanager import Screen

from scene import Scene


class GameScreen(Screen):
    __ball_spawn_dt = 0.0
    ball_spawn_interval = 2
    amount_of_balls = 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scene = Scene(self)

        with self.canvas:
            Color(0.1, 0.3, 0.3, 1)
            self.background = Rectangle(pos=(0, 0))
            Color(0.1, 0.1, 0.1, 1.0)
            self.line = Line(points=[], width=1.5)

        self.scene.add_player()
        Clock.schedule_interval(self.update, 1.0 / 120.0)

    def on_size(self, *args):
        self.background.size = Window.size
        self.scene.data.main_camera.update()

    def update(self, dt):
        if self.manager.current == 'game':
            self.scene.update(dt)

    def on_touch_down(self, touch):
        self.scene.on_touch_down(touch)

    def on_touch_move(self, touch):
        self.scene.on_touch_move(touch)
