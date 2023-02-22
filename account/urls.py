from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    # path('auth/', views.auth),
    path('', views.ranking)
]
