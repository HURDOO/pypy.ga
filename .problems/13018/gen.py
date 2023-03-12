import random


def get_values(n: int) -> str:
    lst = []
    i = 2

    while n > 1:
        if n % i == 0:
            lst.append(str(i))
            while n % i == 0:
                n //= i
        i += 1

    return "\n".join(lst)


def get_input_output() -> list[tuple[str, str]]:
    lst = [("12", "2\n3")]

    random.seed(13018)

    for _ in range(10):
        n = random.randint(10, 100)
        values = get_values(n)
        lst.append((f"{n}", f"{values}"))

    for _ in range(30):
        n = random.randint(100, 1000)
        values = get_values(n)
        lst.append((f"{n}", f"{values}"))

    return lst
