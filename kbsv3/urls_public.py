from django.conf.urls import url
from kbsv3.views import HomeView


urlpatterns = [
    url(r'^$', HomeView.as_view()),
]
