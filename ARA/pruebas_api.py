import requests
import time
import json
from datetime import datetime

def get_api_details():
    url = input("Introduce la URL de la API: ")
    headers = {}
    while True:
        header_key = input("Introduce el nombre del header (o presiona Enter para terminar): ")
        if header_key == "":
            break
        header_value = input(f"Introduce el valor del header '{header_key}': ")
        headers[header_key] = header_value
    return url, headers

def get_payload():
    print("Introduce el body en formato JSON. Por ejemplo: {\"rutAfiliado\": \"16206119-4\"}")
    payload_str = input("Body JSON: ")
    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        print("El body no es un JSON válido. Inténtalo de nuevo.")
        return get_payload()
    return payload

def print_request_details(url, headers, payload, method):
    print("\nDetalles de la solicitud que se va a enviar:")
    print(f"URL: {url}")
    print(f"Método: {method}")
    print("Headers:")
    for key, value in headers.items():
        print(f"  {key}: {value}")
    print("Body:")
    print(json.dumps(payload, indent=2))

def print_results(test_name, responses):
    print(f"\nResultados de la prueba: {test_name}")
    for req_num, status_code, response_text in responses:
        print(f'Solicitud {req_num}: Estado {status_code}')
        if response_text:
            try:
                json_response = json.loads(response_text)
                print(f"La API respondió con: {json.dumps(json_response, indent=2)}")
            except json.JSONDecodeError:
                print(f"La API respondió con: {response_text}")
        else:
            print(f"La API no devolvió nada. Estado: {status_code}")

def check_security_headers(response):
    security_headers = [
        'Content-Security-Policy',
        'Strict-Transport-Security',
        'X-Content-Type-Options',
        'X-Frame-Options',
        'X-XSS-Protection'
    ]
    missing_headers = [header for header in security_headers if header not in response.headers]
    if missing_headers:
        print("\nCabeceras de seguridad faltantes:")
        for header in missing_headers:
            print(f"  - {header}")
    else:
        print("\nTodas las cabeceras de seguridad están presentes.")
    return missing_headers

def save_results_to_file(test_name, responses, missing_headers=None):
    filename = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    results = {
        "test_name": test_name,
        "responses": responses,
        "missing_headers": missing_headers or []
    }
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResultados guardados en el archivo: {filename}")

def handle_request(url, headers, payload, method="POST"):
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=payload)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=payload)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=payload)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, json=payload)
        elif method.upper() == "PATCH":
            response = requests.patch(url, headers=headers, json=payload)
        else:
            print(f"Método HTTP '{method}' no soportado.")
            return None
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None

def test_auth(url, headers, payload):
    print("Ejecutando prueba de autenticación y autorización...")
    print("Headers actuales:")
    for key, value in headers.items():
        print(f"  {key}: {value}")
    api_key_param = input("Introduce el nombre del parámetro donde está la API key: ")
    invalid_api_key = input("Introduce el valor de la API key inválida: ")
    invalid_headers = headers.copy()
    if api_key_param in invalid_headers:
        invalid_headers[api_key_param] = invalid_api_key
        print_request_details(url, invalid_headers, payload, "POST")
        response = handle_request(url, invalid_headers, payload)
        if response:
            print_response("Prueba de autenticación", response)
            missing_headers = check_security_headers(response)
            save_results_to_file("Autenticación y Autorización", [(1, response.status_code, response.text)], missing_headers)
    else:
        print(f"El parámetro '{api_key_param}' no se encuentra en los headers.")

def test_validation(url, headers, payload):
    print("Ejecutando prueba de validación de entradas...")
    invalid_payload = payload.copy()
    responses = []
    for key in payload.keys():
        invalid_value = input(f"Introduce un valor no válido para el parámetro '{key}': ")
        invalid_payload[key] = invalid_value
        print_request_details(url, headers, invalid_payload, "POST")
        response = handle_request(url, headers, invalid_payload)
        if response:
            print_response(f'Prueba de validación para {key}', response)
            responses.append((key, response.status_code, response.text))
        invalid_payload[key] = payload[key]
    if responses:
        missing_headers = check_security_headers(response)
        save_results_to_file("Validación de Entradas", responses, missing_headers)

