from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import CountryForm, QuizForm, UserCreateForm

from random import randrange


from .models import User, Guest, Quiz, Country, Answer, QuizDone


def index(request):
    context = {}
    return render(request, 'Game/index.html', context)


def adminLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('../adminPanel/')
        else:
            messages.error(request, "Username Or Password Incorrect")
    context = {}
    return render(request, 'Game/loginAdmin.html', context)


def guestLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('playerIndex'))
        else:
            messages.error(request, "Username Or Password Incorrect")
    context = {}
    return render(request, 'Game/loginGuest.html', context)


def userLogout(request):
    logout(request)
    return redirect('/')


def accountGuest(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password1'])
            if user is not None:
                login(request, user)
                return redirect(reverse('playerIndex'))
        else:
            messages.error(
                "Please try to change username and make password that contains atleast 8 characters and numbers")
    else:
        form = UserCreateForm()
    context = {"form": form}
    return render(request, 'Game/accountGuest.html', context)

# ADMIN PANEL VIEWS SECTION


@login_required(login_url='adminLogin')
def adminIndex(request):
    total_players = User.objects.filter(is_guest=True).count()
    total_country = Country.objects.all().count()
    total_quiz = Quiz.objects.all().count()
    context = {
        'total_players': total_players,
        'total_country': total_country,
        'total_quiz': total_quiz}
    return render(request, 'Game/admin/index.html', context)


@login_required(login_url='adminLogin')
def viewPlayers(request):
    players = Guest.objects.all().order_by('-id')

    context = {'players': players}
    return render(request, 'Game/admin/viewPlayers.html', context)


@login_required(login_url='adminLogin')
def statusPlayer(request, pk):
    player = get_object_or_404(Guest, id=pk)

    if player.is_activated == True:
        player.is_activated = False
        player.save()
        messages.success(request, 'Player Deactivated successfully')
        return redirect(reverse('viewPlayers'))
    else:
        player.is_activated = True
        player.save()
        messages.success(request, 'Player Activated successfully')
        return redirect(reverse('viewPlayers'))


@login_required(login_url='adminLogin')
def viewCountries(request):
    countries = Country.objects.all().order_by('-id')

    context = {'countries': countries}
    return render(request, 'Game/admin/viewCountries.html', context)


@login_required(login_url='adminLogin')
def addCountry(request):
    form = CountryForm()
    if request.method == "POST":
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Country & City added successfully')
            form = CountryForm()
        else:
            messages.error(request, 'Invalid try again with new datas')
    context = {'form': form}
    return render(request, 'Game/admin/addCountry.html', context)


@login_required(login_url='adminLogin')
def editCountry(request, pk):
    country = get_object_or_404(Country, id=pk)
    form = CountryForm(instance=country)
    print(form)
    if request.method == "POST":
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            messages.success(request, 'Country & City updated successfully')
        else:
            messages.error(request, 'Invalid try again with new datas')
    context = {'form': form}
    return render(request, 'Game/admin/editCountry.html', context)


@login_required(login_url='adminLogin')
def deleteCountry(request, pk):
    country = get_object_or_404(Country, id=pk)
    delete = country.delete()
    return redirect(reverse('viewCountries'))


@login_required(login_url='adminLogin')
def viewQuiz(request):
    quizes = Quiz.objects.all().order_by('-id')

    context = {'quizes': quizes}
    return render(request, 'Game/admin/viewquiz.html', context)


@login_required(login_url='adminLogin')
def statusQuiz(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)

    if quiz.is_activated == True:
        quiz.is_activated = False
        quiz.save()
        #messages.success(request, 'Quiz Deactivated successfully')
        return redirect(reverse('viewQuiz'))
    else:
        quiz.is_activated = True
        quiz.save()
        #messages.success(request, 'Quiz Activated successfully')
        return redirect(reverse('viewQuiz'))


@login_required(login_url='adminLogin')
def deleteQuiz(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)
    delete = quiz.delete()
    return redirect(reverse('viewQuiz'))


@login_required(login_url='adminLogin')
def addQuiz(request):
    form = QuizForm()
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz added successfully')
            form = QuizForm()
        else:
            messages.error(request, 'Invalid try again with new datas')
    context = {'form': form}
    return render(request, 'Game/admin/addQuiz.html', context)


@login_required(login_url='adminLogin')
def editQuiz(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)
    form = QuizForm(instance=quiz)
    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz updated successfully')
        else:
            messages.error(request, 'Invalid try again with new datas')
    context = {'form': form}
    return render(request, 'Game/admin/editQuiz.html', context)

# THIS IS THE BEGINNING OF PLAYER SECTION

# ADMIN PANEL VIEWS SECTION


@login_required(login_url='adminLogin')
def playerIndex(request):
    total_quiz = Quiz.objects.all().count()
    total_quiz_active = Quiz.objects.filter(is_activated=True).count()
    total_quiz_done = QuizDone.objects.filter(user=request.user.id).count()
    chart = request.user.answer_set.all()
    context = {
        'total_quiz': total_quiz,
        'total_quiz_active': total_quiz_active,
        'total_quiz_done': total_quiz_done,
        'charts': chart
    }
    return render(request, 'Game/guest/playerIndex.html', context)


@login_required(login_url='guestLogin')
def listQuiz(request):
    quizes = Quiz.objects.all()
    myquiz = request.user.quizdone_set.all()
    myquiz_count = myquiz.count()
    quiz_done = []
    if myquiz_count >= 1:
        for quiz in myquiz:
            quiz_done.append(quiz.quiz.id)
    print(quiz_done)
    context = {'quizes': quizes, 'quiz_done': quiz_done}
    return render(request, 'Game/guest/listQuiz.html', context)


@login_required(login_url='guestLogin')
def selectGuess(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)
    quiz_name = quiz.name
    quiz_id = quiz.id
    context = {'quiz_name': quiz_name, 'quiz_id': quiz_id}
    return render(request, 'Game/guest/selectGuess.html', context)


@login_required(login_url='guestLogin')
def myMarks(request):
    quizes = request.user.answer_set.all()
    query = False
    if len(quizes) >= 1:
        query = True
    context = {'quizes': quizes, 'query': query}
    return render(request, 'Game/guest/myMarks.html', context)


@login_required(login_url='guestLogin')
def markDetail(request, pk):
    user = request.user.id
    quiz_id = pk

    answer = get_object_or_404(Answer, quiz=quiz_id, user=user)
    context = {'answer': answer}
    return render(request, 'Game/guest/markDetail.html', context)


@login_required(login_url='guestLogin')
def playCountry(request, pk):
    user = request.user.id
    quiz_id = pk

    user_obj = request.user
    quiz_obj = get_object_or_404(Quiz, id=quiz_id)

    # UPDAE THAT QUIZ IS DONETE IN DATABASE

    obj, create = QuizDone.objects.get_or_create(quiz=quiz_obj, user=user_obj)

    if request.method == "POST":
        name = request.POST['country']
        country = request.POST['question_id']
        is_country = True
        is_true = False

        question_data = get_object_or_404(Country, id=country)
        question_country = question_data.country_name.upper()

        if name.upper() == question_country:
            is_true = True
        quiz_instance = get_object_or_404(Quiz, id=quiz_id)
        country_instance = get_object_or_404(Country, id=country)
        user_instance = get_object_or_404(User, id=user)
        answer = Answer.objects.create(name=name, is_country=is_country, is_true=is_true,
                                       quiz=quiz_instance, country=country_instance, user=user_instance)

        return redirect(reverse('markDetail', args=(quiz_id,)))
    else:
        question = Country.objects.all()
        length = len(question)
        random_question = randrange(0, length)

        question_id = question[random_question].id
        city_name = question[random_question].city_name
        context = {'question_id': question_id, 'city_name': city_name}
        return render(request, 'Game/guest/playCountry.html', context)


@login_required(login_url='guestLogin')
def playCity(request, pk):
    user = request.user.id
    quiz_id = pk

    user_obj = request.user
    quiz_obj = get_object_or_404(Quiz, id=quiz_id)

    # UPDAE THAT QUIZ IS DONETE IN DATABASE

    obj, create = QuizDone.objects.get_or_create(quiz=quiz_obj, user=user_obj)

    if request.method == "POST":
        name = request.POST['city']
        country = request.POST['question_id']
        is_country = False
        is_true = False

        question_data = get_object_or_404(Country, id=country)
        question_city = question_data.city_name.upper()

        if name.upper() == question_city:
            is_true = True
        quiz_instance = get_object_or_404(Quiz, id=quiz_id)
        country_instance = get_object_or_404(Country, id=country)
        user_instance = get_object_or_404(User, id=user)
        answer = Answer.objects.create(name=name, is_country=is_country, is_true=is_true,
                                       quiz=quiz_instance, country=country_instance, user=user_instance)

        return redirect(reverse('markDetail', args=(quiz_id,)))
    else:
        question = Country.objects.all()
        length = len(question)
        random_question = randrange(0, length)

        question_id = question[random_question].id
        country_name = question[random_question].country_name
        context = {'question_id': question_id, 'country_name': country_name}
        return render(request, 'Game/guest/playCity.html', context)
