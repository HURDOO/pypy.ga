from django.urls import path, include
from . import views

app_name = 'problem'
urlpatterns = [
    path('', views.main)
]
