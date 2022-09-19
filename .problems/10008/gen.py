import random


def get_input_output() -> list[tuple[str, str]]:
    lst = [('2', '사람'), ('3', '원숭이')]
    random.seed(10008)
    for _ in range(5):
        n = random.randint(0, 1000000)
        lst.append((str(n), '원숭이'))

    lst.extend([('귀요미', '원숭이'), ('몰라', '원숭이'), ('우끼끼', '원숭이'), ('우끼끾끼!!', '원숭이'), ('🐵 (해맑)', '원숭이')])
    return lst
