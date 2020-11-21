from utils import api

data = api.fetch(2017, 1)
print(data)

part1, part2 = 0, 0
for i in range(0, len(data)):
    a = data[i]
    if i+1 < len(data):
        b = data[i+1]
    else:
        b = data[0]
    if a == b:
        part1 += int(a)

    # part2
    bi = int(i + len(data) / 2)
    if bi >= len(data):
        bi -= len(data)
    if a == data[bi]:
        part2 += int(a)

print("Part one {}".format(part1))
print("Part two {}".format(part2))