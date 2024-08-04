from typing import Self

import numpy as np
import numpy.typing as npt
from dataclasses import dataclass, field


@dataclass
class Point2D:
    x: np.float64
    y: np.float64

    @classmethod
    def from_array(cls, array: npt.NDArray[np.float64]) -> Self:
        return cls(x=array[0], y=array[1])

    def to_array(self) -> npt.NDArray[np.float64]:
        return np.array([self.x, self.y])

    def to_int_list(self) -> list[int]:
        return [self.x.astype(int), self.y.astype(int)]


@dataclass
class Rectangle2D:
    left: float
    bottom: float
    right: float
    top: float


@dataclass
class RegularPolygon:
    nr_edges: int = field(default=3)
    radius: float = field(default=1.0)
    start_angle: float = field(default=90.0)
    angle: float = field(init=False)
    points: npt.NDArray[np.float64] = field(init=False)

    def __post_init__(self) -> None:
        self.angle = 360.0 / self.nr_edges
        self.points = np.empty((self.nr_edges, 2), dtype=np.float64)

        # We change the start_angle in order to have the lower edge of every polygon parallel with
        # the horizontal axis.
        if self.nr_edges % 2 == 0:
            self.start_angle += self.angle / 2.0

        self.init_points()

    def init_points(self) -> None:
        deg_rad = np.pi / 180.0
        current_angle = self.start_angle * deg_rad
        min_y = 2.0

        for index in range(self.nr_edges):
            point = Point2D(
                x=self.radius * np.cos(current_angle),
                y=self.radius * np.sin(current_angle),
            )

            self.points[index] = [point.x, point.y]

            if min_y > point.y:
                min_y = point.y

            current_angle += self.angle * deg_rad


@dataclass(init=False)
class WorldToScreenSpace:
    A: float
    B: float
    C: float
    D: float

    def __init__(self, world: Rectangle2D, screen_space: Rectangle2D) -> None:
        self.A = (screen_space.right - screen_space.left) / (world.right - world.left)
        self.B = (screen_space.top - screen_space.bottom) / (world.top - world.bottom)
        self.C = screen_space.left - self.A * world.left
        self.D = screen_space.bottom - self.B * world.bottom

    def mapping(self, point: Point2D) -> Point2D:
        return Point2D(
            x=self.A * point.x + self.C,
            y=self.B * point.y + self.D,
        )
