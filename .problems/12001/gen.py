import random


def reverse(n: int) -> str:
    return str((n % 10) * 10 + n // 10)


def get_input_output() -> list[tuple[str, str]]:
    lst = [('12\n34', '2143'), ('90\n16', '961')]
    random.seed(12001)
    for _ in range(10):
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        lst.append((f'{a}\n{b}', f'{reverse(a)+reverse(b)}'))
    return lst
