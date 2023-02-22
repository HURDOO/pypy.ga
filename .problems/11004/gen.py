import random


def get_input_output() -> list[tuple[str, str]]:
    lst = []

    random.seed(11004)

    for _ in range(30):
        price = random.randint(0, 70000)

        if price < 20000:
            ans = '새벽배송이 불가능합니다.'
        elif price < 50000:
            ans = '배송비 2500원이 추가됩니다.'
        else:
            ans = '무료배송 됩니다.'

        lst.append((str(price), ans))

    lst.extend([
        ('20000', '배송비 2500원이 추가됩니다.'),
        ('50000', '무료배송 됩니다.')
    ])

    return lst
