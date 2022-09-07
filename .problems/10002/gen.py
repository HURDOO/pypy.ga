import os
from pathlib import Path


def get_input_output() -> list[tuple[str, str]]:
    return [('', """한겨레 한마음으로 큰 뜻을 펼친
한강의 복된 기슭에 갈고 닦은 배움터
내일은 새로운 장 배우고 익히세
아- 늘 푸른 희망의 전당 그 이름 잠신
밝은 마음 알찬 슬기 바른 행실로
진리 찾는 보금자리 우리의 잠신""")]


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
