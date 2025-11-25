from django.urls import path

from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.home, name='home'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:pk>/', views.quiz_attempt, name='quiz_attempt'),
    path('quizzes/<int:pk>/data/', views.quiz_data, name='quiz_data'),
    path('quizzes/<int:pk>/submit/', views.submit_quiz, name='submit_quiz'),
    path('results/<int:submission_id>/', views.quiz_result, name='quiz_result'),
    path('events/', views.event_list, name='event_list'),
    path('history/', views.quiz_history, name='quiz_history'),
    path('profile/', views.user_profile, name='user_profile'),
]

