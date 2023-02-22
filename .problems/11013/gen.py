import random


def get_input_output() -> list[tuple[str, str]]:
    lst = [('3\ny\n5\ny\n7\nn', '합계는: 15')]

    random.seed(10013)

    for _ in range(30):
        val = ''
        cnt = random.randint(1, 10)
        ans = 0

        for i in range(cnt):
            num = random.randint(1, 10)
            ans += num

            val += str(num) + '\n'
            if i != cnt-1:
                val += 'y\n'
            else:
                val += 'n\n'

        lst.append((val, '합계는: ' + str(ans)))

    return lst
