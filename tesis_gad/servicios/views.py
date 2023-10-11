''' Import libraries '''
import os
from django.shortcuts import render
from django.conf import settings
import traceback
import sys
import json
from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    '''Función que devuelve la página de inicio del reporte'''
    contex = {}

    return render(request, 'servicios/index.html', contex)


def responder(request):
    '''Función que maneja las opciones escogidas por el usuario'''
    contex = {}

    return render(request, 'servicios/deportes_form.html', contex)