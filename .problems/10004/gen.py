import os
from pathlib import Path


def get_input_output() -> list[tuple[str, str]]:
    lst = [('강호\n강호', "'강호'\n\"강호\"")]
    for s in '박유민, 배철희, 홍기준, 사공윤주, 노연재, 류윤태, 임시원, 탁경선, 백서은, 심명숙' \
             ', 복시정, 김경호, 김재웅, 사공명원, 예원빈, 장문용, 사공석호, 안정우, 복소미, 김시아'.split(', '):
        lst.append((f"{s}\n{s}", "'{}'\n\"{}\"".format(s, s)))
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