def test_sqli(url, headers, payload):
    print("Ejecutando prueba de inyección SQL...")
    param_to_test = input("Introduce el nombre del parámetro donde deseas probar la inyección SQL: ")
    sqli_statement = input("Introduce la sentencia SQL que deseas inyectar: ")
    sqli_payload = payload.copy()
    if param_to_test in sqli_payload:
        sqli_payload[param_to_test] += sqli_statement
        print_request_details(url, headers, sqli_payload, "POST")
        response = handle_request(url, headers, sqli_payload)
        if response:
            print_response(f'Prueba de inyección SQL para {param_to_test}', response)
            missing_headers = check_security_headers(response)
            save_results_to_file("Inyección SQL", [(param_to_test, response.status_code, response.text)], missing_headers)
    else:
        print(f"El parámetro '{param_to_test}' no se encuentra en el payload.")

def test_headers(url, headers, payload):
    print("Mostrando cabeceras de respuesta...")
    print_request_details(url, headers, payload, "POST")
    response = handle_request(url, headers, payload)
    if response:
        for key, value in response.headers.items():
            print(f'{key}: {value}')
        missing_headers = check_security_headers(response)
        save_results_to_file("Cabeceras de Respuesta", [(1, response.status_code, response.text)], missing_headers)

def test_fuzzing(url, headers, payload):
    print("Ejecutando prueba de fuzzing...")
    char_to_repeat = input("Introduce el carácter que deseas repetir: ")
    repeat_count = int(input("Introduce el número de repeticiones: "))
    fuzz_payload = payload.copy()
    fuzz_payload["extraField"] = char_to_repeat * repeat_count
    print_request_details(url, headers, fuzz_payload, "POST")
    response = handle_request(url, headers, fuzz_payload)
    if response:
        print_response("Prueba de fuzzing", response)
        missing_headers = check_security_headers(response)
        save_results_to_file("Fuzzing", [(1, response.status_code, response.text)], missing_headers)

def test_rate_limiting(url, headers, payload):
    print("Ejecutando prueba de control de itinerancia...")
    num_requests = int(input("Introduce el número de solicitudes a enviar: "))
    interval_ms = float(input("Introduce el intervalo entre solicitudes (en milisegundos): "))
    interval = interval_ms / 1000  # Convertir a segundos
    rate_limit_responses = []
    print_request_details(url, headers, payload, "POST")
    for i in range(num_requests):
        response = handle_request(url, headers, payload)
        if response:
            print(f'Solicitud {i + 1}: Estado {response.status_code}')
            if response.status_code != 200:
                rate_limit_responses.append((i + 1, response.status_code, response.text))
        time.sleep(interval)
    if rate_limit_responses:
        save_results_to_file("Control de Itinerancia", rate_limit_responses)

def test_verb_tampering(url, headers, payload):
    print("Ejecutando prueba de verb tampering...")
    method = input("Introduce el método HTTP que deseas probar (GET, POST, PUT, DELETE, PATCH): ")
    print_request_details(url, headers, payload, method)
    response = handle_request(url, headers, payload, method)
    responses = []
    if response:
        print_response(f'Prueba de verb tampering con método {method}', response)
        responses.append((method, response.status_code, response.text))
        missing_headers = check_security_headers(response)
        save_results_to_file(f"Verb Tampering ({method})", responses, missing_headers)

def print_response(test_name, response):
    status_code = response.status_code
    response_text = response.text
    if response_text:
        try:
            json_response = json.loads(response_text)
            print(f'{test_name}: Estado {status_code}, Respuesta:')
            print(json.dumps(json_response, indent=2))
        except json.JSONDecodeError:
            print(f'{test_name}: Estado {status_code}, Respuesta:')
            print(response_text)
    else:
        print(f'{test_name}: Estado {status_code}, La API no devolvió nada.')

def main():
    url, headers = get_api_details()
    payload = get_payload()

    while True:
        print("\nSelecciona una prueba a realizar:")
        print("1. Prueba de Autenticación y Autorización")
        print("2. Prueba de Validación de Entradas")
        print("3. Prueba de Inyección SQL")
        print("4. Mostrar Cabeceras de Respuesta")
        print("5. Prueba de Fuzzing")
        print("6. Prueba de Control de Itinerancia")
        print("7. Prueba de Verb Tampering")
        print("8. Salir")

        choice = input("Introduce el número de la prueba que deseas realizar: ")

        if choice == "1":
            test_auth(url, headers, payload)
        elif choice == "2":
            test_validation(url, headers, payload)
        elif choice == "3":
            test_sqli(url, headers, payload)
        elif choice == "4":
            test_headers(url, headers, payload)
        elif choice == "5":
            test_fuzzing(url, headers, payload)
        elif choice == "6":
            test_rate_limiting(url, headers, payload)
        elif choice == "7":
            test_verb_tampering(url, headers, payload)
        elif choice == "8":
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción del 1 al 8.")
    
    input("\nPresiona Enter para finalizar...")

if __name__ == "__main__":
    main()
