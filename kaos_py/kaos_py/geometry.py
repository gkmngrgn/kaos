import dataclasses


@dataclasses.dataclass
class Point2D:
    x: float
    y: float


@dataclasses.dataclass
class Rectangle2D:
    x: float
    y: float
    width: float
    height: float
