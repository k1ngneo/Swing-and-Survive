from vector import Vec2D
from ballwidget import BallWidget

import math

class Ball:
    
    class Body:
        def __init__(self, position=Vec2D(0.0, 0.0), radius=1.0):
            self.pos = position
            self.rad = radius
            self.vel = Vec2D(0.0, 0.0)
            self.mass = (4.0 / 3.0) * math.pi * (self.rad**3)
        
    
    def __init__(self, position=Vec2D(0.0, 0.0), radius=1.0):
        self.body = Ball.Body(position, radius)
        
        self.__widget = BallWidget()
        self.__widget.color = (1.0, 1.0, 1.0, 1.0)
        self.update()
    
    
    def update(self):
        from scenewidget import SceneWidget as sc
        
        self.__widget.pos = sc.main_camera.world_to_clip(self.body.pos).t()
        self.__widget.radius = self.body.rad / sc.main_camera.size
        self.__widget.update()
    
    
    def set_color(self, r, g, b, a):
        self.__widget.color = (r, g, b, a)
    
    
    def get_widget(self) -> BallWidget:
        return self.__widget
