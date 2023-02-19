from kivy.animation import Animation
from kivy.properties import ListProperty, NumericProperty
from kivy.clock import Clock
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
    scale = NumericProperty(1)

    def __init__(self, **kwargs):
        super(TapButton, self).__init__(**kwargs)
        Clock.schedule_once(self.start_pulsing, .25)
        self.initial_scale = self.scale

    def start_pulsing(self, *args):
        anim = Animation(scale=self.initial_scale * 1.4, duration=.999) + Animation(scale=self.initial_scale, duration=.999)
        anim.start(self)
        anim.repeat = True
        anim.start(self)
