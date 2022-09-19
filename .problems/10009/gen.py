import random


def get_input_output() -> list[tuple[str, str]]:
    lst = [('95', 'A'), ('60', 'B'), ('80', 'A'), ('100', 'A'), ('0', 'C')]
    random.seed(10009)

    for _ in range(5):
        n = 95
        while n != 95:
            n = random.randint(81, 99)
        lst.append((str(n), 'A'))

    for _ in range(5):
        n = random.randint(61, 79)
        lst.append((str(n), 'B'))

    for _ in range(5):
        n = random.randint(1, 59)
        lst.append((str(n), 'C'))

    return lst
