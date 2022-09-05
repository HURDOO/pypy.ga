import json
from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import render, redirect

from problem.load import PROBLEMS_DIR
from .models import Submit, ResultType, SubmitType, getSubmitType
from runner import runner
from account import info
from urllib.parse import quote


def new(request):
    data = request.POST
    print(data)

    if 'user_id' not in request.session:
        return redirect('/problem/12345')
    user_id = request.session['user_id']

    problem_id, _type, code, submit_time = \
        data['problem_id'], getSubmitType(data['type']), \
        data['code'], data['submit_time']

    input_data = None
    if _type == SubmitType.TEST:
        input_data = data['input_type'][0]

    submit = Submit.create(
        _user_id=user_id,
        _problem_id=problem_id,
        _type=_type,
        _code=code,
        _submit_time=submit_time,
        _input_data=input_data
    )

    runner.handle_submit(submit.id, problem_id, code, _type, input_data)

    # return redirect('/submit?problem_id={}&user_id={}'.format(problem_id, user_id))
    return redirect('/submit/{}'.format(submit.id))


def detail(request, submit_id):
    submit = Submit.objects.get(id=submit_id)
    data = {
        'submit_id': submit.id,
        'problem_id': submit.problem_id,
        'user_id': submit.user_id,
        'submit_type': submit.type,
        'result': submit.result,
        'code': submit.code,
        'code_length': submit.code_length,
        'submit_time': str(submit.submit_time + timedelta(hours=9))
    }
    data.update(get_details(submit))
    data.update(info.get_data(request.session))
    return render(request, 'detail.html', context=data)


def get_details(submit: Submit) -> dict:
    if submit.type == SubmitType.GRADE:
        if submit.result == ResultType.ACCEPTED:
            return {
                'time_usage': submit.time_usage,
                'memory_usage': submit.memory_usage,
            }

        stdin, correct_stdout = std(submit.problem_id, submit.last_case_idx)

        if submit.result == ResultType.WRONG_ANSWER:
            return {
                'stdin': stdin,
                'correct_stdout': correct_stdout,
                'stdout': submit.stdout,
            }

        if submit.result in [ResultType.TIME_LIMIT, ResultType.MEMORY_LIMIT]:
            return {
                'stdin': stdin,
                'stdout': submit.stdout
            }

        if submit.result == ResultType.RUNTIME_ERROR:
            return {
                'stdin': stdin,
                'correct_stdout': correct_stdout,
                'stdout': submit.stdout,
                'stderr': submit.stderr
            }

    else:
        if submit.result == ResultType.COMPLETE:
            return {
                'stdin': submit.stdin,
                'stdout': submit.stdout,
                'time_usage': submit.time_usage,
                'memory_usage': submit.memory_usage,
            }

        if submit.result in [ResultType.TIME_LIMIT, ResultType.MEMORY_LIMIT]:
            return {
                'stdin': submit.stdin,
                'stdout': submit.stdout,
            }
        elif submit.result == ResultType.RUNTIME_ERROR:
            return {
                'stdin': submit.stdin,
                'stdout': submit.stdout,
                'stderr': submit.stderr
            }

    return {}


def std(problem_id: int, case_idx: int) -> tuple:

    with open(PROBLEMS_DIR / str(problem_id) / 'in' / '{}.in'.format(case_idx), encoding='UTF-8') as f:
        stdin = f.read()
    with open(PROBLEMS_DIR / str(problem_id) / 'out' / '{}.out'.format(case_idx), encoding='UTF-8') as f:
        correct_stdout = f.read()

    return stdin, correct_stdout


def index(request):
    return redirect('/')
