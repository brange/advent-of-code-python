from utils import api
import math

YEAR, DAY = 2020, 5


def calculate_boundaries(min_, max_, sign):
    if sign == 'F' or sign == 'L':
        return min_, min_ + math.floor((max_ - min_) / 2)
    else:
        return min_ + math.ceil((max_ - min_) / 2), max_


def test_calculate_boundaries(expected_min, expected_max, *args):
    min_, max_ = calculate_boundaries(*args)
    assert min_ == expected_min, "Was {}, but expected {}".format(min_, expected_min)
    assert max_ == expected_max, "Was {}, but expected {}".format(max_, expected_max)


def test():
    test_calculate_boundaries(0, 63, 0, 127, 'L')
    test_calculate_boundaries(0, 31, 0, 63, 'L')
    test_calculate_boundaries(32, 63, 0, 63, 'U')
    test_calculate_boundaries(0, 15, 0, 31, 'L')
    test_calculate_boundaries(16, 31, 0, 31, 'U')
    test_calculate_boundaries(24, 31, 16, 31, 'U')

    assert parse_boarding_id("BFFFBBFRRR") == 567
    assert parse_boarding_id("FFFBBBFRRR") == 119
    assert parse_boarding_id("BBFFBBFRLL") == 820


def calculate_seat_id(row, column):
    return row * 8 + column


def parse_boarding_id(boarding):
    min_, max_ = 0, 127
    for a in range(0,7):
        sign = boarding[a]
        assert sign == 'B' or sign == 'F', "sign was {}".format(sign)
        min_, max_ = calculate_boundaries(min_, max_, sign)
    assert min_ == max_
    row = min_

    min_, max_ = 0, 7
    for a in range(7, 10):
        sign = boarding[a]
        assert sign == 'R' or sign == 'L', "sign was {}".format(sign)
        min_, max_ = calculate_boundaries(min_, max_, sign)
    assert min_ == max_
    column = min_

    return calculate_seat_id(row, column)


def part1(data):
    return max(set(map(parse_boarding_id, data)))


def part2(data):
    seat_ids = set(map(parse_boarding_id, data))

    for row in range(0, 127):
        for column in range(0, 7):
            seat_id = calculate_seat_id(row, column)
            if seat_id not in seat_ids \
                    and (seat_id + 1) in seat_ids \
                    and (seat_id - 1) in seat_ids:
                return seat_id

    raise RuntimeError("No empty seat found")


def solve():
    test()
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))

    assert p1 == 822
    assert p2 == 705


solve()
