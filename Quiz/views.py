import datetime
from datetime import datetime

from django.shortcuts import redirect, render
from Quiz.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import *
from Quiz.forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login


def test(request):
    return render(request, "test.html")

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
        context = {'categories': Category.objects.all(), 'user': user}
        if request.GET.get('category'):
            return redirect(f"/quiz?category={request.GET.get('category')}")
        return render(request, 'index.html', context)
    except KeyError:
        return redirect('/')
        # return login(request)


def quiz(request):
    try:
        user = request.COOKIES['user']
        questions = get_quiz(request)
        return render(request, 'quiz.html', {'questions': questions, 'user': user})
    except KeyError:
        return redirect('/')


def get_quiz(request):
    try:
        user = request.COOKIES['user']
        question_objs = (Question.objects.all())
        category_name = request.GET.get('category')
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

        return random.sample(data, 5)
    # except KeyError:
    #     print('no data here')
    #     return redirect('/login')
    except Exception as e:
        print(e)
    return HttpResponse("Something went wrong")


def all_quiz_results_view(request):
    try:
        user = request.COOKIES['user']
        print(user)
        # return redirect('/index')
        quiz_results = QuizResult.objects.filter(user__username__icontains=user)
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

        context = {'user': user, 'quiz_results': quiz_results, 'highest': highest, 'lowest': lowest,
                   'average': round(float(average), 2)}
        return render(request, 'all_quiz_results_template.html', context)
        # return render(request, 'index.html')
    except KeyError:
        return redirect('/')


def result(request):
    try:
        user = request.COOKIES['user']
        if request.method == 'POST':
            # print(request.POST)
            # input_label_value = request.POST.get('input_label')
            # print("category_name ::::::::",input_label_value)
            user_answers = request.POST.dict()
            user_score = 0

            for question_id, selected_choice_id in user_answers.items():
                if question_id.startswith('question'):
                    try:
                        question = Question.objects.get(
                            pk=int(question_id[8:]))
                        try:
                            category_identifier = question.category.category_name
                            category_instance = Category.objects.get(category_name=category_identifier)
                            user12 = User.objects.get(username=request.COOKIES['user'])
                        except (Category.DoesNotExist or User.DoesNotExist):
                            print("category or user doesnot exist")
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
            quiz_result = QuizResult(user=user12, score=user_score, category=category_instance)
            quiz_result.save()
            percentage = user_score / 5 * 100
            return render(request, 'quiz_result.html',
                          {'user_score': user_score, 'current_datetime': current_date, 'user': user,
                           'percentage': percentage,'category_name':category_instance.category_name})
    except KeyError:
        redirect('/')
    return redirect('quiz')
