from utils import api

YEAR, DAY = 2020, 11


class Seat:
    diffs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.occupied = False
        self.occupied_next = None
        self.adjacent = []

    def key(self):
        return seat_key(self.x, self.y)


def seat_key(x, y):
    return "{}, {}".format(x, y)


def parse_input(data):
    m = {}
    y = 0
    for row in data:
        x = 0
        for s in row:
            if s == 'L':
                seat = Seat(x, y)
                m[seat.key()] = seat
            x += 1
        y += 1
    return m


def run(seats, number_of_adjacent):
    while True:
        changed = False
        for _, seat in seats.items():
            n = count_occupied(seat.adjacent)
            if seat.occupied and n >= number_of_adjacent:
                seat.occupied_next = False
                changed = True
            elif not seat.occupied and n == 0:
                seat.occupied_next = True
                changed = True
        if not changed:
            return
        for _, seat in seats.items():
            if seat.occupied_next is not None:
                seat.occupied = seat.occupied_next
            seat.occupied_next = None


def count_occupied(seats):
    n = 0
    for seat in seats:
        if seat.occupied:
            n += 1
    return n


def part1(data):
    seats = parse_input(data)

    for _, seat in seats.items():
        for diff in seat.diffs:
            x = seat.x + diff[0]
            y = seat.y + diff[1]
            key = seat_key(x, y)
            if key in seats:
                seat.adjacent.append(seats[key])

    run(seats, 4)

    return count_occupied(list(seats.values()))


def part2(data):
    seats = parse_input(data)
    y_max = len(data)
    x_max = len(data[0])
    for _, seat in seats.items():
        for diff in seat.diffs:
            x = seat.x + diff[0]
            y = seat.y + diff[1]
            while 0 <= x < x_max and 0 <= y < y_max:
                key = seat_key(x, y)
                if key in seats:
                    seat.adjacent.append(seats[key])
                    break
                x += diff[0]
                y += diff[1]

    run(seats, 5)

    return count_occupied(list(seats.values()))


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))

    assert p1 == 2289
    assert p2 == 2059


solve()
