from utils import api
import time

data = api.fetch(2017, 5)


def create_arr(d):
    return list(map(int, d.split("\n")))


def solve(arr, part2):
    t = time.process_time()
    index, steps, l = 0, 0, len(arr)
    while index < l:
        s = arr[index]
        steps += 1
        if part2 and s >= 3:
            arr[index] -= 1
        else:
            arr[index] += 1
        index += s
    t = time.process_time() - t
    print("It took {}".format(t))
    return steps


print("part one {}".format(solve(create_arr(data), False)))
print("part two {}".format(solve(create_arr(data), True)))
