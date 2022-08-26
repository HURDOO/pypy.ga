from django.shortcuts import render
from account.info import get_data


def index(request):
    return render(request, 'index.html', get_data(request.session))
