import numpy as np
import numpy.typing as npt
from PIL import Image

from kaos_py.geometry import Point2D, Rectangle2D, WorldToScreenSpace


def points_to_screen_space(
    world: Rectangle2D,
    screen_space: Rectangle2D,
    points: npt.NDArray[np.float64],
) -> npt.NDArray[np.float64]:
    "Transform, map, convert the points elements to the screen space."
    wssp = WorldToScreenSpace(world=world, screen_space=screen_space)
    return np.array([wssp.mapping(Point2D.from_array(p)).to_array() for p in points])


def draw_point_with_size(
    image: Image.Image, width: int, height: int, point: Point2D, radius: int
) -> None:
    "Draw a `crude` circle around the point."
    radius2 = radius**2
    xmin = max(int(point.x - radius), 0)
    xmax = min(int(point.x + radius), width - 1)
    ymin = max(int(point.y - radius), 0)
    ymax = min(int(point.y + radius), height - 1)

    for j in range(ymin, ymax + 1):
        for i in range(xmin, xmax + 1):
            dist = int((i - point.x) ** 2 + (j - point.y) ** 2)
            if dist <= radius2:
                image.putpixel(xy=(i, j), value=(255, 0, 0))


def backend_bmp(
    file_name: str,
    width: int,
    height: int,
    world: Rectangle2D,
    screen_space: Rectangle2D,
    points: npt.NDArray[np.float64],
    point_radius: int,
) -> None:
    image = Image.new("RGB", (width, height), color="white")
    points = points_to_screen_space(world, screen_space, points)

    if point_radius == 0:
        for point in points:
            pixel_position = Point2D.from_array(point).to_int_list()
            image.putpixel(xy=pixel_position, value=(255, 0, 0))
    else:
        for point in points:
            draw_point_with_size(image, width, height, point, point_radius)

    image.save(file_name)
