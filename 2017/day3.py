from utils import api
import math


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def rotate_left(dir):
    if dir.x == 1 and dir.y == 0:
        return Coord(0, 1)
    if dir.x == 0 and dir.y == 1:
        return Coord(-1, 0)
    if dir.x == -1 and dir.y == 0:
        return Coord(0, -1)
    if dir.x == 0 and dir.y == -1:
        return Coord(1, 0)


data = api.fetch(2017, 3)

steps = 0
max_steps = 1
direction = Coord(1, 0)
current = Coord(0, 0)
rotations = 0

part1_answer = None

part2 = {"0,0": 1}
part2_answer = None


def get_nearby(coord):
    n = []
    for x in range(-1,2):
        for y in range(-1,2):
            n.append("{},{}".format(coord.x+x, coord.y+y))
    return n


n = 0
while True:
    n += 1
    if n == int(data):
        part1_answer = int(math.fabs(current.x) + math.fabs(current.y))
    # Create next coord
    steps += 1
    current.x += direction.x
    current.y += direction.y

    # Should we change direction?
    if steps == max_steps:
        direction = rotate_left(direction)
        rotations += 1
        steps = 0
    # Should we increase max steps
    if rotations == 2:
        rotations = 0
        max_steps += 1

    # Part 2
    sum_ = 0
    nearby = get_nearby(current)
    for c in nearby:
        if c in part2:
            sum_ += part2[c]
    part2["{},{}".format(current.x, current.y)] = sum_

    if sum_ > int(data) and part2_answer is None:
        part2_answer = sum_

    if part1_answer is not None and part2_answer is not None:
        break


print("Part one {}".format(part1_answer))
print("Part two {}".format(part2_answer))


