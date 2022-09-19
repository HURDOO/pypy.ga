import os
import random
from pathlib import Path


def get_input_output() -> list[tuple[str, str]]:
    lst = []

    for a, aa in [('1', '짜장면'), ('2', '짬뽕')]:
        for b, bb in [('3', '찍먹'), ('4', '부먹')]:
            for c, cc in [('5', '민초'), ('6', '반민초')]:
                lst.append((f'{a}\n{b}\n{c}', f'나는 {aa}를 좋아하고, {bb}파고, {cc}파야!'))

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
