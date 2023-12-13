from django.urls import re_path as url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url('^response/$', views.responder),
    url('^registro-deportes/$', views.registrar_deportes, name='registrar_deportes'),
    url('^registro-infocentro/$', views.registrar_infocentro, name='registrar_infocentro'),
    url('^registro-salud/$', views.registrar_salud, name='registrar_salud'),
]
