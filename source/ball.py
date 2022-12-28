from vector import Vec2D
from ballwidget import BallWidget


class Ball:
    def __init__(self, position=Vec2D(0.0, 0.0), radius=0.01):
        self.pos = position
        self.radius = radius
        
        self.__widget = BallWidget()
        self.__widget.color = (1.0, 1.0, 1.0, 1.0)
        self.update()
    
    
    def update(self):
        from scenewidget import SceneWidget as sc
        
        self.__widget.pos = sc.main_camera.world_to_clip(self.pos).t()
        self.__widget.radius = self.radius / sc.main_camera.size
        self.__widget.update()
    
    
    def set_color(self, r, g, b, a):
        self.__widget.color = (r, g, b, a)
    
    
    def get_widget(self) -> BallWidget:
        return self.__widget
