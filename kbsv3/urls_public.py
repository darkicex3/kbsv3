from django.conf.urls import url
from kbsv3.views import HomeView
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
import notifications
from notifications import urls
from . import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^site_media/media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^', HomeView.as_view()),
]
