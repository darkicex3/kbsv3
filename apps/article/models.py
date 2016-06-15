from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.core.files.storage import FileSystemStorage
from six import python_2_unicode_compatible
# from haystack.query import SearchQuerySet
from mptt.models import TreeForeignKey, MPTTModel
from .constants import *
import datetime
from django.utils import timezone
from django.db import models
from colorfield.fields import ColorField


def get_upload_filename(instance, filename):
    return "uploaded_files/%s_%s" % (str(datetime.time()).replace('.', '_'), filename)


@python_2_unicode_compatible
class Tag(MPTTModel):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        app_label = 'article'

    name = models.CharField(max_length=50, blank=True, null=True)
    color = ColorField(default='#FF0000', help_text='Please choose a color from <a href="https://flat'
                                                    'uicolors.com/" target="_blank">FLAT UI Color</a>')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    click_counter = models.IntegerField(default=0, editable=False)

    def get_previous_parent(self):
        return self.parent.parent

    def __str__(self):
        return self.name or ''


@python_2_unicode_compatible
class Comment(MPTTModel):
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        app_label = 'article'

    author = models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_AUTHOR_ID)
    comment = models.CharField(max_length=50, blank=True, null=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def get_previous_parent(self):
        return self.parent.parent

    def __str__(self):
        return self.name or ''


class FeedbackManager(models.Model):
    class Meta:
        verbose_name = 'FeedBack Manager'
        verbose_name_plural = 'FeedBack Manager'
        app_label = 'article'

    alert_useless_actived = models.BooleanField(default=False)
    max_useless = models.IntegerField(null=True)

    alert_view_actived = models.BooleanField(default=False)
    min_view = models.IntegerField(null=True)


class DailyRecap(models.Model):
    class Meta:
        verbose_name_plural = 'Daily Recaps'
        verbose_name = 'Daily Recap'
        app_label = 'article'

    # REQUIRED
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_AUTHOR_ID)
    title = models.CharField(max_length=255, default='')
    authorized_users_dr = models.ManyToManyField(User, help_text=group_help, blank=True,
                                                 related_name='authorized_users_dr')
    is_public = models.BooleanField(default=True, help_text=is_public_info)
    by_groups = models.BooleanField(default=True, help_text=by_groups_info)
    authorized_groups = models.ManyToManyField(Group, help_text=group_help, blank=True)
    content = models.TextField(default='')
    modified = models.DateTimeField(editable=False)
    publish_date = models.DateTimeField(help_text=publish_date_help, auto_now_add=True, editable=False)
    view_counter = models.IntegerField(default=0, editable=False)
    useful_counter = models.IntegerField(default=0, editable=False)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_CHOICES[0])

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(DailyRecap, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Article(models.Model):
    class Meta:
        verbose_name_plural = 'Articles'
        app_label = 'article'

    # REQUIRED
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_AUTHOR_ID, related_name='author_article')
    authorized_users = models.ManyToManyField(User, help_text=group_help, blank=True, related_name='authorized_users')
    is_public = models.BooleanField(default=True, help_text=is_public_info)
    by_groups = models.BooleanField(default=True, help_text=by_groups_info)
    authorized_groups = models.ManyToManyField(Group, help_text=group_help, blank=True)
    title = models.CharField(max_length=255, default='')
    content = models.TextField(default='', blank=True)
    file_content_option = models.BooleanField(default=False, help_text=help_option_content)
    url_content_option = models.BooleanField(default=False, help_text=help_option_url)
    url_article = models.CharField(max_length=255, default='', blank=True)
    file_content = models.FileField(upload_to='article_pdf',
                                    blank=True)
    publish_date = models.DateTimeField(help_text=publish_date_help, auto_now_add=True, editable=False)
    modified = models.DateTimeField(editable=False)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_CHOICES[0])
    tags = models.ManyToManyField(Tag, help_text=tags_help)

    # COUNTERS
    useful_counter = models.IntegerField(default=0, editable=False)
    favorite_counter = models.IntegerField(default=0, editable=False)
    view_counter = models.IntegerField(default=0, editable=False)

    # OPTIONNAL
    essential = models.BooleanField(default=False, help_text=ess_help)
    related_questions = models.ManyToManyField('poll.Question', help_text=tags_help, blank=True)
    polls = models.ManyToManyField('poll.Poll', help_text=tags_help, blank=True)
    expiration_date = models.DateTimeField(blank=True, null=True, help_text=expiration_date)

    # STATS
    users_likes = models.ManyToManyField(User, blank=True, related_name='users_likes')
    users_bigup = models.ManyToManyField(User, blank=True, related_name='users_bigup')
    users_view = models.ManyToManyField(User, blank=True, related_name='users_view')
    users_read = models.ManyToManyField(User, blank=True, related_name='users_read')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Article, self).save(*args, **kwargs)

    def get_feedback_alert(self):
        context = {}
        if self.feedback.alert_view_actived:
            if self.feedback.view < self.feedback.min_view:
                context['alert_view'] = MSG_VIEW_ALERT
            else:
                context['alert_view'] = ''

        if self.feedback.alert_useless_actived:
            if self.feedback.useless > self.feedback.max_useless:
                context['alert_useless'] = MSG_USELESS_ALERT
            else:
                context['alert_useless'] = ''

        return context

    def __str__(self):
        return self.title


class Feedback(models.Model):
    class Meta:
        verbose_name = 'FeedBack'
        verbose_name_plural = 'FeedBacks'
        app_label = 'article'

    date = models.DateTimeField()
    author = models.ForeignKey(User, null=True, related_name='author')
    article = models.ForeignKey(Article, null=True, related_name='article')
    rate = models.CharField(max_length=1, choices=RATE_CHOICES, default=RATE_CHOICES[2])
    explanation = models.TextField(default='')

    def __str__(self):
        return self.rate


@python_2_unicode_compatible
class Category(MPTTModel):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=300, unique=True)
    icon = models.CharField(max_length=500, default="radio_button_checked", help_text="Add an icon to your category ! <a href=\"ht"
                                                                           "tps://design.google.com/ico"
                                                                           "ns/\">Click Here !</a>", null=True,
                            blank=True)
    articles = models.ManyToManyField(Article, help_text=tags_help, blank=True)
    activated = models.BooleanField(default=True)
    click_counter = models.IntegerField(default=0)
    static = models.BooleanField(default=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def get_previous_parent(self):
        return self.parent.parent

    def __str__(self):
        return self.name or ''

