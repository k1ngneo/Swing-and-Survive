from kivy.animation import Animation
from kivy.properties import ListProperty, Clock
from kivy.uix.button import Button
from kivymd.uix.behaviors import HoverBehavior


class HoverButton(Button, HoverBehavior):
    background = ListProperty((220 / 255, 20 / 255, 60 / 255, 1))

    def on_enter(self):
        self.background = (180 / 255, 0 / 255, 23 / 255, 1)
        Animation(size_hint=(.45, .1), d=.1).start(self)

    def on_leave(self):
        self.background = (220 / 255, 20 / 255, 60 / 255, 1)
        Animation(size_hint=(.4, .09), d=.1).start(self)


class TapButton(Button):

    def __init__(self, **kwargs):
        super(TapButton, self).__init__(**kwargs)
        Clock.schedule_once(self.start_pulsing, .5)

    def start_pulsing(self, *args):
        anim = Animation(font_size=16.0, d=.999) + Animation(font_size=25.0, d=.999)
        anim.repeat = True
        anim.start(self)
