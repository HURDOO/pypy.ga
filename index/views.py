from django.shortcuts import render
from account import info
from problem import load
from account.models import Account
from copy import deepcopy


def index(request):
    categories = deepcopy(load.PROBLEMS_LIST)

    user_id = info.get_user_id(request.session)
    if user_id is not None:
        submits = Account.objects.get(id=user_id).submits
        for category in categories:
            for problem in category['problems']:
                if str(problem['id']) in submits:
                    problem['score'] = submits[str(problem['id'])]['score']

    data = {'list': categories}
    data.update(info.get_data(request.session))

    if user_id is not None:
        data['manito'] = (user_id // 100 == 103)

    return render(request, 'index.html', data)
