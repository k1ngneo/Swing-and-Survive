from kivy.core.window import Window
from kivy.graphics import *
from kivy.clock import Clock
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

        #self.add_widget(GameData.player.line_widget)
        self.add_ball(GameData.player.control_ball)
        self.add_ball(GameData.player.swinging_ball)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

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

    
    def update(self, dt):
        if dt > 1/120.0:
            dt = 1/120

        self.__physics_engine.update(dt)

        GameData.player.update()
        self.line.points = GameData.player.line_widget.line.points

        for ball in GameData.balls:
            ball.update()

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