import requests
import time

# Configuración de la solicitud
url = 'https://apiqa.laaraucana.cl/crom/api/commercial-validations/simulation/simulate'
headers = {
    'x-api-key': 'AIzaSyDpCtP5VRhszsUcnkA2wN82hLj9j5bJFwE',
    'Content-Type': 'application/json'
}
payload = {
    "companyRut": "76429857-8",
    "amount": "10000000",
    "fee": "12",
    "office": "101",
    "unemploymentInsurance": "X",
    "deceaseInsurance": "X",
    "insuranceType": "08",
    "affiliateType": "2"
}

# Número de solicitudes a enviar
num_requests = 1000
# Intervalo entre solicitudes (en segundos)
interval = 0.1

# Lista para almacenar respuestas que no son 200
non_200_responses = []

for i in range(num_requests):
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        non_200_responses.append((i+1, response.status_code, response.text))
    print(f'Solicitud {i+1}: Estado {response.status_code}')
    # se duerme por el intervalo especificado
    time.sleep(interval)

# Mostrar resultados al final
print("\nPrueba de control de itinerancia completada.")
print("Respuestas del servidor que no fueron 200:")
for req_num, status_code, response_text in non_200_responses:
    print(f'Solicitud {req_num}: Estado {status_code}, Respuesta: {response_text}')


input("\nPresiona Enter para finalizar...")
