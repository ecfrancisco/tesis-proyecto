from django.urls import re_path as url
from . import views

urlpatterns = [
    url(r'^index/$', views.index),
    url('^response/$', views.responder),
    url('^registro/$', views.registrar_deportes, name='registrar_deportes'),
]
