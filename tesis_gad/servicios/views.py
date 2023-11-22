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
    contex = {}

    url = "http://sistema-munipal.lat/api/course"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.dumps(response.json())
        contex["data"] = data
    else:
        print(
            f"Error al obtener los datos. Código de estado: {response.status_code}")

    return render(request, 'servicios/deportes_form.html', contex)


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

        # Convertir el diccionario a formato JSON
        json_data = json.dumps(data)

        print(json_data)

        try:
            # Realizar la solicitud POST
            response = requests.post(url, json=json_data)
            response.raise_for_status()  # Lanzar una excepción si la solicitud no es exitosa
            print(response.status_code)
            print(response.text)

            # Devolver un mensaje exitoso
            return response
        except requests.exceptions.RequestException as e:
            # Capturar cualquier excepción que ocurra durante la solicitud
            return HttpResponseServerError(content=json.dumps({'status': 'error', 'message': str(e)}), content_type='application/json')
        # Imprimir la respuesta

        # Resto de la lógica de la vista...
        # return HttpResponse(status=400)
