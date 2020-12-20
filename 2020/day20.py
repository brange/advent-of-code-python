from utils import api
import math

YEAR, DAY = 2020, 20

LEFT, UPPER, RIGHT, LOWER = 0, 1, 2, 3


class TileContent:
    def __init__(self, data):
        self.raw_data = data
        upper = "".join(data[0])
        lower = "".join(data[-1])
        left = ""
        right = ""
        content = []
        for line in data:
            left += line[0]
            right += line[-1]
            content.append(line[1:-1])
        self.content = content[1:-1]
        self.boundaries = (left, upper, right, lower)


def flip_y(matrix_):
    return matrix_[::-1]


def flip_x(matrix_):
    flipped = []
    for row in matrix_:
        flipped.append(row[::-1])
    return flipped


def rotate(matrix_):
    return list(zip(*matrix_))[::-1]


class Tile:
    def __init__(self, tile_id):
        self.tile_id = tile_id
        self.tile_content = list()
        self.active_tile_content = None
        self.matches = set()


def parse_input(data):
    tiles = []
    for tile_data in data.split("\n\n"):
        tile_data = tile_data.split("\n")
        tile_id = int(tile_data[0].split(" ")[1].split(":")[0])
        tile = Tile(tile_id)
        tiles.append(tile)

        tile_content = []
        for row in tile_data[1:]:
            tile_content.append([c for c in row])
        for _ in range(4):
            tile.tile_content.append(TileContent(tile_content))
            tile.tile_content.append(TileContent(flip_y(tile_content)))
            tile_content = rotate(tile_content)

    return tiles


def find_matches(tiles):
    for tile in tiles:
        for other_tile in tiles:
            if other_tile == tile:
                continue
            for b1 in tile.tile_content:
                for b2 in other_tile.tile_content:
                    for b in b1.boundaries:
                        if b in b2.boundaries:
                            tile.matches.add(other_tile)
                            break
                    else:
                        break
                else:
                    break


def build_image(all_tiles, width, used_tiles={}, x=0, y=0):
    num_matches = 2
    if 0 < x < width - 1:
        num_matches += 1
    if 0 < y < width - 1:
        num_matches += 1

    tiles = set()
    if x > 0:
        for t in used_tiles[(x - 1, y)].matches:
            tiles.add(t)
    if y > 0:
        for t in used_tiles[(x, y - 1)].matches:
            tiles.add(t)
    if len(tiles) == 0:
        tiles = all_tiles
    used_tiles_ = used_tiles.copy()
    for tile in filter(lambda s: s not in used_tiles.values() and len(s.matches) == num_matches, tiles):
        for tile_content in tile.tile_content:
            if x > 0:
                if tile_content.boundaries[LEFT] != used_tiles[(x - 1, y)].active_tile_content.boundaries[RIGHT]:
                    continue
            if y > 0:
                if tile_content.boundaries[UPPER] != used_tiles[(x, y - 1)].active_tile_content.boundaries[LOWER]:
                    continue
            # It fits
            tile.active_tile_content = tile_content
            used_tiles_[(x, y)] = tile
            if x == y == width - 1:
                # Ok, done!
                return used_tiles_
            x_next, y_next = x, y
            if x_next + 1 == width:
                x_next = 0
                y_next += 1
            else:
                x_next += 1
            next_image = build_image(all_tiles, width, used_tiles_, x_next, y_next)
            if next_image:
                return next_image
    return False


def part1(tiles):
    res = 1
    for tile in tiles:
        if len(tile.matches) == 2:
            res *= tile.tile_id

    return res


def part2(tiles):
    size = int(math.sqrt(len(tiles)))
    a = build_image(tiles, size)

    image = []
    for y in range(size):
        row = {}
        for x in range(size):
            tile = a[(x, y)]
            for content_index in range(len(tile.active_tile_content.content)):
                if x == 0:
                    row[content_index] = []
                row[content_index].extend(tile.active_tile_content.content[content_index])
        for line in row.values():
            image.append(line)
    num_hash_in_monster = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".count("#")

    num_hash = 0
    for y in image:
        num_hash += "".join(y).count("#")
    num_sea_monsters = find_sea_monster(image)
    assert num_sea_monsters > 0

    return num_hash - num_sea_monsters * num_hash_in_monster


def find_sea_monster(image):
    monster = [(18, 0),
               (0, 1), (5, 1), (6, 1), (11, 1), (12, 1), (17, 1), (18, 1), (19, 1),
               (1, 2), (4, 2), (7, 2),
               (10, 2), (13, 2), (16, 2)]

    def find(image_):
        max_y = len(image_)
        num_sea_monsters = 0
        for y in range(max_y):
            max_x = len(image_[y])
            for x in range(max_x):
                all_ok = True
                for monster_bit in monster:
                    monster_x = monster_bit[0] + x
                    monster_y = monster_bit[1] + y
                    if not (monster_x < max_x and monster_y < max_y and image_[monster_y][monster_x] == '#'):
                        all_ok = False
                        break
                if all_ok:
                    num_sea_monsters += 1
        return num_sea_monsters

    for _ in range(4):
        images = [image, flip_y(image)]
        image = rotate(image)
        for image_ in images:
            n = find(image_)
            if n > 0:
                return n


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip()

    tiles = parse_input(data)
    find_matches(tiles)

    p1, p1_time = api.time_it(part1, tiles)
    print("Part one {}, it took {} ms".format(p1, p1_time))
    assert p1 == 79412832860579

    p2, p2_time = api.time_it(part2, tiles)
    print("Part two {}, it took {} ms".format(p2, p2_time))
    assert p2 == 2155


solve()
