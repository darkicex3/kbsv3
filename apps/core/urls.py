from django.conf.urls import url
from . import views

app_name = 'core'
urlpatterns = [
    url(r'^poll_fab/', views.poll, name='poll'),
    url(r'^daily_recap/', views.daily_recap, name='daily_recap'),
    url(r'^$', views.index, name='home'),
]
