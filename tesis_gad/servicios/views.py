''' Import libraries '''
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
    response_servicios = requests.get(url_servicios, timeout=3)

    url = "http://sistema-munipal.lat/api/course"
    response_cursos = requests.get(url, timeout=3)

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

    if servicio_seleccionado == 'infocentro':
        # Lógica para obtener datos específicos de infocentro si es necesario
        filtered_ids = [item["_id"]
                        for item in data_servicios["data"] if "infocentro" in item["name"].lower()]
        filtered_courses = [
            item for item in data_cursos["data"] if item["_service"] in filtered_ids]

        contex["data"] = json.dumps(filtered_courses)

        return render(request, 'servicios/infocentro_form.html', contex)

    if servicio_seleccionado == 'salud':
        # Lógica para obtener datos específicos de infocentro si es necesario
        filtered_ids = [item["_id"]
                        for item in data_servicios["data"]
                        if "rehabilitacion" in item["name"].lower()]
        filtered_courses = [
            item for item in data_cursos["data"] if item["_service"] in filtered_ids]

        contex["data"] = json.dumps(filtered_courses)

        return render(request, 'servicios/centro_medico_form.html', contex)
    return None


def registrar_deportes(request):
    ''' Función que registra los servicios de deportes '''
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
            response = requests.post(url, json=data, timeout=3)
            response.raise_for_status()  # Lanzar una excepción si la solicitud no es exitosa

            # Devolver un mensaje exitoso
            return HttpResponse(
                content=json.dumps(
                    {'status': 'success', 'redirect_url': '/'}),
                content_type='application/json'
            )
        except requests.exceptions.RequestException as e:
            # Extrae el mensaje de error de la respuesta de la API
            try:
                error_response = json.loads(e.response.text)
                error_message = error_response.get(
                    'statusMessage', 'Error desconocido en el servidor')
            except (json.JSONDecodeError, AttributeError):
                # Si no se puede decodificar el JSON o si no hay respuesta, usa un mensaje genérico
                error_message = 'Error desconocido en el servidor'

            # Devolver el mensaje de error al cliente
            return HttpResponseServerError(
                content=json.dumps(
                    {'status': 'error', 'message': error_message}),
                content_type='application/json'
            )
    return None


def registrar_infocentro(request):
    ''' Función que registra los servicios de infocentro '''
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
            response = requests.post(url, json=data, timeout=3)
            response.raise_for_status()  # Lanzar una excepción si la solicitud no es exitosa

            # Devolver un mensaje exitoso
            return HttpResponse(
                content=json.dumps(
                    {'status': 'success', 'redirect_url': '/'}),
                content_type='application/json'
            )
        except requests.exceptions.RequestException as e:
            # Extrae el mensaje de error de la respuesta de la API
            try:
                error_response = json.loads(e.response.text)
                error_message = error_response.get(
                    'statusMessage', 'Error desconocido en el servidor')
            except (json.JSONDecodeError, AttributeError):
                # Si no se puede decodificar el JSON o si no hay respuesta, usa un mensaje genérico
                error_message = 'Error desconocido en el servidor'

            # Devolver el mensaje de error al cliente
            return HttpResponseServerError(
                content=json.dumps(
                    {'status': 'error', 'message': error_message}),
                content_type='application/json'
            )
    return None


def registrar_salud(request):
    ''' Función que registra los servicios de salud '''
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
            response = requests.post(url, json=data, timeout=3)
            response.raise_for_status()  # Lanzar una excepción si la solicitud no es exitosa

            # Devolver un mensaje exitoso
            return HttpResponse(
                content=json.dumps(
                    {'status': 'success', 'redirect_url': '/'}),
                content_type='application/json'
            )
        except requests.exceptions.RequestException as e:
            # Extrae el mensaje de error de la respuesta de la API
            try:
                error_response = json.loads(e.response.text)
                error_message = error_response.get(
                    'statusMessage', 'Error desconocido en el servidor')
            except (json.JSONDecodeError, AttributeError):
                # Si no se puede decodificar el JSON o si no hay respuesta, usa un mensaje genérico
                error_message = 'Error desconocido en el servidor'

            # Devolver el mensaje de error al cliente
            return HttpResponseServerError(
                content=json.dumps(
                    {'status': 'error', 'message': error_message}),
                content_type='application/json'
            )
    return None
