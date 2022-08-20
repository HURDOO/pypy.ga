from django.shortcuts import render, redirect
from . import google


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.GET.get('code', False):
        print(request.GET.get('code'))
        return redirect('/')
    else:
        url = google.get_login_url()[0]
        print(url)
        return redirect(url)
