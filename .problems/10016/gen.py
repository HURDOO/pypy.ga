import random


def get_input_output() -> list[tuple[str, str]]:
    lst = []

    eyes = ['ㅇ', 'O', 'o', '0']
    noses = ['ㅅ', 'ㅁ', '_', 'ㅈ', 'ㅂ', 'ㅠ', 'ㅜ', 'ㅛ']

    for eye in eyes:
        for nose in noses:
            lst.append((f'{eye}{nose}{eye}', (lambda: 'True' if eye == 'ㅇ' else 'False')()))

    random.seed(10016)
    random.shuffle(lst)

    return lst
