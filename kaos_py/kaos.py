from dataclasses import dataclass, field
import random
import sys
from typing import Callable, Final, Annotated, TypeAlias

import numpy as np
import numpy.typing as npt
from PIL import Image


WIDTH: Final = 800
HEIGHT: Final = 800


point2d_dtype = np.dtype([("x", np.float64), ("y", np.float64)])
Point2D: TypeAlias = Annotated[np.float64, (2,)]


@dataclass
class Rectangle2D:
    left: np.float64
    bottom: np.float64
    right: np.float64
    top: np.float64


@dataclass
class RegularPolygon:
    nr_edges: int
    radius: float
    start_angle: float
    angle: float = field(init=False)
    points: npt.NDArray[Point2D] = field(
        init=False, default_factory=lambda: np.zeros((0, 2), dtype=point2d_dtype)
    )

    def __post_init__(self) -> None:
        self.angle = 360.0 / self.nr_edges

        # We change the start_angle in order to have the lower edge of every polygon parallel with
        # the horizontal axis.
        if self.nr_edges % 2 == 0:
            self.start_angle += self.angle / 2.0

        self.init_points()

    def init_points(self) -> None:
        deg_rad = np.pi / 180
        current_angle = self.start_angle * deg_rad
        min_y = 2.0

        for point_index in range(self.nr_edges):
            self.points[point_index] = np.array(
                [
                    self.radius * np.cos(current_angle),
                    self.radius * np.sin(current_angle),
                ],
                dtype=point2d_dtype,
            )

            if min_y > self.points[point_index].y:
                min_y = self.points[point_index].y

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
        return np.array(
            [
                self.A * point.x + self.C,
                self.B * point.y + self.D,
            ],
            dtype=point2d_dtype,
        )


class KaosGame:
    max_iterations = 100_000
    ignore_first_iterations = 10

    def __init__(self, polygon: RegularPolygon) -> None:
        self.polygon = polygon
        self.last_point = polygon.points[0]
        self.last_vertex = 0

    def get_next_point(
        self,
        is_valid_fn: Callable[[int, int, int], bool],
        ratio: float,
        dist: int,
    ) -> Point2D:
        running = True
        remove_iter = 0

        while running is True:
            random_vertex = random.randint(0, len(self.polygon.points) - 1)
            if is_valid_fn(random_vertex, self.last_vertex, dist) is True:
                random_point = self.polygon.points[random_vertex]
                point = Point2D(
                    x=((self.last_point.x + random_point.x) * ratio),
                    y=((self.last_point.y + random_point.y) * ratio),
                )
                self.last_vertex = random_vertex
                self.last_point = point
                remove_iter += 1

                if remove_iter >= self.ignore_first_iterations:
                    running = False

        return point


def is_point_valid(random_vertex: int, last_vertex: int, dist: int) -> bool:
    return abs(random_vertex - last_vertex) != dist


def is_point_valid_1(random_vertex: int, last_vertex: int, dist: int) -> bool:
    return True


def generate_points(max_iterations: int, selection: int = 0) -> npt.NDArray[Point2D]:
    if selection == 1:
        is_valid_fn = is_point_valid
        nr_edges = 4
        ratio = 0.5
        distance = 0

    elif selection == 2:
        is_valid_fn = is_point_valid
        nr_edges = 4
        ratio = 0.5
        distance = 2

    elif selection == 3:
        is_valid_fn = is_point_valid
        nr_edges = 5
        ratio = 0.5
        distance = 0

    elif selection == 4:
        is_valid_fn = is_point_valid_1
        nr_edges = 7
        ratio = 0.4
        distance = 0

    elif selection == 5:
        is_valid_fn = is_point_valid
        nr_edges = 7
        ratio = 0.4
        distance = 3

    elif selection == 6:
        is_valid_fn = is_point_valid
        nr_edges = 6
        ratio = 0.4
        distance = 3

    elif selection == 7:
        is_valid_fn = is_point_valid
        nr_edges = 6
        ratio = 0.375
        distance = 0

    elif selection == 8:
        is_valid_fn = is_point_valid
        nr_edges = 6
        ratio = 0.5
        distance = 2

    elif selection == 9:
        is_valid_fn = is_point_valid
        nr_edges = 8
        ratio = 0.4
        distance = 0

    elif selection == 10:
        is_valid_fn = is_point_valid
        nr_edges = 10
        ratio = 0.375
        distance = 1

    elif selection == 11:
        is_valid_fn = is_point_valid
        nr_edges = 10
        ratio = 0.375
        distance = 2

    elif selection == 12:
        is_valid_fn = is_point_valid
        nr_edges = 10
        ratio = 0.375
        distance = 3

    elif selection == 13:
        is_valid_fn = is_point_valid
        nr_edges = 10
        ratio = 0.375
        distance = 4

    elif selection == 14:
        is_valid_fn = is_point_valid
        nr_edges = 10
        ratio = 0.375
        distance = 5

    else:
        is_valid_fn = is_point_valid_1
        nr_edges = 3
        ratio = 0.5
        distance = 0

    polygon = RegularPolygon(nr_edges=nr_edges, radius=1.0, start_angle=90.0)
    kaos = KaosGame(polygon)
    points = np.empty((max_iterations, 2), dtype=point2d_dtype)

    for point_index in range(max_iterations):
        points[point_index] = kaos.get_next_point(is_valid_fn, ratio, distance)

    return points


def points_to_screen_space(
    world: Rectangle2D,
    screen_space: Rectangle2D,
    points: npt.NDArray[Point2D],
) -> None:
    "Transform, map, convert the points elements to the screen space."
    w2ss = WorldToScreenSpace(world=world, screen_space=screen_space)
    for index, point in enumerate(points):
        points[index] = w2ss.mapping(point)


def backend_bmp(
    file_name: str,
    width: int,
    height: int,
    world: Rectangle2D,
    screen_space: Rectangle2D,
    points: npt.NDArray[Point2D],
    point_radius: int,
) -> None:
    points_to_screen_space(world, screen_space, points)
    image = Image.new("RGB", (width, height), color="white")
    radius2 = point_radius**2
    point_color = (255, 0, 0)

    if point_radius == 0:
        for point in points:
            image.putpixel(xy=(int(point.x), int(point.y)), value=point_color)
    else:
        for point in points:
            xmin = max(int(point.x - point_radius), 0)
            xmax = min(int(point.x + point_radius), width - 1)
            ymin = max(int(point.y - point_radius), 0)
            ymax = min(int(point.y + point_radius), height - 1)

            for j in range(ymin, ymax + 1):
                for i in range(xmin, xmax + 1):
                    dist = int((i - point.x) ** 2 + (j - point.y) ** 2)
                    if dist <= radius2:
                        image.putpixel(xy=(i, j), value=point_color)

    image.save(file_name)


def main() -> None:
    # profiler = cProfile.Profile()
    # profiler.enable()

    world = Rectangle2D(-1.08, -1.08, 1.08, 1.08)

    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        selection = int(sys.argv[1])
    else:
        selection = 0

    print(f"Selection is: {selection}")
    points = generate_points(KaosGame.max_iterations, selection=selection)
    screen_space = Rectangle2D(left=0, bottom=0, right=WIDTH - 1, top=HEIGHT - 1)
    file_name = f"kaos_{selection}.bmp"
    backend_bmp(file_name, WIDTH, HEIGHT, world, screen_space, points, 0)
    print(f"Saved to: {file_name}")

    # profiler.disable()
    # stats = pstats.Stats(profiler)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
