from django.contrib import admin
from django.urls import path
from Quiz import views

urlpatterns = [
    path('', views.login),
    path('register', views.register, name='register'),
    path('addUser', views.addUser, name='addUser'),
    path('loginUser', views.loginUser, name='loginUser'),
    path('index', views.index, name='index'),
]
