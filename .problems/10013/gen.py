import os
import random
from pathlib import Path


def get_input_output() -> list[tuple[str, str]]:
    lst = []

    for a in ['짜장면', '짬뽕']:
        for b in ['신라면', '진라면']:
            for c in ['물냉면', '비빔냉면']:
                for d in ['파스타', '스파게티']:
                    lst.append((f'{a}\n{b}\n{c}\n{d}', f'{a}하고 {b}하고 {c}하고 {d}'))

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
