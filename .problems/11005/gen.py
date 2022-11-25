import random


def get_input_output() -> list[tuple[str, str]]:
    lst = []

    random.seed(11005)

    for i in range(0, 101):
        ans = ''
        if i >= 60:
            ans = '합격\n'
        ans += '프로그램 종료'
        lst.append((str(i), ans))

    random.shuffle(lst)
    return lst
