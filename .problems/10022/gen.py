import random


def action(n: int) -> int:
    num = n
    cnt = 0
    while num > 0:
        if num % 10 in [3, 6, 9]:
            cnt += 1
        num //= 10
    if cnt == 0:
        return n
    else:
        return 10000 + cnt


def answer(m: int, n: int) -> int:
    return (m - 1) % n + 1


def get_input_output() -> list[tuple[str, str]]:
    lst = []

    random.seed(10022)

    # 박수 쳐야하는데 안침
    for i in range(2, 22):
        n = random.randint(2, 100)
        m = ((random.randrange(3, 3 ** i) // 10000 + 1) // 10) * 10 + random.choice([3, 6, 9])
        s = ''

        for j in range(1, m):
            s += f'{action(j)}\n'

        lst.append((m, f'{n}\n{s}{m}', f'{answer(m, n)}'))

    # 박수 안쳐야하는데 침
    for _ in range(20):
        n = random.randint(2, 100)
        k = random.randint(1, 5)
        m = 0
        s = ''

        for i in range(k):
            m = m * 10 + random.choice([1, 2, 4, 5, 7, 8, 0])
        if m == 0:
            m = random.choice([1, 2, 4, 5, 7, 8])

        for i in range(1, m):
            s += f'{action(i)}\n'

        lst.append((m, f'{n}\n{s}{10000 + random.choice([1, 2, 3, 4])}', f'{answer(m, n)}'))

    # 박수 횟수 틀림
    for i in range(2, 22):
        n = random.randint(2, 100)
        m = ((random.randrange(3, 3 ** i) // 10000 + 1) // 10) * 10 + random.choice([3, 6, 9])
        s = ''

        for j in range(1, m):
            s += f'{action(j)}\n'

        lst.append(
            (m, f'{n}\n{s}{10000 + random.choice([i for _ in range(1, 6) if i != action(m) % 10])}', f'{answer(m, n)}'))

    # 숫자 틀림
    for _ in range(20):
        n = random.randint(2, 100)
        k = random.randint(1, 5)
        m = 0
        s = ''

        for i in range(k):
            m = m * 10 + random.choice([1, 2, 4, 5, 7, 8, 0])
        if m == 0:
            m = random.choice([1, 2, 4, 5, 7, 8])

        for i in range(1, m):
            s += f'{action(i)}\n'

        lst.append((m, f'{n}\n{s}{(lambda: action(m) + 1 if action(m) % 2 == 1 else action(m) - 1)()}', f'{answer(m, n)}'))

    lst.sort()
    rtn = [('3\n1\n2\n10001\n4\n5\n10001\n7\n8\n10001\n10\n11\n12\n13', '1')]
    for tpl in lst:
        rtn.append((tpl[1], tpl[2]))

    return rtn
