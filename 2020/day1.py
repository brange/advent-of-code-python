from utils import api


YEAR, DAY = 2020, 1


def part1(arr_):
    for a in arr_:
        for b in arr_:
            if a + b == 2020:
                return a*b


def part2(arr_):
    for a in arr_:
        for b in arr_:
            ab = a + b
            if ab > 2020:
                continue
            for c in arr_:
                if ab + c == 2020:
                    return a * b * c


def solve():
    data = api.fetch(YEAR, DAY)
    arr = list(map(int, data.split("\n")))
    p1, p1_time = api.time_it(part1, arr)
    print("Part one {}, it took {} ms".format(p1, p1_time))
    p2, p2_time = api.time_it(part2, arr)
    print("Part two {}, it took {} ms".format(p2, p2_time))


api.time_it(solve)
