import random


def get_input_output():
    lst = []

    random.seed(11006)

    for _ in range(30):
        score = random.randint(0, 100)
        if score < 0 or score > 100:
            ans = '잘못된 숫자를 입력했습니다.'
        elif score >= 80:
            ans = 'A 등급'
        elif score >= 40:
            ans = 'B 등급'
        else:
            ans = 'C 등급'

        lst.append((str(score), ans))

    lst.extend([
        ('80', 'A 등급'),
        ('40', 'B 등급'),
        ('0', 'C 등급'),
        ('100', 'A 등급')
    ])

    return lst
