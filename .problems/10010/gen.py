import random


def get_input_output() -> list[tuple[str, str]]:
    lst = [('1\n1', '평행'), ('1\n0', '만남'), ('1\n-1', '만남\n수직')]

    random.seed(10010)

    uk = 100000000

    for _ in range(30):
        n = random.randint(-uk, uk)
        lst.append((f'{n}\n{n}', '평행'))

    for _ in range(30):
        a = b = 0
        while a == b:
            a = random.randint(-uk, uk)
            b = random.randint(-uk, uk)
        lst.append((f'{a}\n{b}', '만남'))

    for i in range(1, 13):
        n = 2 ** i
        m = -1 / n
        lst.append((f'{n}\n{m}', '만남\n수직'))

    for i in range(1, 6):
        n = 5 ** i
        m = -1 / n
        lst.append((f'{n}\n{m}', '만남\n수직'))

    return lst
