__version__ = "0.1"

from kivy.app import App
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.screenmanager import ScreenManager

from gamescreen import GameScreen
from userinterface import *


class SettingsScreen(Screen):
    pass


class BallCrushApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(GameScreen(name='game'))
        return sm


if __name__ == '__main__':
    BallCrushApp().run()
