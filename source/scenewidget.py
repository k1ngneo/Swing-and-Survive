from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.properties import Clock

from camera import Camera
from vector import Vec2D
from ball import Ball
from physics_engine import PhysicsEngine

import math

class SceneWidget(Widget):
    
    main_camera = Camera(pos=Vec2D(0.0, 0.0), size=7.0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__physics_engine = PhysicsEngine()
        self.__balls = []
        self.__time_passed = 0.0
        
        with self.canvas:
            Color(0.1, 0.3, 0.3, 1)
            self.background = Rectangle(pos=(0, 0))
        
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        
        new_ball = Ball(Vec2D(1.0, 1.0), 0.5)
        new_ball.set_color(0.1, 0.6, 0.1, 1.0)
        new_ball.body.vel = Vec2D(0.01, 0.0)
        self.add_ball(new_ball)
        new_ball = Ball(Vec2D(-1.0, 1.0), 0.5)
        new_ball.set_color(0.1, 0.6, 0.1, 1.0)
        new_ball.body.vel = Vec2D(-0.01, 0.0)
        self.add_ball(new_ball)
        
        new_ball = Ball(Vec2D(0.0, 0.0), 1.0)
        new_ball.set_color(0.1, 0.7, 0.1, 1.0)
        new_ball.body.vel = Vec2D(0.0, 0.01)
        self.add_ball(new_ball)
        
        new_ball = Ball(Vec2D(-0.3, 0.2), 0.1)
        new_ball.set_color(0.1, 0.1, 0.1, 1.0)
        new_ball.body.vel = Vec2D(-0.01, 0.0)
        self.add_ball(new_ball)
        new_ball = Ball(Vec2D(0.3, 0.2), 0.1)
        new_ball.set_color(0.1, 0.1, 0.1, 1.0)
        new_ball.body.vel = Vec2D(0.01, 0.0)
        self.add_ball(new_ball)
        
        self.mouth = Ball(Vec2D(0.0, -0.4), 0.2)
        self.mouth.set_color(0.5, 0.1, 0.1, 1.0)
        self.add_ball(self.mouth)
    
    
    def on_size(self, *args):
        self.background.size = Window.size
        self.main_camera.update()
    
    
    def add_ball(self, new_ball):
        widget = new_ball.get_widget()
        with self.canvas:
            Color(widget.color[0], widget.color[1], widget.color[2], \
                widget.color[3])
        
        self.add_widget(widget)
        self.__balls.append(new_ball)
        self.__physics_engine.add_body(new_ball.body)
    
    
    def update(self, dt):
        self.__time_passed += dt
        self.mouth.body.pos = Vec2D(0.25 * math.sin(self.__time_passed), self.mouth.body.pos.y)

        self.__physics_engine.advance_bodies(dt)

        for ball in self.__balls:
            ball.update()
