from utils import  api

data = api.fetch(2017, 4)

lines = data.split("\n")
part1_answer = 0
part2_answer = 0
for line in lines:
    words = line.split(" ")
    if len(words) == len(set(words)):
        part1_answer += 1

        # part 2
        sorted_words = []
        for word in words:
            sorted_words.append("".join(sorted(word)))
        if len(sorted_words) == len(set(sorted_words)):
            part2_answer += 1


print("Part one: {}".format(part1_answer))
print("Part two: {}".format(part2_answer))
