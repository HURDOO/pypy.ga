from problem.load import PROBLEMS_DIR


def handle_data(output: str, problem_id: int, case_idx: int) -> bool:
    with open(PROBLEMS_DIR / str(problem_id) / 'out' / '{}.out'.format(case_idx), 'r', encoding='UTF-8') as answer_file:
        answer = answer_file.read()
        return output.rstrip() == answer.rstrip()
