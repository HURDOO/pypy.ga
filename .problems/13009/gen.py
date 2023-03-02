import random


def get_input_output() -> list[tuple[str, str]]:

    lst = [("10\n5", "True"), ("10\n20", ""), ("10\n10", "")]
    random.seed(13009)

    for i in range(10):
        x = random.randint(-100, 100)
        y = random.randint(-100, 100)

        input_value = f"{x}\n{y}"
        if x > y:
            lst.append((input_value, "True"))
        else:
            lst.append((input_value, ""))

    return lst
