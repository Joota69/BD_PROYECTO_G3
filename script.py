import pymysql
import pyautogui
import random
import time

def conectar_db():
    try:
        connection = pymysql.connect(
            host='127.0.0.1',  # O usa 'localhost'
            user='root',  # Cambia a tu usuario de MySQL
            password='',  # Cambia a tu contraseña de MySQL
            db='comandos_juego',
            port=3306  # Asegúrate de que este es el puerto correcto
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# Función para obtener un comando aleatorio de la base de datos
def obtener_input_db(connection):
    if connection is None:
        print("Conexión a la base de datos fallida.")
        return None

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT accion, COUNT(*) AS veces_repetidas FROM acciones GROUP BY accion ORDER BY veces_repetidas DESC LIMIT 1; ")
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
    except pymysql.MySQLError as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None

# Función para simular el input de teclado
def simular_input():
    connection = conectar_db()  # Intentamos conectar a la base de datos
    tecla = obtener_input_db(connection)
    if tecla:
        pyautogui.press(tecla)
        print(f'Se presionó desde la DB: {tecla}')
    else:
        print('No se encontraron inputs en la base de datos o la conexión falló.')

# Bucle para generar inputs desde la base de datos cada cierto intervalo
def bucle_inputs_desde_db(intervalo=1):
    try:
        while True:
            simular_input()
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")

# Ejecuta el bucle con un intervalo de 1 segundo entre inputs
bucle_inputs_desde_db(intervalo=1)
