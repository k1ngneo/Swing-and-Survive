from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.button import Button
from kivymd.uix.behaviors import HoverBehavior


class HoverButton(Button, HoverBehavior):
    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)
        self.size_hint = (.4, .09)
        self.font_size = "18sp"
        self.background_color = (1, 1, 1, 1)
        self.color = (1, 1, 1, 1)

    def on_enter(self, *args):
        self.background_color = (0.7, 0.7, 0.7, 1)

    def on_leave(self, *args):
        self.background_color = (1, 1, 1, 1)


class TapButton(Button):
    scale = NumericProperty(1)

    def __init__(self, **kwargs):
        super(TapButton, self).__init__(**kwargs)
        Clock.schedule_once(self.start_pulsing, .25)
        self.initial_scale = self.scale

    def start_pulsing(self, *args):
        anim = Animation(scale=self.initial_scale * 1.4, duration=.999) + Animation(scale=self.initial_scale,
                                                                                    duration=.999)
        anim.start(self)
        anim.repeat = True


class SettingsButton(Button, HoverBehavior):
    angle = NumericProperty(1)

    def on_enter(self):
        Animation(angle=45, duration=0.3).start(self)

    def on_leave(self):
        Animation(angle=0, duration=0.3).start(self)

    def on_press(self):
        Animation(angle=0, duration=0.3).start(self)
