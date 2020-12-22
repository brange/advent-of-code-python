from utils import api
from enum import IntEnum


class PLAYER(IntEnum):
    ONE = 1
    TWO = 2


YEAR, DAY = 2020, 22


def play_combat(player1, player2):
    while len(player1) > 0 and len(player2) > 0:
        p1, player1 = player1[0], player1[1:]
        p2, player2 = player2[0], player2[1:]
        if p1 > p2:
            player1.extend([p1, p2])
        else:
            player2.extend([p2, p1])

    return player1, player2


def part1(data):
    data = data.replace('Player 1:\n', '').replace('Player 2:\n', '')

    player1 = list(map(int, data.split("\n\n")[0].split("\n")))
    player2 = list(map(int, data.split("\n\n")[1].split("\n")))

    player1, player2 = play_combat(player1, player2)
    winner = player1 if len(player1) > 0 else player2

    score = 0
    multiplier = len(winner)
    for card in winner:
        score += card * multiplier
        multiplier -= 1
    return score


def prev_key(player):
    return tuple(player)


def recursive_combat(player1, player2):
    prev_p1, prev_p2 = set(), set()
    while len(player1) > 0 and len(player2) > 0:
        key1, key2 = prev_key(player1), prev_key(player2)
        if key1 in prev_p1 or key2 in prev_p2:
            player2 = []
            break
        prev_p1.add(key1)
        prev_p2.add(key2)

        p1, player1 = player1[0], player1[1:]
        p2, player2 = player2[0], player2[1:]

        if len(player1) >= p1 and len(player2) >= p2:
            recursive_p1, _ = recursive_combat(player1[:p1], player2[:p2])
            winner = PLAYER.ONE if len(recursive_p1) > 0 else PLAYER.TWO
        else:
            winner = PLAYER.ONE if p1 > p2 else PLAYER.TWO

        if winner == PLAYER.ONE:
            player1.extend([p1, p2])
        else:
            player2.extend([p2, p1])

    return player1, player2


def part2(data):
    data = data.replace('Player 1:\n', '').replace('Player 2:\n', '')

    player1 = list(map(int, data.split("\n\n")[0].split("\n")))
    player2 = list(map(int, data.split("\n\n")[1].split("\n")))

    #player1 = [9, 2, 6, 3, 1]
    #player2 = [5, 8, 4, 7, 10]

    player1, player2 = recursive_combat(player1, player2)

    winner = player1 if len(player1) > 0 else player2
    score = 0
    multiplier = len(winner)
    for card in winner:
        score += card * multiplier
        multiplier -= 1
    return score


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip()

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))
    assert p1 == 32598

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))
    assert p2 == 35836


solve()
