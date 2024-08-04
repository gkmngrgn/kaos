import random
from typing import Callable
import numpy as np
import numpy.typing as npt

from kaos_py.geometry import Point2D, RegularPolygon


class KaosGame:
    max_iterations = 100_000
    ignore_first_iterations = 10

    def __init__(self, polygon: RegularPolygon) -> None:
        self.polygon = polygon
        self.last_point = Point2D.from_array(polygon.points[0])
        self.last_vertex = 0

    def get_next_point(
        self,
        func: Callable[[int, int, int], bool],
        ratio: float,
        dist: int,
    ) -> Point2D:
        running = True
        remove_iter = 0

        while running is True:
            random_vertex = random.randint(0, self.polygon.points.shape[0] - 1)

            if func(random_vertex, self.last_vertex, dist) is True:
                random_point = Point2D.from_array(self.polygon.points[random_vertex])
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


def is_valid_point(random_vertex: int, last_vertex: int, dist: int) -> bool:
    return abs(random_vertex - last_vertex) != dist


def is_valid_point_1(random_vertex: int, last_vertex: int, dist: int) -> bool:
    return True


def generate_points(length: int, selection: int = 0) -> npt.NDArray[np.float64]:
    points = np.empty((length, 2), dtype=np.float64)

    if selection == 1:
        func = is_valid_point
        nr_edges = 4
        ratio = 0.5
        distance = 0

    elif selection == 2:
        func = is_valid_point
        nr_edges = 4
        ratio = 0.5
        distance = 2

    elif selection == 3:
        func = is_valid_point
        nr_edges = 5
        ratio = 0.5
        distance = 0

    elif selection == 4:
        func = is_valid_point_1
        nr_edges = 7
        ratio = 0.4
        distance = 0

    elif selection == 5:
        func = is_valid_point
        nr_edges = 7
        ratio = 0.4
        distance = 3

    elif selection == 6:
        func = is_valid_point
        nr_edges = 6
        ratio = 0.4
        distance = 3

    elif selection == 7:
        func = is_valid_point
        nr_edges = 6
        ratio = 0.375
        distance = 0

    elif selection == 8:
        func = is_valid_point
        nr_edges = 6
        ratio = 0.5
        distance = 2

    elif selection == 9:
        func = is_valid_point
        nr_edges = 8
        ratio = 0.4
        distance = 0

    elif selection == 10:
        func = is_valid_point
        nr_edges = 10
        ratio = 0.375
        distance = 1

    elif selection == 11:
        func = is_valid_point
        nr_edges = 10
        ratio = 0.375
        distance = 2

    elif selection == 12:
        func = is_valid_point
        nr_edges = 10
        ratio = 0.375
        distance = 3

    elif selection == 13:
        func = is_valid_point
        nr_edges = 10
        ratio = 0.375
        distance = 4

    elif selection == 14:
        func = is_valid_point
        nr_edges = 10
        ratio = 0.375
        distance = 5

    else:
        func = is_valid_point_1
        nr_edges = 3
        ratio = 0.5
        distance = 0

    polygon = RegularPolygon(nr_edges=nr_edges)
    kaos = KaosGame(polygon)

    for index in range(points.shape[0]):
        points[index] = kaos.get_next_point(func, ratio, distance).to_array()

    return points
