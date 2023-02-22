import json

import requests
from django.shortcuts import redirect, render

from . import google, models, info
from .models import Account
from pypyga.settings import conf

ADMIN_USER_ID = conf['admin_id']


def login(request):
    data = {}
    if request.POST:
        print(request.POST)
        student_id = request.POST['student_id']
        student_pw = request.POST['student_pw']

        res = requests.request('POST', 'https://jamsin.tk/account/api/',
                               data=json.dumps({
                                   'id': student_id,
                                   'pw': student_pw,
                               })).text
        print(res)
        res = json.loads(res)
        if 'number' in res:
            account = models.handle_login(res['number'])
            request.session[info.USER_ID_KEY] = account.id
            return redirect('/')
        else:
            data['error'] = '사용자를 찾을 수 없어요.'

    return render(request, 'login.html', context=data)


def logout(request):
    del request.session[info.USER_ID_KEY]
    return redirect('/')


# def auth(request):
#     code = request.GET.get('code')
#     email = google.get_email(code)
#     try:
#         account = models.handle_login(email)
#         request.session[info.USER_ID_KEY] = account.id
#         return redirect('/')
#     except AttributeError:
#         # not school account
#         return redirect('/account/login')


def ranking(request):
    accounts = Account.objects.order_by('-score', 'last_submit').exclude(id=ADMIN_USER_ID)
    if len(accounts) < 4:
        data = {
            'accounts': accounts
        }
    else:
        data = {
            'first': accounts[0],
            'second': accounts[1],
            'third': accounts[2],
            'accounts': accounts[3:]
        }
    data.update(info.get_data(request.session))
    return render(request, 'account.html', data)
