import os
from pathlib import Path


def get_input_output() -> list[tuple[str, str]]:
    lst = []
    for s in '유은미, 황광희, 정희선, 봉인태, 예미영, 설현빈, 문남혁, 이현빈, 황은경, 강연진' \
            ', 문민웅, 홍영우, 권선희, 제갈문철, 류명진, 문시우, 봉설현, 김다연, 복용남, 남궁지희'.split(', '):
        lst.append((s, s))
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
    with open(INPUT_DIR / INPUT_FILENAME.format(idx+1), 'w', encoding='UTF-8') as input_file:
        input_file.write(stdin + '\n')
    with open(OUTPUT_DIR / OUTPUT_FILENAME.format(idx+1), 'w', encoding='UTF-8') as output_file:
        output_file.write(stdout + '\n')
