import random

from korean_name_generator import namer


def get_input_output() -> list[tuple[str, str]]:
    lst = [('5\n이현중\n송강호\n최용훈\n이오름\n김마루', '이현중\n송강호\n최용훈\n이오름\n김마루')]

    random.seed(10021)

    for i in range(2, 16):
        names = ''
        for j in range(i):
            gender = random.random() < 0.5
            name = namer.generate(gender)
            names += name + '\n'
        lst.append((f'{i}\n{names}', names))
    return lst
