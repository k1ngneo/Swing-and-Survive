import os

from kivy.graphics import *

from source.ball import Ball
from source.hostile_balls_spawner import HostileBallsSpawner
from source.physics_engine import PhysicsEngine
from source.player import Player
from source.vector import Vec2D


class Scene:
    def __init__(self, parent):
        from source.scene_data import SceneData

        self.data = SceneData()
        self.engine = PhysicsEngine(self)
        self.parent_widget = parent
        self.__ball_spawn_dt = 0.0
        self.__last_touch = 0
        self.__dt = 0.0

    def add_player(self):
        self.data.player = Player()
        self.add_ball(self.data.player.control_ball)
        self.add_ball(self.data.player.swinging_ball)
        self.parent_widget.add_widget(self.data.player.line_widget)
        self.engine.player = self.data.player
        self.engine.control_ball = self.data.player.control_ball.body
        self.engine.swing_ball = self.data.player.swinging_ball.body
        self.engine.swing_range = self.data.player.swing_range

    def add_ball(self, new_ball: Ball):
        widget = new_ball.get_widget()
        with self.parent_widget.canvas:
            Color(widget.color[0], widget.color[1], widget.color[2], widget.color[3])
        self.parent_widget.add_widget(widget)
        self.data.balls.append(new_ball)
        self.engine.add_body(new_ball.body)

    def remove_ball(self, ball):
        widget = ball.get_widget()
        self.parent_widget.remove_widget(widget)
        self.data.balls.remove(ball)
        self.engine.remove_body(ball.body)

    def spawn_balls(self):
        hb = HostileBallsSpawner(self, self.data.amount_of_balls, self.data.balls_speed)
        for ball in hb.hostile_balls:
            self.add_ball(ball)

    def despawn_balls_check(self):
        for ball in self.data.balls:
            distance = ball.body.pos.dist(self.data.main_camera.pos)
            if distance > HostileBallsSpawner.spawn_radius + ball.body.rad:
                if self.data.player and ball is self.data.player.swinging_ball:
                    continue

                self.remove_ball(ball)

    def update(self, dt):
        self.__dt = dt
        if dt > 0.2:
            dt = 0.2

        self.data.score += dt

        self.despawn_balls_check()
        self.engine.update(dt)

        if self.data.player:
            self.data.player.update()

        self.__ball_spawn_dt += dt
        if self.__ball_spawn_dt >= self.data.ball_spawn_interval:
            self.__ball_spawn_dt -= self.data.ball_spawn_interval
            self.spawn_balls()

        for ball in self.data.balls:
            ball.update()

    def on_player_hit(self):
        store_score(self.data.score)
        summary_screen = self.parent_widget.manager.get_screen('summary')
        self.clear_scene()
        self.parent_widget.manager.current = 'summary'
        summary_screen.ids.sc.text = f'Score: {int(self.data.score)}'

    def on_touch_down(self, touch):
        self.__last_touch = touch.spos

    def on_touch_up(self, touch):
        if self.data.player:
            self.data.player.control_ball.body.vel = Vec2D(0.0, 0.0)

    def on_touch_move(self, touch):
        if self.data.player:
            camera = self.data.main_camera
            ball = self.data.player.control_ball.body

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
            self.data.player.move(delta_pos, self.__dt)
            self.__last_touch = touch.spos

    def clear_scene(self):
        for ball in self.data.balls:
            self.parent_widget.remove_widget(ball.get_widget())
        if self.data.player:
            self.parent_widget.remove_widget(self.data.player.line_widget)
        self.data.clear()
        self.engine.clear()


def store_score(score):
    filename = "score.txt"
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            file.write(str(score))
    else:
        with open(filename, "r") as file:
            existing_score = float(file.read())
        if score > existing_score:
            with open(filename, "w") as file:
                file.write(str(score))
