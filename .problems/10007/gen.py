import random


def get_input_output() -> list[tuple[str, str]]:
    lst = [('2022', '2565')]
    random.seed(10007)
    for _ in range(99):
        n = random.randint(0, 2999)
        lst.append((str(n), str(n+543)))
    return lst
