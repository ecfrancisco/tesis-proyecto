''' Import libraries '''
import os
from django.shortcuts import render
from django.conf import settings
from datetime import datetime
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    '''Función que devuelve la página de inicio del reporte'''
    contex = {}

    return render(request, 'servicios/index.html', contex)


def responder(request):
    '''Función que maneja las opciones escogidas por el usuario'''
    contex = {}

    url = "http://sistema-munipal.lat/api/course"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.dumps(response.json())

        # for course_data in data.get('data', []):
        #     # Obtener datos generales
        #     spaces = course_data.get("spaces")
        #     startDate = course_data.get("startDate")
        #     endDate = course_data.get("endDate")

        #     # Obtener datos de los horarios
        #     schedules = course_data.get("schedules", [])
        #     for schedule in schedules:
        #         startTime = schedule.get("startTime")
        #         endTime = schedule.get("endTime")
        #         day = schedule.get("day")
        #         # print(f"Horario: {day}, Inicio: {startTime}, Fin: {endTime}")

        #     # Obtener el nombre del profesor si existe
        #     teacher_data = course_data.get("_teacher", {})
        #     teacher_fullName = teacher_data.get("fullName", "")
        #     # print(f"Nombre del profesor: {teacher_fullName}")

        #     course_name = course_data["name"]
        #     print(f"Nombre del curso: {course_name}")

        #     # Obtener datos según el nombre
        #     name_to_search = "Escuela de fufbol sub 10-14"
        #     if course_name.strip() == name_to_search.strip():
        #         print("Hola")
        #         print(f"Datos para {name_to_search}:")
        #         print(f"Espacios: {spaces}")
        #         print(f"Fecha de inicio: {startDate}")
        #         print(f"Fecha de fin: {endDate}")
        contex["data"] = data
    else:
        print(
            f"Error al obtener los datos. Código de estado: {response.status_code}")

    return render(request, 'servicios/deportes_form.html', contex)


def registrar_deportes(request):
    if request.method == 'POST':
        print(request.POST)
        # Accede a los datos del formulario

        horario = request.POST['horario']
        flt_curso = request.POST['flt_curso']
        # Otros campos del formulario...

        nombre_completo = ' '.join(word.capitalize() for word in (
            request.POST['flt_nombre_1'],
            request.POST['flt_nombre_2'],
            request.POST['flt_apellidos']
        ))
        zona_eleccion = request.POST['zona_eleccion']
        fecha_objeto = datetime.strptime(request.POST['fecha'], "%Y-%m-%d")
        epoch = int(fecha_objeto.timestamp())
        direccion = request.POST['flt_canton_list'].capitalize()
        celular = "0" + request.POST['flt_telefono'].replace("-", "")[-9:]
        cedula = ''
        genero = "M" if request.POST['femenino'] == "masculino" else "F"

        # Resto de la lógica de la vista...
        return HttpResponse(status=400)
