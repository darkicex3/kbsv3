from django.conf.urls import url
from kbsv3.views import HomeView
from apps.core.views import TenantView
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
import notifications
from notifications import urls
from . import settings


urlpatterns = [
    url(r'^$', HomeView.as_view()),
    url(r'^site_media/media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
]
