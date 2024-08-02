async def generate_points(points: list[Point2D], selection: int = 0) -> int:
    if selection == 1:
        nr_edges = 4
        ratio = 0.5
        distance = 0

    elif selection == 2:
        nr_edges = 4
        ratio = 0.5
        distance = 2

    elif selection == 3:
        nr_edges = 5
        ratio = 0.5
        distance = 0

    elif selection == 4:
        nr_edges = 7
        ratio = 0.4
        distance = 0

    elif selection == 5:
        nr_edges = 7
        ratio = 0.4
        distance = 3

    elif selection == 6:
        nr_edges = 6
        ratio = 0.4
        distance = 3

    elif selection == 7:
        nr_edges = 6
        ratio = 0.375
        distance = 0

    elif selection == 8:
        nr_edges = 6
        ratio = 0.5
        distance = 2

    elif selection == 9:
        nr_edges = 8
        ratio = 0.4
        distance = 0

    elif selection == 10:
        nr_edges = 10
        ratio = 0.375
        distance = 1

    elif selection == 11:
        nr_edges = 10
        ratio = 0.375
        distance = 2

    elif selection == 12:
        nr_edges = 10
        ratio = 0.375
        distance = 3

    elif selection == 13:
        nr_edges = 10
        ratio = 0.375
        distance = 4

    elif selection == 14:
        nr_edges = 10
        ratio = 0.375
        distance = 5

    else:
        nr_edges = 3
        ratio = 0.5
        distance = 0
