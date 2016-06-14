from django.conf.urls import include, url
from apps.poll import views


urlpatterns = [
    url(r'^get_current_question/', views.GetCurrentQuestionView.as_view(), name='get_current_question'),
]

