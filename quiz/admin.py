from django.contrib import admin
from models import Question, Score, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    fields = ('answer', 'weight')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'correct_answer')
    
    inlines = [AnswerInline]


admin.site.register(Question)
#admin.site.register(Question, QuestionAdmin)
admin.site.register(Score)
admin.site.register(Answer)