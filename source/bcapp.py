from kivy.app import App
from kivy.core.window import Window

from canvas import GameScreen


class BallCrushApp(App):
    
    def __init__(self):
        App.__init__(self)
        App.title = 'Ball Crush'
        self.gameScr = GameScreen().build()

    def build(self):
        return self.gameScr
