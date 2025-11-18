from django.db import models

#model for Quiz
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

#model for Question
class Question(models.Model):
    MULTIPLE_CHOICE = 'multiple_choice'
    SINGLE_CHOICE = 'single_choice'
    TEXT = 'text'

    QUESTION_TYPE_CHOICES = [
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (SINGLE_CHOICE, 'Single Choice'),
        (TEXT, 'Text'),
    ]

    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=32, choices=QUESTION_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quiz.title}: {self.text[:50]}'

#model for Answer
class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.question.text[:30]} - {self.text[:30]}'

#model for UserSubmission
class UserSubmission(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='submissions', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=150)
    score = models.PositiveIntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_name} - {self.quiz.title}'

#model for UserAnswer
class UserAnswer(models.Model):
    submission = models.ForeignKey(
        UserSubmission, related_name='answers', on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, related_name='user_answers', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='user_answers', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['submission', 'question'],
                name='unique_submission_question',
            )
        ]

    def __str__(self):
        return f'{self.submission.user_name} - {self.question.text[:30]}'

#model for Event
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.title
