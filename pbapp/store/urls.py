from django.conf.urls import include, url

from . import views


app_name = 'store'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^search/$', views.search, name='search'),
    url(r'^show_products/$', views.display_my_products, name='show'),
    url(r'^add_product/(?P<product_id>[0-9]+)/$', views.add_product_to_favorite, name='add'),
    url(r'^index/$', views.index, name='index'),
    url(r'^detail/(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^log_out/$', views.log_out, name='logOut')
]
