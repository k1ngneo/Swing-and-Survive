from kivy.core.window import Window
from vector import Vec2D

'''
    Clip Space
     (0,1)            (1,1)
       +----------------+
       |                |
       |   (0.5, 0.5)   |
       |       *        |
       |                |
       |                |
       +----------------+
     (0,0)            (1,0)
     
     
    World Space
                    cam.pos+0.5*size
       +----------------+
       |                |
       |   camera.pos   |
       |       *        |
       |                |
       |                |
       +----------------+
  cam.pos-0.5*size    
'''


class Camera:
    def __init__(self, pos=Vec2D(0.0, 0.0), size=10.0):
        self.pos = pos
        self.size = size
        self.hw_ratio = Window.size[1] / Window.size[0]

    def world_to_clip(self, vertex: Vec2D) -> Vec2D:
        cam_size = Vec2D(self.size, self.size * self.hw_ratio)
        vertex = vertex - (self.pos - 0.5 * cam_size)
        vertex = vertex / cam_size
        return vertex

    def update(self):
        self.hw_ratio = Window.size[1] / Window.size[0]
