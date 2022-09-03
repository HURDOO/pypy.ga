from django.shortcuts import render, redirect
from .models import Submit, SubmitType, getSubmitType
from runner import runner


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
    return render(request, 'detail.html', context={
        'submit_id': submit.id,
        'problem_id': submit.problem_id,
        'user_id': submit.user_id,
        'submit_type': submit.type,
        'result': submit.result,
        'memory_usage': submit.memory_usage,
        'time_usage': submit.time_usage,
        'submit_time': submit.submit_time,
        'code': submit.code,
        'code_length': submit.code_length,
        'stdin': submit.stdin,
        'stdout': submit.stdout,
        'stderr': submit.stderr
    })


def index(request):
    return redirect('/')
