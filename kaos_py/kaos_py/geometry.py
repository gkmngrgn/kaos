from dataclasses import dataclass, field


@dataclass
class Point2D:
    x: float
    y: float


@dataclass
class Rectangle2D:
    left: float
    bottom: float
    right: float
    top: float


@dataclass
class RegularPython:
    nr_edges: int = field(default=3)
    radius: float = field(default=1.0)
    start_angle: float = field(default=90.0)
    angle: float = field(default=120.0)
    points: list[Point2D] = field(default_factory=list)
