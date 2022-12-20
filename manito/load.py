import json
import random

import yaml

from . import models
from problem import load

first_day_manito = {}
student_name = {}
second_day_manito = {}

with open(load.PROBLEMS_DIR / 'first_day.yml', encoding='UTF-8') as f:
    first_day_manito = yaml.load(f.read(), yaml.FullLoader)

with open(load.PROBLEMS_DIR / 'students.yml', encoding='UTF-8') as f:
    student_name = yaml.load(f.read(), yaml.FullLoader)

second_day_file = load.PROBLEMS_DIR / 'second_day.yml'
if second_day_file.is_file():
    with open(second_day_file, encoding='UTF-8') as f:
        second_day_manito = yaml.load(f.read(), yaml.FullLoader)

print(student_name)
for student in student_name:
    print(student)
    account = models.get_manito_account(int(student))
    account.gen_balance()


def gen_second_day() -> None:
    if second_day_file.is_file():
        return

    lst = list(range(1, 27))
    lst.remove(5)
    lst.remove(20)

    rand = random.sample(lst, 24)
    for i in range(24):
        second_day_manito[str(lst[i])] = rand[i]

    with open(second_day_file, 'w', encoding='UTF-8') as ff:
        ff.write(yaml.dump(second_day_manito))


gen_second_day()
