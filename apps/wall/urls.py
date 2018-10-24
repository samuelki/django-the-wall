from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^wall$', views.wall),
    url(r'^logout$', views.logout),
    url(r'^add_message$', views.add_message),
    url(r'^message/(?P<id>\d+)/delete$', views.delete_message),
    url(r'^comment$', views.comment)
]