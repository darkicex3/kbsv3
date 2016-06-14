from django.contrib import admin
# -- ARTICLE APP MODELS --
from apps.poll.models import Poll, Question, Choice


class PollQuestionsInline(admin.TabularInline):
    model = Poll.questions.through


class QuestionChoicesInline(admin.TabularInline):
    model = Question.choices.through


class PollAdmin(admin.ModelAdmin):
    inlines = (PollQuestionsInline,)
    exclude = ('questions',)
    list_display = ['title', 'id', 'publish_date', 'id_current_question']
    list_filter = ['publish_date']
    ordering = ['id']


class QuestionAdmin(admin.ModelAdmin):
    inlines = (QuestionChoicesInline,)
    exclude = ('choices',)
    list_display = ['title', 'id']
    ordering = ['title']


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'votes', 'type', 'id']
    list_editable = ['type']


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
