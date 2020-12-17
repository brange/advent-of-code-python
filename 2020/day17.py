from utils import api

YEAR, DAY = 2020, 17


class Cube:
    def __init__(self, x, y, z, w, use_w, active):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.active = active
        self.active_next = None
        self.neighbor_keys = {}
        delta = [-1, 0, 1]
        w_delta = delta if use_w else [0]
        for x_diff in delta:
            for y_diff in delta:
                for z_diff in delta:
                    for w_diff in w_delta:
                        if x_diff == y_diff == z_diff == w_diff == 0:
                            continue
                        key = cube_key(x + x_diff, y + y_diff, z + z_diff, w + w_diff)
                        if key in self.neighbor_keys:
                            self.neighbor_keys[key] = self.neighbor_keys[key] + 1
                        else:
                            self.neighbor_keys[key] = 1

    def key(self):
        return cube_key(self.x, self.y, self.z, self.w)


def cube_key(x, y, z, w):
    # abs(z) and abs(w) because of symmetry
    return x, y, abs(z), abs(w)


def parse_input(data, use_w):
    y = 0
    cubes = []
    for row in data:
        x = 0
        for c in row:
            cubes.append(Cube(x, y, 0, 0, use_w, c == '#'))
            x = x + 1
        y = y + 1
    return cubes


def run(data, w_diff=0):
    cubes = dict()
    x_min, y_min = 0, 0
    x_max, y_max, z_max, w_max = 0, 0, 1, 1
    for cube in parse_input(data, w_diff > 0):
        cubes[cube.key()] = cube
        x_max = max(x_max, cube.x)
        y_max = max(y_max, cube.y)
    x_max += 1
    y_max += 1

    for round_ in range(0, 6):
        changed = []

        # Add new cubes.
        x_min -= 1
        x_max += 1
        y_min -= 1
        y_max += 1
        z_max += 1
        w_max += w_diff

        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                for z in range(0, z_max):
                    for w in range(0, w_max):
                        key = cube_key(x, y, z, w)
                        if key not in cubes:
                            cubes[key] = Cube(x, y, z, w, w_diff > 0, False)

        for cube in cubes.values():
            num_active = 0
            for key, worth in cube.neighbor_keys.items():
                if key in cubes:
                    if cubes[key].active:
                        num_active += worth
                if num_active > 3:
                    break
            if cube.active:
                if not (2 <= num_active <= 3):
                    cube.active_next = False
                    changed.append(cube)
            else:
                if num_active == 3:
                    cube.active_next = True
                    changed.append(cube)
        for cube in changed:
            cube.active = cube.active_next

    res = 0
    for cube in cubes.values():
        if cube.active:
            if cube.z > 0 and cube.w > 0:
                res += 4
            elif cube.z > 0 or cube.w > 0:
                res += 2
            else:
                res += 1
    return res


def part1(data):
    return run(data, 0)


def part2(data):
    return run(data, 1)


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))
    assert p1 == 359

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))
    assert p2 == 2228


solve()
