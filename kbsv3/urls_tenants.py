from apps.core.views import TenantView
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
import notifications
from notifications import urls
from . import settings

urlpatterns = [
    # url(r'^$', TenantView.as_view()),
    url(r'^site_media/media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
    url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^attachments/', include('attachments.urls', namespace='attachments')),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^manager/', include('apps.manager.urls', namespace='contents')),
    url(r'^article/', include('apps.article.urls', namespace='articles')),
    url(r'^poll/', include('apps.poll.urls', namespace='polls')),
    url(r'^registration/', include('apps.registration.urls', namespace='registration')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.core.urls', namespace='core')),
]
