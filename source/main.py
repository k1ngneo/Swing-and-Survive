__version__ = "0.1"

from kivy.app import App
from kivy.uix.label import Label

class BallsCrushers(App):
    def build(self):
        return Label(text='Hello world')

BallsCrushers().run()
