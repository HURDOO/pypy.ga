from django.shortcuts import render
from account.info import get_data

def index(request, problem):
    data = {'problem_url': f'https://raw.githubusercontent.com/HURDOO/python-trainer/master/problems/{problem}.md'}
    data.update(get_data(request.session))

    return render(request, 'problem/problem.html', data)

# https://raw.githubusercontent.com/HURDOO/python-trainer/master/problems/12345.md
