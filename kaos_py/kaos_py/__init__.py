from typing import Final

from kaos_py.backend_bmp import backend_bmp
from kaos_py.geometry import Rectangle2D
from kaos_py.kaos_game import KaosGame, generate_points


WIDTH: Final = 800
HEIGHT: Final = 800


def main() -> None:
    world = Rectangle2D(-1.08, -1.08, 1.08, 1.08)
    selection = 0
    points = generate_points(KaosGame.max_iterations, selection=selection)
    screen_space = Rectangle2D(left=0, bottom=0, right=WIDTH - 1, top=HEIGHT - 1)
    backend_bmp(f"kaos_{selection}.bmp", WIDTH, HEIGHT, world, screen_space, points, 0)
