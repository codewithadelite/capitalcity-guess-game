from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('loginAdmin/', views.adminLogin, name='adminLogin'),
    path('loginGuest/', views.guestLogin, name='guestLogin'),
    path('accountGuest/', views.accountGuest, name='accountGuest'),
    path('logout/', views.userLogout, name='logout'),

    # ADMIN PANEL URLS

    path('adminPanel/', views.adminIndex, name='adminIndex'),
    path('adminPanel/players', views.viewPlayers, name='viewPlayers'),
    path('adminPanel/players/<str:pk>/status',
         views.statusPlayer, name='statusPlayer'),

    path('adminPanel/countries', views.viewCountries, name='viewCountries'),
    path('adminPanel/addCountry', views.addCountry, name='addCountry'),
    path('adminPanel/<str:pk>/editCountry',
         views.editCountry, name='editCountry'),
    path('adminPanel/<str:pk>/deleteCountry',
         views.deleteCountry, name='deleteCountry'),

    path('adminPanel/quiz', views.viewQuiz, name='viewQuiz'),
    path('adminPanel/quiz/<str:pk>/status',
         views.statusQuiz, name='statusQuiz'),
    path('adminPanel/addQuiz', views.addQuiz, name='addQuiz'),
    path('adminPanel/<str:pk>/editQuiz', views.editQuiz, name='editQuiz'),
    path('adminPanel/<str:pk>/deleteQuiz', views.deleteQuiz, name='deleteQuiz'),

    # PLAYER PANEL

    path('playerPanel/', views.playerIndex, name='playerIndex'),
    path('playerPanel/listQuiz', views.listQuiz, name='listQuiz'),
    path('playerPanel/<str:pk>/selectGuess',
         views.selectGuess, name='selectGuess'),
    path('playerPanel/<str:pk>/playCountry',
         views.playCountry, name='playCountry'),
    path('playerPanel/<str:pk>/playCity', views.playCity, name='playCity'),
    path('playerPanel/myMarks', views.myMarks, name='myMarks'),
    path('playerPanel/<str:pk>/markDetail',
         views.markDetail, name='markDetail'),


]
