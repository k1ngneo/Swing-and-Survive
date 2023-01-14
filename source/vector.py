from math import sqrt
from math import pow


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
        return Vec2D(self.x / other.x, self.y / other.y)

    def length(self) -> float:
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    def dist(self, other):
        return sqrt(pow((self.x - other.x), 2) + pow((self.y - other.y), 2))

    def normalize(self):
        return self * (1/sqrt(pow(self.x, 2) + pow(self.y, 2)))

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y

    def t(self):
        return self.x, self.y
