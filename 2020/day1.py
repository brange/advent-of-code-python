from utils import api


def part1(arr_):
    for a in arr_:
        for b in arr_:
            if a + b == 2020:
                return a*b


def part2(arr_):
    for a in arr_:
        for b in arr_:
            if a + b > 2020:
                continue
            for c in arr_:
                if a + b + c == 2020:
                    return a * b * c


def solve():
    data = api.fetch(2020, 1)
    arr = list(map(int, data.split("\n")))
    print("Part one {}".format(part1(arr)))
    print("Part two {}".format(part2(arr)))


api.time_it(solve)
