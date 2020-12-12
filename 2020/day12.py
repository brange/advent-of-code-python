from utils import api
import numpy as np

YEAR, DAY = 2020, 12

DIRECTIONS = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}
N = DIRECTIONS['N']
E = DIRECTIONS['E']
S = DIRECTIONS['S']
W = DIRECTIONS['W']


def rotate_degrees(direction, degrees):
    theta = np.radians(degrees)
    cos, sin = np.cos(theta), np.sin(theta)
    rot = np.array(((cos, -sin), (sin, cos)))
    res = rot.dot(direction)
    return round(res[0]), round(res[1])


def rotate(direction, r_or_l, amount):
    degrees = amount if r_or_l == 'L' else -amount
    return rotate_degrees(direction, degrees)


class Position:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = E


def test_rotate():
    assert rotate(N, 'R', 90) == E
    assert rotate(E, 'R', 90) == S
    assert rotate(S, 'R', 90) == W
    assert rotate(W, 'R', 90) == N

    assert rotate(N, 'L', 90) == W
    assert rotate(W, 'L', 90) == S
    assert rotate(S, 'L', 90) == E
    assert rotate(E, 'L', 90) == N

    assert rotate(N, 'L', 180) == S
    assert rotate(N, 'R', 180) == S

    assert rotate(W, 'L', 180) == E
    assert rotate(W, 'R', 180) == E

    assert rotate(S, 'L', 180) == N
    assert rotate(S, 'R', 180) == N

    assert rotate(E, 'L', 180) == W
    assert rotate(E, 'R', 180) == W

    assert rotate(E, 'L', 270) == S
    assert rotate(W, 'L', 270) == N

    print("Tests done")


def part1(data):
    position = Position()

    for row in data:
        a = row[0:1]
        amount = int(row[1:])
        if a in DIRECTIONS.keys():
            position.x += DIRECTIONS[a][0]*amount
            position.y += DIRECTIONS[a][1]*amount
        elif a == 'L' or a == 'R':
            position.direction = rotate(position.direction, a, amount)
        elif a == 'F':
            position.x += position.direction[0] * amount
            position.y += position.direction[1] * amount

    return abs(position.x) + abs(position.y)


def part2(data):
    position = Position()
    waypoint = Position()
    waypoint.x = 10
    waypoint.y = 1

    for row in data:
        a = row[0:1]
        amount = int(row[1:])
        if a in DIRECTIONS.keys():
            waypoint.x += DIRECTIONS[a][0]*amount
            waypoint.y += DIRECTIONS[a][1]*amount
        elif a == 'L' or a == 'R':
            waypoint.x, waypoint.y = rotate((waypoint.x, waypoint.y), a, amount)
        elif a == 'F':
            position.x += waypoint.x * amount
            position.y += waypoint.y * amount

    return abs(position.x) + abs(position.y)


def solve():
    test_rotate()
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))
    assert p1 == 521

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))
    assert p2 == 22848


solve()
