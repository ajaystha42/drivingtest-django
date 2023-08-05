from django.shortcuts import redirect, render
from Quiz.models import User
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from .models import *


def login(request):
    try:
        user = request.COOKIES['user']
        return render(request, 'index.html')
    except KeyError:
        return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def addUser(request):
    user_id = request.POST['user_id']
    name = request.POST['name']
    password = request.POST['password']
    user_info = User.objects.filter(user_id=user_id)
    if not user_info.exists():
        User.objects.create(
            user_id=user_id,
            name=name,
            password=password)
        return redirect('/')

    return render(request, 'register.html', {
        'error': "User already exists. Please choose other username.",
    })


def loginUser(request):
    try:
        user = User.objects.get(
            user_id=request.POST['user_id'], password=request.POST['password'])

        # Authentication - Setting Userinfo to cookie

        response = HttpResponseRedirect(reverse('index'))
        response.set_cookie('user', user.user_id)
        return response
    except (KeyError, User.DoesNotExist):
        return render(request, 'login.html', {
            'error': "Invalid Credentials. Try again!",
        })


def index(request):
    try:
        user = request.COOKIES['user']
        context = {'categories': Category.objects.all()}
        if request.GET.get('category'):
            return redirect(f"/quiz?category={request.GET.get('category')}")
        return render(request, 'index.html', context)
    except KeyError:
        return render(request, 'login.html')

def quiz(request):
    questions = get_quiz(request)

    return render(request, 'quiz.html', {'questions': questions})


def get_quiz(request):
    try:
        question_objs = (Question.objects.all())

        if request.GET.get('category'):
            question_objs = question_objs.filter(category__category_name__icontains=request.GET.get('category'))

        question_objs = list(question_objs)
        data = []
        random.shuffle(question_objs)
        for question_obj in question_objs:
            data.append({
                "category": question_obj.category.category_name,
                "question": question_obj.question,
                "marks": question_obj.marks,
                "answers": question_obj.get_answer()
            })
        payload = {
            'status': True,
            'data': data
        }

        return JsonResponse(payload)

    except Exception as e:
        print(e)
    return HttpResponse("Something went wrong")
