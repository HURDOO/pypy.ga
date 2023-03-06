import random


def calc(a: int, b: int, sign: str) -> str:
    if sign == '+':
        return str(a+b)
    elif sign == '-':
        return str(a-b)
    elif sign == '*':
        return str(a*b)
    else:
        return str(a/b)


def get_input_output() -> list[tuple[str, str]]:
    lst = []
    for sign in ['+', '-', '*', '/']:
        lst.append(("5\n" + sign + "\n2", calc(5, 2, sign)))

    random.seed(13013)
    for i in range(1, 97):
        a = random.randint(-1000*i, 1000*i)
        b = random.randint(-1000*i, 1000*i)
        sign = random.sample(['+', '-', '*', '/'], k=1)[0]

        lst.append((f"{a}\n{sign}\n{b}", calc(a, b, sign)))

    return lst
