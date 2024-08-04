import sys
from typing import Final

from kaos_py.backend_bmp import backend_bmp
from kaos_py.geometry import Rectangle2D
from kaos_py.kaos_game import KaosGame, generate_points


WIDTH: Final = 800
HEIGHT: Final = 800


def cli() -> None:
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
