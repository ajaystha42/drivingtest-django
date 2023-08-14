import datetime
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from .models import *
from django.urls import reverse
from Quiz.forms import UserRegistrationForm, UserLoginForm


def loginUser(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # next_url = request.POST.get('next')
                # print('NEXT URL    ', next_url)
                # if next_url:
                #     return HttpResponseRedirect(next_url)
                # else:
                response = HttpResponseRedirect(reverse('index'))
                return response
            messages.error(request, 'Check your Credentials again')
            return render(request, 'login.html', {
                'form': form,
                'user': None
            })
        else:
            print(form.error_class.as_data())
            messages.error(request, 'Error Occured. Please try again.')
            return render(request, 'login.html', {
                'form': form
            })

    form = UserLoginForm()
    if request.user.is_authenticated:
        return redirect('/index')
    return render(request, 'login.html', {'form': form, 'user': None})


def logoutUser(request):
    logout(request)
    return redirect('/login')


def register(request):
    form = UserRegistrationForm()
    if request.user.is_authenticated:
        return redirect('/index')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(email=email).exists():
                messages.error(
                    request, 'Email already exists. Please choose unique email.')

                return render(request, 'register.html', {
                    'form': form,
                    'user': None
                })
            new_user = User.objects.create_user(
                username=username, email=email, password=password)
            new_user.save()
            # Directly login after successful register
            login(request, new_user)
            return redirect("/")
        else:
            # print(form.errors.as_data())
            # existing_username = form.data['username']
            # if User.objects.filter(username=existing_username).exists():
            #     messages.error(
            #         request, 'Username already exists. Please choose another username')
            # else:
            #     invalid_password = form.errors.as_data()['password']
            #     if invalid_password:
            #         messages.error(
            #             request, 'Password must be at least 8 characters long and contain letters, symbols and numbers.')
            #     else:
            messages.error(
                request, 'Error Occured. Please try again.')
    return render(request, 'register.html', {'form': form})


@login_required(login_url="/login")
def index(request):

    context = {'categories': Category.objects.all(),
               'user': request.user.username}
    if request.GET.get('category'):
        return redirect(f"/quiz?category={request.GET.get('category')}")
    return render(request, 'index.html', context)


@login_required(login_url="/login")
def quiz(request):
    questions = get_quiz(request)
    return render(request, 'quiz.html', {'questions': questions, 'user': request.user.username})


@login_required(login_url="/login")
def get_quiz(request):
    question_objs = (Question.objects.all())
    try:
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
        if len(question_objs) >= 5:
            return random.sample(data, 5)
        else:
            return random.sample(data, len(question_objs))
    except ValueError:
        return render(request, 'quiz.html')


@login_required(login_url="/login")
def all_quiz_results_view(request):
    try:
        quiz_results = QuizResult.objects.filter(
            user__username__icontains=request.user)
        highest = lowest = total_score = count = 0
        for quiz_result in quiz_results:
            score = quiz_result.score
            if highest < score:
                highest = score
            if lowest > score:
                lowest = score
            total_score += score
            count += 1
        average = total_score / count

        context = {'user': request.user.username, 'quiz_results': quiz_results, 'highest': highest, 'lowest': lowest,
                   'average': round(float(average), 2)}
        return render(request, 'all_quiz_results_template.html', context)
    except ZeroDivisionError:
        print('division zero exception  ')
        return render(request, 'all_quiz_results_template.html')


@login_required(login_url="/login")
def result(request):
    if request.method == 'POST':
        user_answers = request.POST.dict()
        user_score = 0

        for question_id, selected_choice_id in user_answers.items():
            if question_id.startswith('question'):
                try:
                    question = Question.objects.get(
                        pk=int(question_id[8:]))
                    try:
                        category_identifier = question.category.category_name
                        category_instance = Category.objects.get(
                            category_name=category_identifier)
                        user12 = User.objects.get(
                            username=request.user)
                    except (Category.DoesNotExist or User.DoesNotExist):
                        return redirect('/')

                    selected_choice = Answer.objects.get(
                        pk=int(selected_choice_id))
                    if selected_choice.is_correct:
                        user_score += 1
                except Answer.DoesNotExist:
                    print(
                        f"Answer matching query does not exist for question ID {question_id[8:]}")
        current_date = datetime.now()
        # Create a new quiz result
        quiz_result = QuizResult(
            user=user12, score=user_score, category=category_instance)
        quiz_result.save()
        percentage = user_score / 5 * 100
        return render(request, 'quiz_result.html',
                      {'user_score': user_score, 'current_datetime': current_date, 'user': request.user.username,
                       'percentage': percentage, 'category_name': category_instance.category_name})
    return redirect('quiz')
