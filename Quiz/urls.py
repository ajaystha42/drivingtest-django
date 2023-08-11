from django.contrib import admin
from django.urls import path
from Quiz import views

# from .views import CustomLoginView

urlpatterns = [
    path('', views.loginUser),
    path('login', views.loginUser),
    path('logoutUser', views.logoutUser),
    path('register', views.register, name='register'),
    path('index', views.index, name='index'),
    path('api/get-quiz', views.get_quiz, name="get_quiz"),
    path('quiz/', views.quiz, name='quiz'),
    path('result', views.result, name='result'),
    path('all-quiz-results/', views.all_quiz_results_view, name='all-quiz-results'),
]
