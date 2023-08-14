from django.urls import path
from Quiz import views
from django.urls import re_path


urlpatterns = [
    path('', views.loginUser),
    path('login', views.loginUser),
    path('logoutUser', views.logoutUser),
    path('register', views.register, name='register'),
    path('index', views.index, name='index'),
    path('quiz/', views.quiz, name='quiz'),
    path('result', views.result, name='result'),
    path('score/', views.score, name='score'),
    re_path(r'^.*/$', views.redirect_to_home),
]
