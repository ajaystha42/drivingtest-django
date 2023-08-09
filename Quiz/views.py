import datetime
from datetime import datetime

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
            return redirect('/index')
            # return render(request, 'index.html')
        except KeyError:
            return render(request, 'login.html', {'form': form, 'user': None})


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

    return render(request, 'register.html', {'form': form, 'user': None})


def index(request):
    try:
        user = request.COOKIES['user']
        context = {'categories': Category.objects.all()}
        if request.GET.get('category'):
            return redirect(f"/quiz?category={request.GET.get('category')}")
        return render(request, 'index.html', context)
    except KeyError:
        return redirect('/')
        # return login(request)


def quiz(request):
    questions = get_quiz(request)
    return render(request, 'quiz.html', {'questions': questions})


def get_quiz(request):
    try:
        user = request.COOKIES['user']
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
    except KeyError:
        print('no data here')
        return redirect('/login')
    # except Exception as e:
    #     print(e)
    # return HttpResponse("Something went wrong")


def all_quiz_results_view(request):
    try:
        user = request.COOKIES['user']
        # return redirect('/index')
        quiz_results = QuizResult.objects.all()  # Get all quiz results
        context = {'user': user, 'quiz_results': quiz_results}
        return render(request, 'all_quiz_results_template.html', context)
        # return render(request, 'index.html')
    except KeyError:
        return redirect('/')


def result(request):
    if request.method == 'POST':
        user_answers = request.POST.dict()
        print('request jere  ', user_answers)
        user_score = 0

        for question_id, selected_choice_id in user_answers.items():
            if question_id.startswith('question'):
                try:
                    question = Question.objects.get(pk=int(question_id[8:]))
                    print('question', question)
                    selected_choice = Answer.objects.get(
                        pk=int(selected_choice_id))
                    print("Selected choice ID:", selected_choice_id)
                    print("Selected choice:", selected_choice)
                    if selected_choice.is_correct:
                        user_score += 1
                        print("User score:", user_score)
                except Answer.DoesNotExist:
                    print(
                        f"Answer matching query does not exist for question ID {question_id[8:]}")
        current_date = datetime.now()
        try:
            user12 = User.objects.get(username=request.COOKIES['user'])
        except User.DoesNotExist:
            return redirect('/')
            # return login(request)
        else:
            # Create a new quiz result
            quiz_result = QuizResult(user=user12, score=user_score)
            quiz_result.save()

        return render(request, 'quiz_result.html', {'user_score': user_score, 'current_datetime': current_date})

    return redirect('quiz')

    # right_answers = 0
    # question_ids = request.POST["questionids"].split(',')
    # print(question_ids)
    # for question_id in question_ids:
    #     question = Question.objects.get(pk=question_id)
    #     user_answer = request.POST['question' + str(question.id)]
    #     correct_choices = question.choice_set.filter(
    #         pk=user_answer, is_correct=True)
    #     if len(correct_choices) > 0:
    #         right_answers += 1
    #         for choice in correct_choices:
    #             print('Question %s - User choice %s => Correct choice %s' %
    #                   (question.id, user_answer, str(choice)))
    #     else:
    #         print("Question => " + question.question_text +
    #               " Answer => " + user_answer)
    # user = User.objects.get(pk=user_id)
    # result = user.quizresults_set.create(
    #     right_answers=right_answers, quiz_played_on=timezone.now())
    # return HttpResponseRedirect(reverse('Quiz:quiz_result', args=(user_id, result.id)))
