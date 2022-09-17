from django.shortcuts import redirect, render
from .info import USER_ID_KEY

from . import google
from . import models


def login(request):
    return render(request, 'login.html', context={
        'login_url': google.get_login_url()
    })


def logout(request):
    del request.session[USER_ID_KEY]
    return redirect('/')


def auth(request):
    code = request.GET.get('code')
    email = google.get_email(code)
    try:
        account = models.handle_login(email)
        request.session[USER_ID_KEY] = account.id
        return redirect('/')
    except AttributeError:
        # not school account
        return redirect(USER_ID_KEY)

