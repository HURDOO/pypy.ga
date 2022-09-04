from django.shortcuts import redirect, render

from . import google
from . import models


def login(request):
    return render(request, 'login.html', context={
        'login_url': google.get_login_url()
    })


def logout(request):
    del request.session['user_id']
    return redirect('/')


def auth(request):
    code = request.GET.get('code')
    email = google.get_email(code)
    try:
        account = models.handle_login(email)
        request.session['user_id'] = account.id
        return redirect('/')
    except AttributeError:
        # not school account
        return redirect('/account/login')

