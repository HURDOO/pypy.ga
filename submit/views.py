from django.shortcuts import render, redirect


def index(request):
    if request.POST:
        print(request.POST)
    else:
        print('Get request')
    return redirect('/problem/10003')
