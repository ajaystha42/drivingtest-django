from django.urls import path
from Quiz import views
from django.urls import re_path


urlpatterns = [
    path('login', views.loginUser, name='login'),
    path('logoutUser', views.logoutUser, name='logout'),
    path('register', views.register, name='register'),
    path('', views.index, name='home'),
    path('index', views.index, name='index'),
    path('quiz/', views.quiz, name='quiz'),
    path('result', views.result, name='result'),
    path('score/', views.score, name='score'),
    re_path(r'^.*/$', views.redirect_to_home),
]
