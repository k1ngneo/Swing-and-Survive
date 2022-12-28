from kivy.animation import Animation
from kivy.properties import ListProperty, ObjectProperty, Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivymd.uix.behaviors import HoverBehavior


class HoverButton(Button, HoverBehavior):
    background = ListProperty((220 / 255, 20 / 255, 60 / 255, 1))

    def on_enter(self):
        self.background = (180 / 255, 0 / 255, 23 / 255, 1)
        Animation(size_hint=(.45, .1), d=.1).start(self)

    def on_leave(self):
        self.background = (220 / 255, 20 / 255, 60 / 255, 1)
        Animation(size_hint=(.4, .09), d=.1).start(self)


class MenuScreen(Screen):
    bg_color = ObjectProperty([.4, .4, .4, 1])

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.start_pulsing, 2)

    def start_pulsing(self, *args):
        anim = Animation(bg_color=[.5, .5, .5, 1]) + Animation(bg_color=[.4, .4, .4, 1])
        anim.repeat = True
        anim.start(self)
