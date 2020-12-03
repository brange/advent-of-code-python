from utils import api

YEAR, DAY = 2020, 3


def part1(data):
    return traverse(data, 3, 1)


def traverse(data, delta_x, delta_y):
    x, y = 0, 0
    num_trees = 0
    max_y = len(data)
    max_x = len(data[0])

    while True:
        x = (x + delta_x) % max_x
        y += delta_y
        if y >= max_y:
            break
        if data[y][x] == '#':
            num_trees += 1

    return num_trees


def part2(data):
    product = traverse(data, 1, 1)
    product *= traverse(data, 3, 1)
    product *= traverse(data, 5, 1)
    product *= traverse(data, 7, 1)
    product *= traverse(data, 1, 2)
    return product


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))

    assert p1 == 189
    assert p2 == 1718180100


solve()
