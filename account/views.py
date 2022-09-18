from django.shortcuts import redirect, render

from . import google, models, info
from .models import Account


def login(request):
    return render(request, 'login.html', context={
        'login_url': google.get_login_url()
    })


def logout(request):
    del request.session[info.USER_ID_KEY]
    return redirect('/')


def auth(request):
    code = request.GET.get('code')
    email = google.get_email(code)
    try:
        account = models.handle_login(email)
        request.session[info.USER_ID_KEY] = account.id
        return redirect('/')
    except AttributeError:
        # not school account
        return redirect('/account/login')


def ranking(request):
    accounts = Account.objects.order_by('-score')
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
