from django.contrib import admin
from .models import Question, Answer

# Register your models here.
admin.site.register(Answer)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'question_text']

