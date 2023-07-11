import os

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from source.scene import Scene

main_sound_path = os.path.join(os.getcwd(), 'assets', 'sounds')
menu_theme = os.path.join(main_sound_path, 'upbeat_funk.wav')


class GameScreen(Screen):
    __ball_spawn_dt = 0.0
    scene_widget = ObjectProperty(Widget())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scene = Scene(self)
        self.theme_sound = SoundLoader.load(menu_theme)

        self.scene.add_player()
        Clock.schedule_interval(self.update, 1.0 / 120.0)

    def on_size(self, *args):
        self.scene.data.main_camera.update()

    def update(self, dt):
        if self.manager.current == 'game':
            self.scene.update(dt)
            self.ids.score.text = f'Score: {int(self.scene.data.score)}'

    def on_touch_down(self, touch):
        self.scene.on_touch_down(touch)

    def on_touch_up(self, touch):
        self.scene.on_touch_up(touch)

    def on_touch_move(self, touch):
        self.scene.on_touch_move(touch)

    def on_enter(self):
        self.theme_sound.volume = 0.3
        self.theme_sound.loop = True
        self.theme_sound.play()

    def on_leave(self):
        self.theme_sound.stop()
