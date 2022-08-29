from django.urls import path
from . import views

app_name = 'submit'
urlpatterns = [
    path('new', views.new),
    path('', views.index)
]
