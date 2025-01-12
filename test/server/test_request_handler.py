import pytest
from unittest.mock import MagicMock
from io import BytesIO
import json

from server.request_handler import RequestHandler
from server.constants import HttpStatus, HttpMethod


@pytest.fixture
def handler():
    # Creamos un mock para la ruta
    mock_handler = MagicMock()
    routes = {
        ("/ping", HttpMethod.POST): mock_handler,  # Ruta válida
    }
    # Instanciamos RequestHandler con las rutas mockeadas
    return RequestHandler(routes), mock_handler


def test_process_request_valid_json(handler):
    handler_instance, mock_handler = handler
    # Simulamos el cuerpo de la solicitud en formato JSON válido
    headers = {"Content-Length": "42"}
    body = BytesIO(b'{"message": "pong", "status": true}')  # Cuerpo válido JSON

    # Definimos lo que esperamos
    mock_handler.return_value = {"response": "pong"}

    # Llamamos al método
    response, status_code = handler_instance.process_request(
        "request", "/ping", "POST", headers, body
    )

    # Verificamos los resultados
    mock_handler.assert_called_once_with("request", {"message": "pong", "status": True})
    assert status_code == HttpStatus.OK
    assert response == {"response": "pong"}


def test_process_request_invalid_json(handler):
    handler_instance, _ = handler
    # Simulamos el cuerpo de la solicitud con un JSON inválido
    headers = {"Content-Length": "20"}
    body = BytesIO(b'{"message": "pong", "status": ')  # JSON roto

    # Llamamos al método
    response, status_code = handler_instance.process_request(
        "request", "/ping", "POST", headers, body
    )

    # Verificamos el error que debería haberse producido
    assert status_code == HttpStatus.BAD_REQUEST
    assert response == "Invalid JSON"


def test_process_request_route_not_found(handler):
    handler_instance, _ = handler
    # Simulamos una ruta no existente
    headers = {"Content-Length": "42"}
    body = BytesIO(b'{"message": "pong", "status": true}')  # Cuerpo válido JSON

    # Llamamos al método con una ruta que no existe
    response, status_code = handler_instance.process_request(
        "request", "/notfound", "POST", headers, body
    )

    # Verificamos que la respuesta sea "Not Found"
    assert status_code == HttpStatus.NOT_FOUND
    assert response == "Not Found"


def test_process_request_unsupported_body_format(handler):
    handler_instance, _ = handler
    # Simulamos un cuerpo de solicitud que no puede ser leído como un flujo
    headers = {"Content-Length": "42"}
    body = "Unsupported body format"  # Cuerpo no en formato de flujo (BufferedReader)

    # Llamamos al método
    response, status_code = handler_instance.process_request(
        "request", "/ping", "POST", headers, body
    )

    # Verificamos que el formato no soportado fue manejado correctamente
    assert status_code == HttpStatus.INTERNAL_SERVER
    assert response == "Unsupported body format"
