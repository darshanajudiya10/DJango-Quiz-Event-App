from django.contrib import admin

from .models import Answer, Event, Question, Quiz, UserAnswer, UserSubmission


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'question_type', 'created_at')
    list_filter = ('question_type', 'quiz')
    search_fields = ('text',)
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text',)


class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0


@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'quiz', 'score', 'submitted_at')
    list_filter = ('quiz',)
    search_fields = ('user_name',)
    inlines = [UserAnswerInline]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    search_fields = ('title', 'location')
