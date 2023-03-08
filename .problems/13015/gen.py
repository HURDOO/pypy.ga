import random


def get_answer(i, j):
    # 1행 1열의 값
    result = 1

    # i행 1열의 값
    for x in range(i - 1):
        # 컴퓨터는 0부터 센다는 걸 잊지 말자고요!
        result = result + (2 + x)

    # i행 j열의 값
    for y in range(j - 1):
        result = result + i + y

    return result


def get_input_output() -> list[tuple[str, str]]:
    lst = [("4\n1", "10"), ("10\n10", "181"), ("2\n3", "8"), ("1\n1", "1")]

    random.seed(13015)

    for _ in range(30):
        i = random.randint(1, 100)
        j = random.randint(1, 100)
        result = get_answer(i, j)
        lst.append((f"{i}\n{j}", f"{result}"))

    return lst
