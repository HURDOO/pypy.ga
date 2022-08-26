import django.http
from django.shortcuts import redirect
from . import google
from .models import AccountModel


def login(request):
    return redirect(google.get_login_url())


def logout(request):
    del request.session['user_id']
    return redirect('/')


def auth(request):
    code = request.GET.get('code')
    email = google.get_email(code)
    account = AccountModel(email=email)
    request.session['user_id'] = account.id
    return redirect('/')
