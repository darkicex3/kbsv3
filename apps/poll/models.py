from django.contrib.auth.models import User
from .constants import *
from django.db import models


class Choice(models.Model):
    class Meta:
        app_label = 'poll'

    title = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=TYPE_CHOICES[0], help_text="This choice is"
                                                                                                   "right or wrong ?")

    def __str__(self):
        return self.title


class Question(models.Model):
    class Meta:
        app_label = 'poll'

    illustration = models.FileField(upload_to='questions_img/%Y/%m/%d', blank=True)
    choices = models.ManyToManyField(Choice, blank=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Poll(models.Model):
    class Meta:
        app_label = 'poll'

    title = models.CharField(max_length=255, default='')
    questions = models.ManyToManyField(Question, blank=True)
    users = models.ManyToManyField(User, blank=True, editable=False)
    publish_date = models.DateTimeField(auto_now_add=True, editable=False)
    id_current_question = models.IntegerField(default=0)

    def __str__(self):
        return self.title
