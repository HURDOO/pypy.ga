import random


def get_input_output() -> list[tuple[str, str]]:
    lst = []

    random.seed(11003)

    for _ in range(30):
        weight = random.randint(35, 100)
        height = random.randrange(120, 200)

        bmi = weight/height**2*10000

        if bmi < 18.5:
            ans = '마른 체형입니다.'
        elif bmi < 25:
            ans = '표준입니다.'
        elif bmi < 30:
            ans = '비만입니다.'
        else:
            ans = '고도 비만입니다.'

        lst.append((f'{height}\n{weight}', ans))

    lst.extend([
        ('180\n59.94', '표준입니다.'),  # bmi = 18.5
        ('180\n81', '비만입니다.'),  # bmi = 25
        ('160\n76.8', '고도 비만입니다.')  # bmi = 30
    ])

    return lst
