import requests
import json

PROBLEMS_LIST_URL = 'https://raw.githubusercontent.com/HURDOO/python-trainer/master/.problems/list.json'
PROBLEM_URL = 'https://raw.githubusercontent.com/HURDOO/python-trainer/master/.problems/{}.md'
PROBLEMS_LIST_HTML = ''
PROBLEMS_LIST = []


def load_problems():
    global PROBLEMS_LIST
    PROBLEMS_LIST = json.loads(requests.get(PROBLEMS_LIST_URL).text)


def load_problems1():
    global PROBLEMS_LIST_HTML
    PROBLEMS_LIST_HTML = """
        <table>
            <tr id="header">
                <th>#</th>
                <th>문제</th>
                <th>난이도</th>
                <th>제출 수</th>
                <th>정답</th>
            </tr>
    """

    response = requests.get(PROBLEMS_LIST_URL)
    categories = json.loads(response.text)

    for category in categories:
        category_name = category['category']
        problems = category['problems']

        PROBLEMS_LIST_HTML += get_category_html(category_name)

        for problem in problems:
            problem_id = problem['id']
            problem_name = problem['name']

            PROBLEMS_LIST_HTML += get_problem_html(problem_id, problem_name)

    PROBLEMS_LIST_HTML += "</table>"
    PROBLEMS_LIST_HTML = PROBLEMS_LIST_HTML.replace('\n', '')


def get_category_html(category_name: str) -> str:
    return f"""
        <th>
            <td colspan="5">{category_name}</td>
        </th>
    """


def get_problem_html(problem_id: int, problem_name: str) -> str:
    return f"""
        <th>
            <td>{problem_id}</td>
            <td><a href="{PROBLEM_URL.format(problem_id)}">{problem_name}</a></td>
        </th>
    """
