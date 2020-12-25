from utils import api

YEAR, DAY = 2020, 24
DIRECTIONS = {'e': (2, 0), 'w': (-2, 0), 'se': (1, -1), 'sw': (-1, -1), 'ne': (1, 1), 'nw': (-1, 1)}


def part1(data):
    tiles = {}
    for row in data:
        # e, se, sw, w, nw, and ne
        index, x, y = 0, 0, 0
        while index < len(row):
            direction = row[index]
            index += 1
            if direction in 'ns':
                direction += row[index]
                index += 1
            x += DIRECTIONS[direction][0]
            y += DIRECTIONS[direction][1]
        key = (x, y)
        if key not in tiles:
            tiles[key] = 0
        if tiles[key]:
            tiles[key] = 0
        else:
            tiles[key] = 1
    return sum(tiles.values()), tiles


def calculate_color(tile, tiles):
    num_black = 0
    color = tiles.get(tile, 0)
    missing_tiles = set()
    for (x_diff, y_diff) in DIRECTIONS.values():
        key_ = (tile[0] + x_diff, tile[1] + y_diff)
        if key_ in tiles:
            num_black += tiles[key_]
        else:
            missing_tiles.add(key_)

    # Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
    # Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
    if color and (num_black == 0 or num_black > 2):
        return 0, missing_tiles
    elif not color and num_black == 2:
        return 1, missing_tiles
    return None, missing_tiles


def part2(tiles):
    for day in range(100):
        changed_tiles = {}
        missing_tiles = set()
        for tile, color in tiles.items():
            next_color, missing = calculate_color(tile, tiles)
            missing_tiles.update(missing)
            if next_color is not None:
                changed_tiles[tile] = next_color

        for tile in missing_tiles:
            color = calculate_color(tile, tiles)[0]
            if color is not None:
                changed_tiles[tile] = color

        for key, value in changed_tiles.items():
            tiles[key] = value

    return sum(tiles.values())


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))
    assert p1[0] == 332

    p2, p2_time = api.time_it(part2, p1[1])
    print("Part two {}, it took {} ms".format(p2, p2_time))
    assert p2 == 3900


solve()
