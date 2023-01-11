from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import *
from kivy.uix.screenmanager import Screen

from ball import Ball
from camera import Camera
from physics_engine import PhysicsEngine
from vector import Vec2D


class GameScreen(Screen):
    main_camera = Camera(pos=Vec2D(0.0, 0.0), size=7.0)
    __ball_spawn_dt = 0.0
    ball_spawn_interval = 2
    amount_of_balls = 3
    balls = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__physics_engine = PhysicsEngine()
        self.__last_touch = 0

        with self.canvas:
            Color(0.1, 0.3, 0.3, 1)
            self.background = Rectangle(pos=(0, 0))

        Clock.schedule_interval(self.update, 1.0 / 120.0)

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
        self.balls.append(new_ball)
        self.__physics_engine.add_body(new_ball.body)

    def remove_ball(self, ball):
        widget = ball.get_widget()
        self.remove_widget(widget)
        self.balls.remove(ball)
        self.__physics_engine.remove_body(ball.body)

    def despawn_balls(self):
        import hostile_balls
        for ball in self.balls:
            distance = ball.body.pos.dist(self.main_camera.pos)
            if distance > hostile_balls.HostileBalls.spawn_radius + ball.body.rad:
                self.remove_ball(ball)

    def update(self, dt):
        self.despawn_balls()
        self.__physics_engine.update(dt)
        self.__ball_spawn_dt += dt
        if self.__ball_spawn_dt >= self.ball_spawn_interval:
            self.__ball_spawn_dt -= self.ball_spawn_interval
            self.spawn_balls(self.amount_of_balls)
        for ball in self.balls:
            ball.update()

    def spawn_balls(self, amount):
        import hostile_balls
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
