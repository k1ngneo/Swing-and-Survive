__version__ = "0.2"

from kivy.app import App
from kivy.config import Config, ConfigParser
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import FadeTransition, Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.settings import SettingsWithNoMenu
from kivy.uix.widget import Widget

from game_screen import GameScreen
from scene import Scene
from user_interface import *

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '550')
Config.write()


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.conf = ConfigParser()
        self.conf.read('settings.ini')

        with self.canvas:
            Color(0, 0, 0, 1)
            self.background = Rectangle(pos=(0, 0))

        # Create a BoxLayout for the settings screen
        settings_layout = FloatLayout()

        # Create a SettingsWithNoMenu object and add it to the layout
        settings = SettingsWithNoMenu()
        settings_layout.add_widget(settings)

        # Add the sound and music configuration option
        settings.add_json_panel('Settings', self.conf, data='''
                [
                    {
                        "type": "bool",
                        "title": "Music",
                        "desc": "Turn music on or off",
                        "section": "music",
                        "key": "enable_music"
                    },
                    {
                        "type": "bool",
                        "title": "Sound",
                        "desc": "Turn sound on or off",
                        "section": "sound",
                        "key": "enable_sound"
                    }
                ]
                ''')

        # Add a back button
        back_button = HoverButton(text='Save', pos_hint={'x': 0.3, 'y': 0.05})
        back_button.bind(on_press=self.go_back)
        settings_layout.add_widget(back_button)

        # Add the layout to the screen
        self.add_widget(settings_layout)

    def on_size(self, *args):
        self.background.size = Window.size

    def go_back(self, instance):
        self.manager.current = 'menu'

class SummaryScreen(Screen):
    def __init__(self, **kwargs):
        super(SummaryScreen, self).__init__(**kwargs)

        restart_button = Button(text='Play Again', pos_hint={'x': 0.5, 'y': 0.2})
        restart_button.color = (0.1, 0.1, 0.1, 1)
        restart_button.background_color = (0, 0, 0, 0)
        restart_button.size_hint_y = 0.1
        restart_button.bind(on_press=self.restart)
        self.ids.grid.add_widget(restart_button)

        main_menu_button = Button(text='Main Menu')
        main_menu_button.color = (0.1, 0.1, 0.1, 1)
        main_menu_button.background_color = (0, 0, 0, 0)
        main_menu_button.size_hint_y = 0.1
        main_menu_button.bind(on_press=self.go_to_main_menu)
        self.ids.grid.add_widget(main_menu_button)

    def restart(self, instance):
        self.manager.get_screen('game').scene.data.score = 0.0
        self.manager.get_screen('game').scene.add_player()
        self.manager.current = 'game'

    def go_to_main_menu(self, instance):
        self.manager.get_screen('game').scene.data.score = 0.0
        self.manager.get_screen('game').scene.add_player()
        self.manager.current = 'menu'

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

