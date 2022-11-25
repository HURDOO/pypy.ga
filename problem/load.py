# import requests
import yaml

from account import info
from pypyga.settings import BASE_DIR

PROBLEMS_LIST = []
PROBLEM_MD = {}
PROBLEM_LEVEL = {}
PROBLEM_PERMS = {}
PROBLEM_CODE = {}

PROBLEMS_DIR = BASE_DIR / '.problems'


def has_permission(user_id: int, problem_id: int):
    if str(problem_id) in PROBLEM_PERMS:
        perm = PROBLEM_PERMS[str(problem_id)]
        if user_id is None or not info.has_permission(user_id, perm):
            return False
    return True


def load_problems():
    global PROBLEMS_LIST
    with open(PROBLEMS_DIR / 'list.yml', encoding='UTF-8') as f:
        PROBLEMS_LIST = yaml.load(f.read(), Loader=yaml.FullLoader)

    for category in PROBLEMS_LIST:
        for problem in category['problems']:
            problem_id = str(problem['id'])
            PROBLEM_LEVEL[problem_id] = problem['level']

            # Read .md
            with open(PROBLEMS_DIR / problem_id / (problem_id + '.md'), encoding='UTF-8') as f:
                PROBLEM_MD[problem_id] = f.read()

            # Read serve.py
            if 'serve_code' in problem:
                with open(PROBLEMS_DIR / problem_id / 'serve.py', encoding='UTF-8') as f:
                    PROBLEM_CODE[problem_id] = f.read()

    global PROBLEM_PERMS
    with open(PROBLEMS_DIR / 'perm.yml', encoding='UTF-8') as f:
        PROBLEM_PERMS = yaml.load(f.read(), Loader=yaml.FullLoader)
    if PROBLEM_PERMS is None:
        PROBLEM_PERMS = {}


load_problems()
