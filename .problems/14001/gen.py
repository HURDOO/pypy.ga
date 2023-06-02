import random


def bs(base_cnt, animal_cnt, gun_length, bases, animals):

    bases.sort()

    cnt = 0
    for animal in animals:

        x, y = animal[0], animal[1]

        left = 1
        right = base_cnt

        while left <= right:
            mid = (left+right) // 2

            base = bases[mid-1]
            distance = abs(base-x)+y

            if distance <= gun_length:
                cnt += 1
                break

            else:
                if x >= base:
                    left = mid+1
                else:
                    right = mid-1

    return cnt


def get_input_output() -> list[tuple[str, str]]:
    arr = [(
        """4 8 4
6 1 4 9
7 2
3 3
4 5
5 1
2 2
1 4
8 4
9 4
""",
        "6"), (
        """1 5 3
3
2 2
1 1
5 1
4 2
3 3
""",
        "5"
    )]

    random.seed(14001)
    for i in range(5):
        base_cnt = random.randint(1, 10)
        animal_cnt = random.randint(5, 15)
        gun_length = random.randint(1, 30)

        bases = random.sample(range(1, base_cnt+1), base_cnt)
        animals_x = random.sample(range(1, 31), animal_cnt)
        animals_y = random.sample(range(1, 31), animal_cnt)

        print(base_cnt, animal_cnt, gun_length)
        print(bases)

        animals = []
        for j in range(animal_cnt):
            animals.append((animals_x[j], animals_y[j]))

        print(animals)

        result = bs(base_cnt, animal_cnt, gun_length, bases, animals)

        print(result)

        input_val = f'{base_cnt} {animal_cnt} {gun_length}\n'
        for j in range(base_cnt):
            if j == 0:
                input_val += str(bases[j])
            else:
                input_val += " " + str(bases[j])

        for animal in animals:
            input_val += f"\n{animal[0]} {animal[1]}"

        arr.append((input_val, str(result)))
        # print(arr)

    return arr
