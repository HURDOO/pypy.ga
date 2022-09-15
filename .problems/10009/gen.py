import os
import random
from pathlib import Path


def get_input_output() -> list[tuple[str, str]]:
    lst = [('95', 'A'), ('60', 'B'), ('80', 'A'), ('100', 'A'), ('0', 'C')]
    random.seed(10009)

    for _ in range(5):
        n = 95
        while n != 95:
            n = random.randint(81, 99)
        lst.append((str(n), 'A'))

    for _ in range(5):
        n = random.randint(61, 79)
        lst.append((str(n), 'B'))

    for _ in range(5):
        n = random.randint(1, 59)
        lst.append((str(n), 'C'))

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
