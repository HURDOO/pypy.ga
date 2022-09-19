import random


def get_input_output() -> list[tuple[str, str]]:
    lst = [('4\n2', '6\n2\n8\n2.0'), ('5\n3', '8\n2\n15\n1.6666666666666667')]

    random.seed(10006)

    # 1 <= b <= a <= 100
    for i in range(48):
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        a, b = max(a, b), min(a, b)
        lst.append((get_input(a, b), get_output(a, b)))

    # 1 <= a,b <= 1,0000,0000
    for i in range(50):
        a = random.randint(1, 100000000)
        b = random.randint(1, 100000000)
        lst.append((get_input(a, b), get_output(a, b)))

    return lst


def get_input(a: int, b: int) -> str:
    return f'{a}\n{b}'


def get_output(a: int, b: int) -> str:
    return f'{a+b}\n{a-b}\n{a*b}\n{a/b}'
