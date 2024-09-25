import mysql.connector
import re

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(user="root", password="####",
                                   host="####", database="####",
                                   port="####")
miCursor = conexion.cursor()

# Función para validar el usuario
def validar_usuario(usuario):
    if re.match("^[a-zA-Z0-9]+$", usuario):
        return True
    else:
        return False

usuario = input("Inserta usuario: ")
password = input("Inserta contraseña: ")

# Validar el usuario para que no contenga espacios ni booleanos
if not validar_usuario(usuario):
    print("Error: El nombre de usuario no debe contener espacios y solo puede contener caracteres alfanuméricos.")
else:
    sql = "SELECT * FROM acceso WHERE usuario = %s AND contraseña = %s"

    # Ejecución de la consulta con parámetros seguros
    miCursor.execute(sql, (usuario, password))
    myresult = miCursor.fetchall()
    if myresult:
        for x in myresult:
            print(x)
    else:
        print("No se encontraron resultados.")

# Cerrar el cursor y la conexión
miCursor.close()
conexion.close()
