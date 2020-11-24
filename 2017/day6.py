from utils import api


def solve():
    data = api.fetch(2017, 6)

    banks = list(map(int, data.split("\t")))
    print(banks)
    existing = [''.join(map(str, banks))]
    len_ = len(banks)
    turns = 0

    while True:
        turns += 1
        index = 0
        max_ = banks[index]
        for i in range(0, len_):
            if banks[i] > max_:
                max_ = banks[i]
                index = i

        blocks = banks[index]
        banks[index] = 0

        for _ in range(0, blocks):
            index += 1
            banks[index % len_] += 1
        e = ''.join(map(str, banks))
        if e in existing:
            print("It took {} turns (part one)".format(turns))
            assert turns == 3156
            prev = existing.index(e)
            part2 = turns - prev
            assert part2 == 1610
            print("The infinite loop contains {} cycles (part two)".format(part2))
            break
        existing.append(e)


api.time_it(solve)
