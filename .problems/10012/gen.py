import random


def get_input_output() -> list[tuple[str, str]]:
    lst = []

    random.seed(10012)

    for i in range(1, 11):
        for j in range(1, 11):
            lst.append((f'{i}\n{j}', str(i+j)))

    random.shuffle(lst)

    return lst
