''' Import libraries '''
import os
from django.shortcuts import render
from django.conf import settings


def index(request):
    '''Función que devuelve la página de inicio del reporte'''
    contex = {}

    return render(request, 'login/index.html', contex)
