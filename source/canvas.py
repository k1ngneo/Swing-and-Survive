from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty

canvaskv = '''
<GameScreen>:
	
	FloatLayout:
		canvas:
			Color:
				rgb: 0.1, 0.6, 0.6
			Rectangle:
				pos: 0, 0
				size: root.width, root.height
			
			Color:
				rgb: 1, 0.5, 0.3
			Ellipse:
				pos: root.main_ball.position.x - 0.5 * root.main_ball.radius, root.main_ball.position.y - 0.5 * root.main_ball.radius
				size: root.main_ball.radius, root.main_ball.radius


GameScreen
'''

class Vec2:
	def __init__(self, pos_x = 0.0, pos_y = 0.0):
		self.x = pos_x
		self.y = pos_y


class Ball:
	def __init__(self, pos = Vec2(0.0, 0.0), radius = 1.0):
		self.position = pos
		self.radius = radius


class GameScreen(Widget):
	def __init__(self, **kwargs):
		super(GameScreen, self).__init__(**kwargs)
		
		self.main_ball = ObjectProperty(Ball())
		self.main_ball = Ball(pos = Vec2(100.0, 100.0), radius = 10.0)
	
	
	def on_touch_down(self, touch):
		pass
		
	
	def on_touch_move(self, touch):
		pass
	
	
	def on_touch_up(self, touch):
		pass
	
	
	def build(self):
		return Builder.load_string(canvaskv)
