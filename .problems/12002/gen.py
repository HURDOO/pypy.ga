import random


def get_input_output() -> list[tuple[str,str]]:
    lst = [('5\n1\n2\n3\n4\n5', '5\n4\n3\n2\n1')]
    random.seed(12002)
    for _ in range(10):
        n = random.randint(1, 100)
        input_str = str(n)

        arr = []
        for __ in range(n):
            m = random.randint(1, 100)
            input_str += '\n' + str(m)
            arr.append(m)

        output_str = ""
        for i in arr[::-1]:
            output_str += str(i) + '\n'

        lst.append((input_str, output_str))

    return lst
