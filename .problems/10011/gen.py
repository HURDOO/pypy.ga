import random


def get_input_output() -> list[tuple[str, str]]:
    lst = [('1000\n2000\n3000\n5000\n5000', '6000원'),
           ('1000\n2000\n3000\n6000\n13000', '10000원'),
           ('1000\n2000\n3000\n10000\n15000', '배달 불가')]

    random.seed(10011)

    for _ in range(10):
        a = random.randint(1, 100) * 100
        b = random.randint(1, 100) * 100
        c = random.randint(1, 100) * 100
        hap = a + b + c

        d = hap - random.randint(0, 100) * 100
        e = d + random.randint(0, (hap - d) // 100) * 100
        lst.append((get_input(a, b, c, d, e), f'{hap}원'))

        d = hap - random.randint(0, 100) * 100
        e = hap + random.randint(0, 100) * 100
        lst.append((get_input(a, b, c, d, e), f'{hap + 4000}원'))

        d = hap + random.randint(0, 100) * 100
        e = d + random.randint(0, 100) * 100
        lst.append((get_input(a, b, c, d, e), '배달 불가'))

    uk = 100000000

    for _ in range(50):
        a = random.randint(1, uk)
        b = random.randint(1, uk)
        c = random.randint(1, uk)
        hap = a + b + c

        d = random.randint(0, uk * 3)
        e = d + random.randint(0, abs(hap - d))
        lst.append((get_input(a, b, c, d, e),
                    (lambda: '배달 불가' if hap < d
                    else (lambda: f'{hap + 4000}원' if hap < e else f'{hap}원')()
                     )()
                    ))

    for _ in range(6):
        a = random.randint(1, uk)
        b = random.randint(1, uk)
        c = random.randint(1, uk)
        hap = a + b + c

        d, e = 0, 0
        lst.append((get_input(a, b, c, d, e), f'{hap}원'))

        d, e = 0, hap + random.randint(0, uk * 3 - hap)
        lst.append((get_input(a, b, c, d, e), f'{hap + 4000}원'))

        d, e = hap - random.randint(0, uk * 3 - hap), 0
        lst.append((get_input(a, b, c, d, e), f'{hap}원'))

    return lst


def get_input(a: int, b: int, c: int, d: int, e: int) -> str:
    return f'{a}\n{b}\n{c}\n{d}\n{e}'
