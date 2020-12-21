from utils import api

YEAR, DAY = 2020, 21


class Food:
    allergens: list[str]
    ingredients: list[str]

    def __init__(self, ingredients, allergens):
        self.ingredients = ingredients
        self.allergens = allergens


def parse_input(data):
    foods = []
    # mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    for row in data:
        split = row.split("(")
        foods.append(
            Food(ingredients=split[0].strip().split(' '),
                 allergens=[a.strip() for a in row.split('(')[1][8:-1].split(',')])
        )
    return foods


def build_allergen_maps(foods):
    allergens = {}
    allergen_count = {}
    for food in foods:
        for allergen in food.allergens:
            allergen_count[allergen] = allergen_count.get(allergen, 0) + 1
            allergens.setdefault(allergen, {})
            for ingredient in food.ingredients:
                allergens[allergen][ingredient] = allergens[allergen].get(ingredient, 0) + 1
    return allergens, allergen_count


def part1(data):
    foods = parse_input(data)
    allergens, allergen_count = build_allergen_maps(foods)

    non_allergens = set()
    for allergen, ingredients_count in allergens.items():
        for ingredient, count in ingredients_count.items():
            if count != allergen_count[allergen]:
                non_allergens.add(ingredient)
    for allergen, ingredients_count in allergens.items():
        for ingredient, count in ingredients_count.items():
            if ingredient in non_allergens and count == allergen_count[allergen]:
                non_allergens.remove(ingredient)

    part1_answer = 0
    for ingredient in non_allergens:
        for food in foods:
            if ingredient in food.ingredients:
                part1_answer += 1
    return part1_answer, non_allergens


def part2(data, non_allergens):
    foods = parse_input(data)

    for food in foods:
        for non_allergen in non_allergens:
            if non_allergen in food.ingredients:
                food.ingredients.remove(non_allergen)

    allergens, allergen_count = build_allergen_maps(foods)
    allergen_ingredient = {}
    while len(allergen_ingredient) < len(allergens):
        for allergen, ingredient_count in allergens.items():
            matches = []
            for ingredient, count in ingredient_count.items():
                if count == allergen_count[allergen] and ingredient not in allergen_ingredient.values():
                    matches.append(ingredient)
            if len(matches) == 1:
                allergen_ingredient[allergen] = matches[0]

    return ",".join([allergen_ingredient[x] for x in sorted(allergen_ingredient.keys())])


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1[0], p1_time))
    assert p1[0] == 2287

    p2, p2_time = api.time_it(part2, data, p1[1])
    print("Part two {}, it took {} ms".format(p2, p2_time))
    assert p2 == 'fntg,gtqfrp,xlvrggj,rlsr,xpbxbv,jtjtrd,fvjkp,zhszc'


solve()
