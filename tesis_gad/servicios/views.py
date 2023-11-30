''' Import libraries '''
import os
from django.shortcuts import render
from django.conf import settings
from datetime import datetime
import json
import requests
from unidecode import unidecode
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError


def index(request):
    '''Función que devuelve la página de inicio del reporte'''
    contex = {}

    return render(request, 'servicios/index.html', contex)


def responder(request):
    '''Función que maneja las opciones escogidas por el usuario'''
    servicio_seleccionado = request.GET['servicio']
    contex = {}

    url_servicios = "http://sistema-munipal.lat/api/service"
    response_servicios = requests.get(url_servicios)

    url = "http://sistema-munipal.lat/api/course"
    response_cursos = requests.get(url)

    if response_cursos.status_code == 200 and response_servicios.status_code == 200:
        data_cursos = response_cursos.json()
        data_servicios = response_servicios.json()
    else:
        print(
            f"Error al obtener los datos. Código de estado: {response_cursos.status_code}")

    if servicio_seleccionado == 'deportes':
        # Lógica para obtener datos específicos de deportes si es necesario
        filtered_ids = [item["_id"]
                        for item in data_servicios["data"] if "futbol" in item["name"].lower()]

        filtered_courses = [
            item for item in data_cursos["data"] if item["_service"] in filtered_ids]

        contex["data"] = json.dumps(filtered_courses)

        return render(request, 'servicios/deportes_form.html', contex)
    elif servicio_seleccionado == 'infocentro':
        # Lógica para obtener datos específicos de infocentro si es necesario
        filtered_ids = [item["_id"]
                        for item in data_servicios["data"] if "infocentro" in item["name"].lower()]
        filtered_courses = [
            item for item in data_cursos["data"] if item["_service"] in filtered_ids]

        contex["data"] = json.dumps(filtered_courses)

        return render(request, 'servicios/infocentro_form.html', contex)
    elif servicio_seleccionado == 'salud':
        # Lógica para obtener datos específicos de infocentro si es necesario
        filtered_ids = [item["_id"]
                        for item in data_servicios["data"] if "rehabilitacion" in item["name"].lower()]
        filtered_courses = [
            item for item in data_cursos["data"] if item["_service"] in filtered_ids]

        contex["data"] = json.dumps(filtered_courses)

        return render(request, 'servicios/centro_medico_form.html', contex)


def registrar_deportes(request):
    if request.method == 'POST':
        print(request.POST)
        # Accede a los datos del formulario

        zona_eleccion = request.POST['zona_eleccion']
        fecha_objeto = datetime.strptime(request.POST['fecha'], "%Y-%m-%d")
        epoch = int(fecha_objeto.timestamp() * 1000)
        direccion = unidecode(request.POST.get('flt_canton_list', ''))
        celular = "0" + request.POST['flt_telefono'].replace("-", "")[-9:]
        cedula = request.POST['flt_cedula']
        genero = "M" if request.POST['flt_genero_list'] == "masculino" else "F"
        id_course = request.POST['id_course']

        nombre_completo = ' '.join(word.capitalize() for word in (
            request.POST['flt_nombre_1'],
            request.POST['flt_nombre_2'],
            request.POST['flt_apellidos']
        ))

        print(
            f"Datos: {zona_eleccion}, {genero}, {cedula}, {nombre_completo}, {direccion}, {epoch}, {celular}, {id_course}")

        url = 'http://sistema-munipal.lat/api/inscription'

        # Datos a enviar en el cuerpo de la solicitud
        data = {
            "name": nombre_completo,
            "birdthDate": epoch,
            "zone": zona_eleccion,
            "address": direccion,
            "phone": celular,
            "cedula": cedula,
            "sexo": genero,
            "_course": id_course
        }

        try:
            # Realizar la solicitud POST
            response = requests.post(url, json=data)
            response.raise_for_status()  # Lanzar una excepción si la solicitud no es exitosa
            print(response.status_code)
            print(response.text)

            # Devolver un mensaje exitoso
            return HttpResponse(
                content=json.dumps(
                    {'status': 'success', 'redirect_url': '/servicios/index/'}),
                content_type='application/json'
            )
        except requests.exceptions.RequestException as e:
            # Capturar cualquier excepción que ocurra durante la solicitud
            return HttpResponseServerError(content=json.dumps({'status': 'error', 'message': str(e)}), content_type='application/json')
    return None


def registrar_infocentro(request):
    if request.method == 'POST':
        print(request.POST)
        # Accede a los datos del formulario

        zona_eleccion = request.POST['zona_eleccion']
        fecha_objeto = datetime.strptime(request.POST['fecha'], "%Y-%m-%d")
        epoch = int(fecha_objeto.timestamp() * 1000)
        direccion = unidecode(request.POST.get('flt_canton_list', ''))
        celular = "0" + request.POST['flt_telefono'].replace("-", "")[-9:]
        cedula = request.POST['flt_cedula']
        genero = "M" if request.POST['flt_genero_list'] == "masculino" else "F"
        id_course = request.POST['id_course']

        nombre_completo = ' '.join(word.capitalize() for word in (
            request.POST['flt_nombre_1'],
            request.POST['flt_nombre_2'],
            request.POST['flt_apellidos']
        ))

        print(
            f"Datos: {zona_eleccion}, {genero}, {cedula}, {nombre_completo}, {direccion}, {epoch}, {celular}, {id_course}")

        url = 'http://sistema-munipal.lat/api/inscription'

        # Datos a enviar en el cuerpo de la solicitud
        data = {
            "name": nombre_completo,
            "birdthDate": epoch,
            "zone": zona_eleccion,
            "address": direccion,
            "phone": celular,
            "cedula": cedula,
            "sexo": genero,
            "_course": id_course
        }

        try:
            # Realizar la solicitud POST
            response = requests.post(url, json=data)
            response.raise_for_status()  # Lanzar una excepción si la solicitud no es exitosa
            print(response.status_code)
            print(response.text)

            # Devolver un mensaje exitoso
            return HttpResponse(
                content=json.dumps(
                    {'status': 'success', 'redirect_url': '/servicios/index/'}),
                content_type='application/json'
            )
        except requests.exceptions.RequestException as e:
            # Capturar cualquier excepción que ocurra durante la solicitud
            return HttpResponseServerError(content=json.dumps({'status': 'error', 'message': str(e)}), content_type='application/json')
    return None


def registrar_salud(request):
    if request.method == 'POST':
        print(request.POST)
        # Accede a los datos del formulario

    return None