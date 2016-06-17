# -- VENDORS MODELS --
from django_mptt_admin.admin import DjangoMpttAdmin  # DJANGO MPTT ALLOW TREE VIEW
from django_summernote.admin import SummernoteModelAdmin  # DJANGO SUMMERNOTE ALLOW TEXT EDITOR FOR ARTICLES CONTENT
from attachments.admin import AttachmentInlines  # DJANGO ATTACHMENTS ALLOW ATTACHMENTS TO ARTICLES

# -- ARTICLE APP MODELS --
from apps.article.models import Tag, Article, \
    Feedback, Category, FeedbackManager, Comment, DailyRecap

# -- DJANGO ADMIN MODEL --
from django.contrib.admin.models import LogEntry  # LOG OF ALL ACTIONS PERFORM ON ADMIN INTERFACE
from django.contrib import admin

# -- MODELS FUNCTIONS --
from .functions import *  # ADDITIONAL FUNCTIONS FOR MODELS IN DJANGO ADMIN


class TagAdmin(DjangoMpttAdmin):
    list_display = ['name', 'click_counter', 'color']
    ordering = ['name']
    actions = [make_desactivated, make_activated, duplicate_event]


class DailyRecapAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    class Media:
        css = {
            'all': ('core/css/admin/article.css',)
        }
        js = ('core/js/admin/article.js',)

    fieldsets = (
        (None, {
            'fields': ('author', 'title', 'content')
        }),
        ('Advanced options', {
            'fields': ('is_public', 'by_groups', 'authorized_groups', 'authorized_users_dr'),
        }),
    )

    list_display = ['title', 'id', 'modified',
                    'useful_counter', 'view_counter', 'status', 'is_public']

    list_editable = ['status', 'is_public']
    list_filter = ['authorized_groups', 'status', 'publish_date']
    search_fields = ['title', 'id']
    inlines = (AttachmentInlines,)
    ordering = ['title']
    actions = [make_published, make_draft, make_withdrawn, duplicate_event, deleteall, reset_counter]


class ArticleAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    class Media:
        css = {
            'all': ('core/css/admin/article.css',)
        }
        js = ('core/js/admin/article.js',)

    fieldsets = (
        (None, {
            'fields': ('author', 'title', 'content', 'tags')
        }),
        ('Advanced options', {
            'fields': ('essential', 'is_public', 'by_groups', 'authorized_groups', 'authorized_users',
                       'file_content_option', 'file_content', 'file_content_s3', 'url_content_option',
                       'url_article', 'related_questions', 'polls', 'users_likes'),
        }),
    )

    list_display = ['title', 'id', 'publish_date', 'modified',
                    'useful_counter', 'favorite_counter', 'view_counter', 'status', 'is_public']

    list_editable = ['status', 'is_public']
    list_filter = ['authorized_groups', 'status', 'publish_date', 'essential', 'file_content_option',
                   'url_content_option']
    search_fields = ['title', 'id']
    inlines = (AttachmentInlines,)
    ordering = ['title']
    actions = [make_published, make_draft, make_withdrawn, duplicate_event, deleteall, reset_counter]


class FeedBackAdmin(admin.ModelAdmin):
    list_display = ['author', 'get_article_id', 'rate', 'date', 'explanation']
    ordering = ['date']
    list_filter = ['rate', 'date']
    search_fields = ['author']

    def get_article_title(self, obj):
        return '%s' % obj.article.title

    get_article_title.short_description = 'Article Name'

    def get_article_id(self, obj):
        return '%s' % obj.article.id

    get_article_id.short_description = 'Article ID'


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'change_message', 'content_type', 'action_time', 'object_id']
    ordering = ['user_id']
    list_filter = ['user_id', 'action_time', 'content_type']
    search_fields = ['change_message', 'object_id']


class ShortcutAdmin(DjangoMpttAdmin, admin.ModelAdmin):
    list_display = ['name', 'static', 'activated', 'click_counter', 'icon']
    list_editable = ['activated', 'static']
    ordering = ['name']
    actions = [make_desactivated, make_activated, duplicate_event]


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, ShortcutAdmin)
admin.site.register(Feedback, FeedBackAdmin)
admin.site.register(DailyRecap, DailyRecapAdmin)
admin.site.register(FeedbackManager)
admin.site.register(Comment)
