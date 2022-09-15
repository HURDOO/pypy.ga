import os
import random
from pathlib import Path


def get_input_output() -> list[tuple[str, str]]:
    lst = [('4\n2', '6\n2\n8\n2.0'), ('5\n3', '8\n2\n15\n1.6666666666666667')]

    random.seed(10006)

    # 1 <= b <= a <= 100
    for i in range(48):
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        a, b = max(a, b), min(a, b)
        lst.append((get_input(a, b), get_output(a, b)))

    # 1 <= a,b <= 1,0000,0000
    for i in range(50):
        a = random.randint(1, 100000000)
        b = random.randint(1, 100000000)
        lst.append((get_input(a, b), get_output(a, b)))

    return lst


def get_input(a: int, b: int) -> str:
    return f'{a}\n{b}'


def get_output(a: int, b: int) -> str:
    return f'{a+b}\n{a-b}\n{a*b}\n{a/b}'


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
