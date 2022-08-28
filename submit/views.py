from django.shortcuts import render, redirect


def index(request):
    if request.POST:
        print(request.POST)
    return redirect('/')
