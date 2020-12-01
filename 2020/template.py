from utils import api

YEAR, DAY = 2020, 1


def part1(data):
    return 0


def part2(data):
    return 0


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))


solve()
