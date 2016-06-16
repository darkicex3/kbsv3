from django.conf.urls import url
from . import views

app_name = 'core'
urlpatterns = [
    url(r'^poll_fab/', views.poll, name='poll'),
    url(r'^daily_recap/', views.daily_recap, name='daily_recap'),
    url(r'^get_tenant_style/', views.GetTenantStyle.as_view(), name='get_tenant_style'),
    url(r'^$', views.index, name='home'),
]
