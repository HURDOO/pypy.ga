import requests
import yaml
from pypyga.settings import conf, BASE_DIR


PROBLEMS_LIST_URL = conf['url']['problem_list']
PROBLEM_URL = conf['url']['problem']
PROBLEMS_LIST = []

PROBLEMS_DIR = BASE_DIR / '.problems'


def load_problems():
    global PROBLEMS_LIST
    PROBLEMS_LIST = yaml.load(requests.get(PROBLEMS_LIST_URL).text, Loader=yaml.FullLoader)
