Uso del Script

# API Security Testing Script

Este script permite realizar una serie de pruebas de seguridad en cualquier API, incluyendo pruebas de autenticación, validación de entradas, inyección SQL, fuzzing, control de itinerancia, verb tampering, y verificación de cabeceras de seguridad.

## Requisitos

- Python 3.x
- Biblioteca `requests`

Puedes instalar la biblioteca `requests` utilizando pip:

```bash
pip install requests

Uso
Clona este repositorio o descarga el archivo pruebas_api.py.

1.- Ejecuta el script desde la línea de comandos:

python pruebas_api.py

2.- Sigue las instrucciones en pantalla para introducir la URL de la API, los headers necesarios y el body en formato JSON.

3.- Selecciona la prueba que deseas realizar a través del menú interactivo.

Pruebas Disponibles
1. Prueba de Autenticación y Autorización
Realiza una prueba de autenticación utilizando una clave API inválida.

2. Prueba de Validación de Entradas
Permite introducir valores no válidos para cada parámetro del payload y muestra la solicitud antes de enviarla.

3. Prueba de Inyección SQL
Permite seleccionar el parámetro y la sentencia SQL a inyectar, mostrando la solicitud antes de enviarla.

4. Mostrar Cabeceras de Respuesta
Muestra las cabeceras de la respuesta y verifica la presencia de cabeceras de seguridad.

5. Prueba de Fuzzing
Permite seleccionar el carácter y el número de repeticiones para la prueba de fuzzing, mostrando la solicitud antes de enviarla.

6. Prueba de Control de Itinerancia
Permite seleccionar el número de solicitudes y el intervalo entre ellas para la prueba de control de itinerancia, mostrando la solicitud antes de enviarla y verificando la presencia de cabeceras de seguridad.

7. Prueba de Verb Tampering
Permite seleccionar el método HTTP a utilizar para probar verb tampering.

8. Salir
Sale del menú interactivo y finaliza el script.

Resultados de las Pruebas
Los resultados de las pruebas se guardarán en un archivo JSON con un nombre basado en la fecha y hora actuales. El archivo incluirá las respuestas y las cabeceras de seguridad faltantes.
