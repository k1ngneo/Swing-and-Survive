import math


class Vec2D:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	
	def __add__(self, other):
		return Vec2D(self.x + other.x, self.y + other.y)
	
	
	def __sub__(self, other):
		return Vec2D(self.x - other.x, self.y - other.y)
	
	
	def __mul__(self, other):
		if isinstance(other, self.__class__):
			return Vec2D(self.x * other.x, self.y * other.y)
		elif isinstance(other, float) or isinstance(other, int):
			return Vec2D(other * self.x, other * self.y)
	
	__rmul__ = __mul__
	
	def __truediv__(self, other):
		return Vec2D(self.x / other.x, self.y / other.y)
	
	
	def length(self) -> float:
		return math.sqrt(self.x**2 + self.y**2)
	
	
	def t(self):
		return (self.x, self.y)
