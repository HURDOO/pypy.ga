import random


def get_input_output() -> list[tuple[str, str]]:
    lst = [("36", "True"), ("43", "False")]

    random.seed(13019)

    for _ in range(40):
        n = random.randint(0, 2730)
        answer = True

        m = n
        while m > 1:
            if m % 4 == 3:
                answer = False
            m //= 4

        lst.append((f"{n}", f"{answer}"))

    return lst
