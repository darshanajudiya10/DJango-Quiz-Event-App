import json

from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from .models import Answer, Event, Quiz, UserAnswer, UserSubmission


def home(request):
    latest_quizzes = Quiz.objects.order_by('-created_at')[:3]
    upcoming_events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')[:3]
    return render(
        request,
        'quizzes/home.html',
        {
            'latest_quizzes': latest_quizzes,
            'upcoming_events': upcoming_events,
        },
    )

def user_profile(request):
    return render(request, 'quizzes/user_profile.html')

def quiz_list(request):
    quizzes = Quiz.objects.order_by('-created_at')
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})


def quiz_attempt(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    return render(request, 'quizzes/quiz_attempt.html', {'quiz': quiz})


@require_GET
def quiz_data(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.prefetch_related('answers').all()
    data = {
        'id': quiz.id,
        'title': quiz.title,
        'description': quiz.description,
        'questions': [
            {
                'id': question.id,
                'text': question.text,
                'question_type': question.question_type,
                'answers': [
                    {'id': answer.id, 'text': answer.text} for answer in question.answers.all()
                ],
            }
            for question in questions
        ],
    }
    return JsonResponse(data)


@require_POST
@transaction.atomic
def submit_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    try:
        payload = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    user_name = (payload.get('user_name') or '').strip()
    answers_map = payload.get('answers') or {}

    if not user_name:
        return JsonResponse({'error': 'Name is required.'}, status=400)

    questions = list(quiz.questions.prefetch_related('answers'))
    submission = UserSubmission.objects.create(quiz=quiz, user_name=user_name, score=0)

    correct_count = 0
    user_answers = []

    for question in questions:
        answer_id = answers_map.get(str(question.id)) or answers_map.get(question.id)
        if not answer_id:
            continue

        answer = next((a for a in question.answers.all() if a.id == int(answer_id)), None)
        if answer is None:
            continue

        is_correct = answer.is_correct
        if is_correct:
            correct_count += 1

        user_answers.append(
            UserAnswer(
                submission=submission,
                question=question,
                answer=answer,
                is_correct=is_correct,
            )
        )

    if user_answers:
        UserAnswer.objects.bulk_create(user_answers)

    submission.score = correct_count
    submission.save(update_fields=['score'])

    return JsonResponse(
        {
            'redirect_url': reverse('quizzes:quiz_result', args=[submission.id]),
            'score': correct_count,
        }
    )


def quiz_result(request, submission_id):
    submission = get_object_or_404(
        UserSubmission.objects.select_related('quiz').prefetch_related(
            'answers__question', 'answers__answer'
        ),
        pk=submission_id,
    )
    total_questions = submission.quiz.questions.count()
    return render(
        request,
        'quizzes/quiz_result.html',
        {
            'submission': submission,
            'total_questions': total_questions,
        },
    )


def event_list(request):
    events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')
    return render(request, 'quizzes/events.html', {'events': events})


def quiz_history(request):
    submissions = UserSubmission.objects.select_related('quiz').order_by('-submitted_at')
    return render(request, 'quizzes/quiz_history.html', {'submissions': submissions})
