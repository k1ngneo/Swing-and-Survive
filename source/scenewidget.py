from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.metrics import *
from kivy.properties import Clock

from camera import Camera
from vector import Vec2D
from ballwidget import BallWidget


class SceneWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.ballWidgets = []
        
        with self.canvas:
            Color(0.1, 0.3, 0.3, 1)
            self.background = Rectangle(pos=(0, 0))
        
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        
        self.camera = Camera()
        
        # ball creation
        # --------------------
        
        # setting ball's world position and radius
        ball_pos = Vec2D(-2.5, 0.0)
        ball_rad = 1.0
        
        # creating widget for rendering
        self.mainBall = BallWidget()
        # converting world-space position to clip-space position
        self.mainBall.pos = self.camera.worldToClip(ball_pos).t()
        # scaling radius from world-space to clip-space
        self.mainBall.radius = ball_rad / self.camera.size
        self.mainBall.color = (0.1, 0.1, 0.1, 1.0)
        
        self.add_ball(self.mainBall)
    
    
    def on_size(self, *args):
        self.background.size = Window.size
        self.camera.update()
    
    
    def add_ball(self, new_ball):
        ball_width = new_ball.radius
        ball_size = (ball_width, ball_width * (Window.size[0] / Window.size[1]))
        
        with self.canvas:
            Color(new_ball.color[0], new_ball.color[1], new_ball.color[2], \
				new_ball.color[3])
        
        self.add_widget(new_ball)
        new_ball.update()
        self.ballWidgets.append(new_ball)
    
    
    def update(self, dt):
        for ball in self.ballWidgets:
            ball.update()
