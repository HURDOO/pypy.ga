import os
import random
from pathlib import Path


def get_input_output() -> list[tuple[str, str]]:
    lst = [('1000\n2000\n3000\n5000\n5000', '6000원'),
           ('1000\n2000\n3000\n6000\n13000', '10000원'),
           ('1000\n2000\n3000\n10000\n15000', '배달 불가')]

    random.seed(10011)

    for _ in range(10):
        a = random.randint(1, 100) * 100
        b = random.randint(1, 100) * 100
        c = random.randint(1, 100) * 100
        hap = a+b+c

        d = hap - random.randint(0, 100) * 100
        e = d + random.randint(0, (hap-d)//100) * 100
        lst.append((f'{a}\n{b}\n{c}\n{d}\n{e}', f'{hap}원'))

        d = hap - random.randint(0, 100) * 100
        e = hap + random.randint(0, 100) * 100
        lst.append((f'{a}\n{b}\n{c}\n{d}\n{e}', f'{hap+4000}원'))

        d = hap + random.randint(0, 100) * 100
        e = d + random.randint(0, 100) * 100
        lst.append((f'{a}\n{b}\n{c}\n{d}\n{e}', '배달 불가'))

    uk = 100000000

    for _ in range(50):
        a = random.randint(1, uk)
        b = random.randint(1, uk)
        c = random.randint(1, uk)
        hap = a+b+c

        d = random.randint(0, uk*3)
        e = d + random.randint(0, abs(hap-d))
        lst.append((f'{a}\n{b}\n{c}\n{d}\n{e}',
                   (lambda: '배달 불가' if hap < d
                    else (lambda: f'{hap+4000}원' if hap < e else f'{hap}원')()
                    )()
                    ))

    for _ in range(6):
        a = random.randint(1, uk)
        b = random.randint(1, uk)
        c = random.randint(1, uk)
        hap = a+b+c

        d, e = 0, 0
        lst.append((f'{a}\n{b}\n{c}\n{d}\n{e}', f'{hap}원'))

        d, e = 0, hap + random.randint(0, uk*3-hap)
        lst.append((f'{a}\n{b}\n{c}\n{d}\n{e}', f'{hap+4000}원'))

        d, e = hap - random.randint(0, uk*3-hap), 0
        lst.append((f'{a}\n{b}\n{c}\n{d}\n{e}', f'{hap}원'))

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
