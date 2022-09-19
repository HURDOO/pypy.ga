import os
from pathlib import Path
from importlib import import_module

PROBLEMS_DIR = Path(__file__).resolve().parent
INPUT_FILENAME = '{}.in'
OUTPUT_FILENAME = '{}.out'


def generate(case_list: list[tuple[str, str]], problem_id: str) -> None:

    problem_dir = PROBLEMS_DIR / problem_id
    input_dir = problem_dir / 'in'
    output_dir = problem_dir / 'out'

    if not os.path.exists(input_dir):
        os.mkdir(input_dir)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for idx in range(len(case_list)):
        stdin, stdout = case_list[idx]
        with open(input_dir / INPUT_FILENAME.format(idx + 1), 'w',
                  encoding='UTF-8', newline='\n') as input_file:
            input_file.write(stdin + '\n')
        with open(output_dir / OUTPUT_FILENAME.format(idx + 1), 'w',
                  encoding='UTF-8', newline='\n') as output_file:
            output_file.write(stdout + '\n')


if __name__ == '__main__':
    problem = input('문제 번호: ')
    problem_gen = import_module(problem + '.gen')
    print(problem_gen.__file__)
    generate(problem_gen.get_input_output(), problem)
