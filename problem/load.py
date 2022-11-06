# import requests
import yaml
from pypyga.settings import BASE_DIR

PROBLEMS_LIST = []
PROBLEM_MD = {}
PROBLEM_LEVEL = dict()

PROBLEMS_DIR = BASE_DIR / '.problems'


def load_problems():
    global PROBLEMS_LIST
    with open(PROBLEMS_DIR / 'list.yml', encoding='UTF-8') as f:
        PROBLEMS_LIST = yaml.load(f.read(), Loader=yaml.FullLoader)
    for category in PROBLEMS_LIST:
        for problem in category['problems']:
            problem_id = str(problem['id'])
            PROBLEM_LEVEL[problem_id] = problem['level']
            with open(PROBLEMS_DIR / problem_id / (problem_id + '.md'), encoding='UTF-8') as f:
                PROBLEM_MD[problem_id] = f.read()


load_problems()
