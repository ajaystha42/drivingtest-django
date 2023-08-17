"""
Author:
Ajay Shrestha
Gaurab Pokharel
Nirajan Karki
Sakar Thapa
"""
from django.urls import path
from Quiz import views
from django.urls import re_path

urlpatterns = [
    path('login', views.loginUser, name='login'),  # URL for the login view
    path('logoutUser', views.logoutUser, name='logout'),  # URL for the logout view
    path('register', views.register, name='register'),  # URL for the registration view
    path('', views.index, name='home'),  # URL for the index
    path('index', views.index, name='index'),  # URL for the index view
    path('quiz/', views.quiz, name='quiz'),  # URL for the quiz view
    path('result', views.result, name='result'),  # URL for the result view
    path('score/', views.score, name='score'),  # URL for the score view
    re_path(r'^.*/$', views.redirect_to_home),  # Redirect others URL's to the home page
]
