from django.shortcuts import redirect, render
from Quiz.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse


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


def logout(request):
    print('inside logouttasdasdadasdasdnasdjkansdjkasndjkasndjasndjasndjkasndkjasndkj')
    pass


def index(request):
    return render(request, 'index.html')
