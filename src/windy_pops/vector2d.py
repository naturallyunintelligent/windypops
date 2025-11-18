import math
from dataclasses import dataclass


@dataclass
class Vector2D:
    x: float
    y: float

    def dot(self, other: "Vector2D") -> float:
        return self.x * other.x + self.y * other.y

    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalised(self) -> "Vector2D":
        magnitude = self.magnitude()
        return Vector2D(self.x / magnitude, self.y / magnitude)

    @classmethod
    def from_bearing_and_magnitude(cls, bearing: float, magnitude: float) -> "Vector2D":
        return Vector2D(
            magnitude * math.sin((bearing / 360) * 2 * math.pi),
            magnitude * math.cos((bearing / 360) * 2 * math.pi),
        )
