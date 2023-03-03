__version__ = "0.1"

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import FadeTransition, Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget
from kivy.config import Config
from game_screen import GameScreen
from scene import Scene
from user_interface import *

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '550')
Config.write()


class SettingsScreen(Screen):
    pass

class SummaryScreen(Screen):
    pass

class Background(Widget):
    pass

class MenuScreen(Screen):
    __ball_spawn_dt = 0.0
    scene_widget = ObjectProperty(Widget())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scene = Scene(self.scene_widget)
        Clock.schedule_interval(self.update, 1.0 / 120.0)

    def on_size(self, *args):
        self.scene.data.main_camera.update()

    def update(self, dt):
        if self.manager.current == 'menu':
            self.scene.update(dt)


class BallCrushApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(SummaryScreen(name='summary'))
        return sm


if __name__ == '__main__':
    BallCrushApp().run()
