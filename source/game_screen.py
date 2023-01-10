from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import *
from functools import partial
from kivy.uix.screenmanager import Screen

import hostile_balls
from camera import Camera
from vector import Vec2D
from ball import Ball
from physics_engine import PhysicsEngine


class GameScreen(Screen):
    main_camera = Camera(pos=Vec2D(0.0, 0.0), size=7.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__physics_engine = PhysicsEngine()
        self.__balls = []
        self.__last_touch = 0

        with self.canvas:
            Color(0.1, 0.3, 0.3, 1)
            self.background = Rectangle(pos=(0, 0))

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(partial(self.spawn_balls_over_time, 2), 2)

        self.__main_ball = Ball(Vec2D(0.0, 0.0), 0.5)
        self.__main_ball.set_color(0.7, 0.4, 0.1, 1.0)
        self.add_ball(self.__main_ball)

    def on_size(self, *args):
        self.background.size = Window.size
        self.main_camera.update()

    def add_ball(self, new_ball):
        widget = new_ball.get_widget()
        with self.canvas:
            Color(widget.color[0], widget.color[1], widget.color[2], widget.color[3])

        self.add_widget(widget)
        self.__balls.append(new_ball)
        self.__physics_engine.add_body(new_ball.body)

    def update(self, dt):
        self.__physics_engine.update(dt)
        for ball in self.__balls:
            ball.update()

    # made as in kivy.Clock documentation
    def spawn_balls_over_time(self, amount, *largs):
        hb = hostile_balls.HostileBalls(amount)
        for ball in hb.hostile_balls:
            self.add_ball(ball)

    def on_touch_down(self, touch):
        self.__last_touch = touch.spos

    def on_touch_move(self, touch):
        camera = self.main_camera
        ball = self.__main_ball.body

        # calculating change of touch position between frames
        delta_x = (touch.spos[0] - self.__last_touch[0]) * camera.size
        delta_y = (touch.spos[1] - self.__last_touch[1]) * camera.size
        delta_y = delta_y * camera.hw_ratio
        new_pos = ball.pos + Vec2D(delta_x, delta_y)

        # limiting ball's position with camera's borders
        if new_pos.x + ball.rad > camera.pos.x + 0.5 * camera.size:
            new_pos.x = camera.pos.x + 0.5 * camera.size - ball.rad
        elif new_pos.x - ball.rad < camera.pos.x - 0.5 * camera.size:
            new_pos.x = camera.pos.x - 0.5 * camera.size + ball.rad

        if new_pos.y + ball.rad > camera.pos.y + 0.5 * camera.size * camera.hw_ratio:
            new_pos.y = camera.pos.y + 0.5 * camera.size * camera.hw_ratio - ball.rad
        elif new_pos.y - ball.rad < camera.pos.y - 0.5 * camera.size * camera.hw_ratio:
            new_pos.y = camera.pos.y - 0.5 * camera.size * camera.hw_ratio + ball.rad

        ball.pos = new_pos

        self.__last_touch = touch.spos
