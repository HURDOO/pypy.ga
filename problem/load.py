import requests
import yaml
from pypyga.settings import conf, BASE_DIR


PROBLEMS_LIST_URL = conf['url']['problem_list']
PROBLEM_URL = conf['url']['problem']
PROBLEMS_LIST = []
PROBLEM_LEVEL = dict()

PROBLEMS_DIR = BASE_DIR / '.problems'


def load_problems():
    global PROBLEMS_LIST
    PROBLEMS_LIST = yaml.load(requests.get(PROBLEMS_LIST_URL).text, Loader=yaml.FullLoader)
    # with open(PROBLEMS_DIR / 'list.yml', encoding='UTF-8') as f:
    #     PROBLEMS_LIST = yaml.load(f.read(), Loader=yaml.FullLoader)
    for category in PROBLEMS_LIST:
        for problem in category['problems']:
            PROBLEM_LEVEL[str(problem['id'])] = problem['level']
