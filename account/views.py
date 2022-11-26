from django.shortcuts import redirect, render

from . import google, models, info
from .models import Account
from pypyga.settings import conf

ADMIN_USER_ID = conf['admin_id']


def login(request):
    if request.POST:
        student_id = request.POST['student_id']
        return redirect(google.get_student_login_url(student_id))

    data = {
        'login_url': google.get_login_url()
    }

    user_agent = request.META['HTTP_USER_AGENT'].lower()
    if 'kakaotalk' in user_agent:
        if 'iphone' in user_agent:
            data['kakaotalk'] = 'iphone'
        else:
            data['kakaotalk'] = 'android'
    else:
        data['kakaotalk'] = 'none'

    return render(request, 'login.html', context=data)


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
    accounts = Account.objects.order_by('-score', 'id').exclude(id=ADMIN_USER_ID)
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
