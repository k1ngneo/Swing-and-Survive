from math import sqrt


class Vec2D:
    def __init__(self, x=0.0, y=0.0):
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
        if isinstance(other, self.__class__):
            return Vec2D(self.x / other.x, self.y / other.y)
        elif isinstance(other, float) or isinstance(other, int):
            return Vec2D(self.x / other, self.y / other)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def length(self) -> float:
        return sqrt(self.x**2 + self.y**2)

    def dist(self, other) -> float:
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def dist2(self, other) -> float:
        return (self.x - other.x)**2 + (self.y - other.y)**2

    def normalize(self):
        return self * (1/sqrt(self.x**2 + self.y**2))

    def t(self):
        return self.x, self.y
