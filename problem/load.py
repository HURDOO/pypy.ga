import requests
import json
from pypyga.settings import conf


PROBLEMS_LIST_URL = conf['url']['problem_list']
PROBLEM_URL = conf['url']['problem']
PROBLEMS_LIST = []


def load_problems():
    global PROBLEMS_LIST
    PROBLEMS_LIST = json.loads(requests.get(PROBLEMS_LIST_URL).text)
