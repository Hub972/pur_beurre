from django.conf.urls import include, url

from . import views



app_name = 'store'
urlpatterns = [
    url(r'^login/$', views.login, name='login')
]