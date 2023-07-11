from source.camera import Camera
from source.vector import Vec2D


class SceneData:
    main_camera = Camera(pos=Vec2D(0.0, 0.0), size=20.0)
    score = 0

    def __init__(self):
        self.balls = []
        self.ball_spawn_interval = 3
        self.amount_of_balls = 5
        self.balls_speed = 10

        self.player = None

    def clear(self):
        self.balls.clear()
        self.player = None
