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
        
        self.__ball_widgets = []
        
        with self.canvas:
            Color(0.1, 0.3, 0.3, 1)
            self.background = Rectangle(pos=(0, 0))
        
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        
        self.camera = Camera(Vec2D(0.0, 0.0), 10.0)
        
        # ball creation
        # --------------------
        
        # setting ball's world position and radius
        ball_pos = Vec2D(-2.5, 0.0)
        ball_rad = 1.0
        
        # creating widget for rendering
        self.main_ball = BallWidget()
        # converting world-space position to clip-space position
        self.main_ball.pos = self.camera.world_to_clip(ball_pos).t()
        # scaling radius from world-space to clip-space
        self.main_ball.radius = ball_rad / self.camera.size
        self.main_ball.color = (0.1, 0.1, 0.1, 1.0)
        
        self.add_ball(self.main_ball)
    
    
    def on_size(self, *args):
        self.background.size = Window.size
        self.camera.update()
    
    
    def add_ball(self, new_ball):
        with self.canvas:
            Color(new_ball.color[0], new_ball.color[1], \
				new_ball.color[2], new_ball.color[3])
        
        self.add_widget(new_ball)
        new_ball.update()
        self.__ball_widgets.append(new_ball)
    
    
    def update(self, dt):
        for ball in self.__ball_widgets:
            ball.update()
