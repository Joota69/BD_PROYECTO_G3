import mysql.connector
import time
from datetime import datetime

# Conectar a la base de datos MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='junction.proxy.rlwy.net',  
            user='root',
            password='dDiAXNSAWEsOVhDfudxhyuqcfdHNxMog', 
            db='Diagrama_ER_BD',
            port=39036  
        )
        if connection.is_connected():
            print("Conexión establecida correctamente.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error al conectar: {err}")
        return None

# Función para obtener los tiempos de inicio y fin de votación
def get_votacion_times():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute('call start_voto;')
        cursor.execute("SELECT start_votacion, end_votacion FROM Tiempodevotacion ORDER BY idtiempo DESC LIMIT 1;")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            start_votacion, end_votacion = result
            print(f"Tiempo de inicio de votación: {start_votacion}")
            print(f"Tiempo de fin de votación: {end_votacion}")
            return start_votacion, end_votacion
        else:
            print("No se encontraron tiempos de votación.")
            return None, None
    else:
        print("No se pudo establecer la conexión a la base de datos.")
        return None, None

# Función para llamar al procedimiento almacenado
def start_voto():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute('call start_voto;')
        connection.commit()
        cursor.close()
        connection.close()
        print("Procedimiento almacenado start_voto ejecutado.")

# Función principal para monitorear el tiempo y ejecutar el procedimiento almacenado infinitamente
def monitor_votacion():
    while True:
        _, end_votacion = get_votacion_times()
        if end_votacion:
            while True:
                current_time = datetime.now()
                # Compara la hora actual con el tiempo de fin de votación
                if current_time >= end_votacion:
                    start_voto()
                    print(f"Procedimiento ejecutado a las: {datetime.now()}")
                    break
                # Esperar un segundo antes de volver a comprobar
                time.sleep(1)
        else:
            print("No se pudo obtener el tiempo de fin de votación.")
        # Espera 1 segundo antes de volver a consultar los tiempos y repetir el proceso
        time.sleep(1)

if __name__ == "__main__":
    monitor_votacion()
