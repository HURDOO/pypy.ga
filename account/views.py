import django.http
import re
from django.shortcuts import redirect
from . import google
from . import models


def login(request):
    return redirect(google.get_login_url())


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
        return redirect('/problem/12345')

