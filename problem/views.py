from django.shortcuts import render, redirect
from account import info
from . import load


def index(request, problem):
    data = {
        'problem_id': problem,
        'problem_url': f'https://raw.githubusercontent.com/HURDOO/python-trainer/master/.problems/{problem}.md'
    }
    data.update(info.get_data(request.session))

    return render(request, 'problem.html', data)


def reload(request):
    load.load_problems()
    return redirect('/')
