from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import *
from kivy.uix.screenmanager import Screen

from camera import Camera
from vector import Vec2D
from ball import Ball
import physics_engine
import player

class GameData:
    main_camera = Camera(pos=Vec2D(0.0, 0.0), size=20.0)
    player = None
    balls = []

class GameScreen(Screen):
    __ball_spawn_dt = 0.0
    ball_spawn_interval = 2
    amount_of_balls = 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        GameData.player = player.Player()
        self.__physics_engine = physics_engine.PhysicsEngine()

        self.__last_touch = 0

        with self.canvas:
            Color(0.1, 0.3, 0.3, 1)
            self.background = Rectangle(pos=(0, 0))
            Color(0.1, 0.1, 0.1, 1.0)
            self.line = Line(points=[], width=1.5)

        self.add_ball(GameData.player.control_ball)
        self.add_ball(GameData.player.swinging_ball)

        Clock.schedule_interval(self.update, 1.0 / 120.0)

    def on_size(self, *args):
        self.background.size = Window.size
        GameData.main_camera.update()

    def add_ball(self, new_ball: Ball):
        widget = new_ball.get_widget()
        with self.canvas:
            Color(widget.color[0], widget.color[1], widget.color[2], widget.color[3])

        self.add_widget(widget)
        GameData.balls.append(new_ball)
        self.__physics_engine.add_body(new_ball.body)

    def remove_ball(self, ball):
        widget = ball.get_widget()
        self.remove_widget(widget)
        GameData.balls.remove(ball)
        self.__physics_engine.remove_body(ball.body)

    def despawn_balls(self):
        import hostile_balls
        for ball in GameData.balls:
            distance = ball.body.pos.dist(GameData.main_camera.pos)
            if distance > hostile_balls.HostileBalls.spawn_radius + ball.body.rad:
                self.remove_ball(ball)

    def update(self, dt):
        # if dt > 1/120:
        #     dt = 1/120

        GameData.player.update()

        self.despawn_balls()
        self.__physics_engine.update(dt)
        self.__ball_spawn_dt += dt
        if self.__ball_spawn_dt >= self.ball_spawn_interval:
            self.__ball_spawn_dt -= self.ball_spawn_interval
            self.spawn_balls(self.amount_of_balls)

        self.line.points = GameData.player.line_widget.line.points

        for ball in GameData.balls:
            ball.update()

    def spawn_balls(self, amount):
        import hostile_balls
        hb = hostile_balls.HostileBalls(amount)
        for ball in hb.hostile_balls:
            self.add_ball(ball)

    def on_touch_down(self, touch):
        self.__last_touch = touch.spos

    def on_touch_move(self, touch):
        camera = GameData.main_camera
        ball = GameData.player.control_ball.body

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

        delta_pos = new_pos - ball.pos
        GameData.player.move(delta_pos)

        self.__last_touch = touch.spos
