from django.conf.urls import url
from kbsv3.views import HomeView
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', HomeView.as_view()),
    url(r'^admin/', admin.site.urls),
]
