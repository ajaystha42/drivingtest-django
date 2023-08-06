from django.shortcuts import redirect, render
from Quiz.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import *
from Quiz.forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login


def login(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                print(username)
                print(password)
                user = authenticate(
                    request, username=username, password=password)
                print('inside loginnnnnnnnnnnnnnn    ', user)

                if user:
                    response = HttpResponseRedirect(reverse('index'))
                    response.set_cookie('user', user.username)
                    return response

                # Authentication - Setting Userinfo to cookie
                # remove this
                user = User.objects.get(
                    username=username, password=password)
                response = HttpResponseRedirect(reverse('index'))
                response.set_cookie('user', user.username)
                return response
            else:
                return render(request, 'login.html', {
                    'error': "form is invalid!",
                    'form': form})
        except User.DoesNotExist:
            return render(request, 'login.html', {
                'error': "Invalid Credentials. Try again!",
                'form': form
            })

    else:
        try:
            user = request.COOKIES['user']
            return render(request, 'index.html')
        except KeyError:
            return render(request, 'login.html', {'form': form})


def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                user_info = User.objects.filter(username=username)
                if not user_info.exists():
                    form.save()
                    return redirect('/')

                return render(request, 'register.html', {
                    'error': "User already exists. Please choose other username.",
                    'form': form
                })
            except:
                pass

    return render(request, 'register.html', {'form': form})


def index(request):
    try:
        user = request.COOKIES['user']
        context = {'categories': Category.objects.all()}
        if request.GET.get('category'):
            return redirect(f"/quiz?category={request.GET.get('category')}")
        return render(request, 'index.html', context)
    except KeyError:
        # redirect('/')
        return login(request)


def quiz(request):
    questions = get_quiz(request)
    return render(request, 'quiz.html', {'questions': questions})


def get_quiz(request):
    try:
        question_objs = (Question.objects.all())

        if request.GET.get('category'):
            question_objs = question_objs.filter(
                category__category_name__icontains=request.GET.get('category'))

        question_objs = list(question_objs)

        data = []
        random.shuffle(question_objs)
        for question_obj in question_objs:
            data.append({
                "id": question_obj.id,
                "category": question_obj.category.category_name,
                "question": question_obj.question,
                "marks": question_obj.marks,
                "answers": question_obj.get_answer()
            })

        return random.sample(data, 3)

    except Exception as e:
        print(e)
    return HttpResponse("Something went wrong")
