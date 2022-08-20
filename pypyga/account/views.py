import django.http
from django.shortcuts import redirect
from . import google
from account.models import AccountModel


def index(request):
    code = request.GET.get('code', False)
    if code:
        code = request.GET.get('code')
        email = google.get_email(code)
        account = AccountModel(email=email)
        request.session['user'] = account.id
        return redirect('/')
    else:
        return redirect(google.get_login_url())
