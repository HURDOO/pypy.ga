import os
import random
from pathlib import Path


def get_input_output() -> list[tuple[str, str]]:
    lst = [('1\n1', '평행'), ('1\n0', '만남'), ('1\n-1', '만남\n수직')]

    random.seed(10010)

    uk = 100000000

    for _ in range(30):
        n = random.randint(-uk, uk)
        lst.append((f'{n}\n{n}', '평행'))

    for _ in range(30):
        a = b = 0
        while a == b:
            a = random.randint(-uk, uk)
            b = random.randint(-uk, uk)
        lst.append((f'{a}\n{b}', '만남'))

    for _ in range(30):
        n = 0
        while n == 0:
            n = random.randint(-uk, uk)
        lst.append((f'{n}\n{-n}', '만남\n수직'))

    return lst


PROBLEM_DIR = Path(__file__).resolve().parent
INPUT_DIR = PROBLEM_DIR / 'in'
OUTPUT_DIR = PROBLEM_DIR / 'out'
INPUT_FILENAME = '{}.in'
OUTPUT_FILENAME = '{}.out'

if not os.path.exists(INPUT_DIR):
    os.mkdir(INPUT_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

case_list = get_input_output()

for idx in range(len(case_list)):
    stdin, stdout = case_list[idx]
    with open(INPUT_DIR / INPUT_FILENAME.format(idx + 1), 'w', encoding='UTF-8') as input_file:
        input_file.write(stdin + '\n')
    with open(OUTPUT_DIR / OUTPUT_FILENAME.format(idx + 1), 'w', encoding='UTF-8') as output_file:
        output_file.write(stdout + '\n')
