import keyboard
import time
import mysql.connector

# Función para capturar teclas y enviarlas a la base de datos
def capturar_teclas(rango, id_usuario, puerto):
    teclas_presionadas = []
    teclas_validas = ['w', 'a', 's', 'd', '1']  # Se agregó '1' a las teclas válidas

    # Definir los límites de voto por rango
    if rango == 1:
        limite_votos = 1
    elif rango == 2:
        limite_votos = 5
    elif rango == 3:
        limite_votos = 10
    else:
        print("Rango no válido.")
        return

    votos_realizados = 0

    def registrar_tecla(tecla_evento):
        nonlocal votos_realizados  # Acceder a la variable externa
        if tecla_evento.event_type == keyboard.KEY_DOWN and tecla_evento.name in teclas_validas:
            if votos_realizados < limite_votos:
                teclas_presionadas.append(tecla_evento.name)
                votos_realizados += 1
            else:
                print(f"Has alcanzado el límite de votos para el rango {rango}.")

    print(f"Inicia la captura de teclas (solo w, a, s, d, 1), rango {rango}, tienes 5 segundos...")

    # Inicia la captura de eventos de teclado
    keyboard.hook(registrar_tecla)

    # Espera 5 segundos
    time.sleep(5)

    # Detiene la captura de eventos de teclado
    keyboard.unhook_all()

    # Conexión a la base de datos
    try:
        conexion = mysql.connector.connect(
            host="junction.proxy.rlwy.net",  # Tu host
            user="Florian",  # Tu usuario
            password="1234",  # Tu contraseña
            database="Diagrama_ER_BD",  # El nombre de tu base de datos
            port=puerto  # El puerto que ingrese el usuario
        )

        cursor = conexion.cursor()

        # Verificar si el usuario existe en la tabla Usuarios
        cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE IdUsuario = %s", (id_usuario,))
        resultado = cursor.fetchone()

        if resultado[0] == 0:
            # Insertar el usuario en la tabla Usuarios si no existe
            print(f"El usuario con IdUsuario {id_usuario} no existe. Insertando en la tabla Usuarios...")
            cursor.execute("INSERT INTO Usuarios (IdUsuario) VALUES (%s)", (id_usuario,))
            conexion.commit()

        # Sentencia SQL para insertar cada tecla en la tabla 'Evento'
        for tecla in teclas_presionadas:
            sql = "INSERT INTO Evento (IdUsuario, Tecla) VALUES (%s, %s)"
            valores = (id_usuario, tecla)
            cursor.execute(sql, valores)

        # Confirmar la inserción
        conexion.commit()
        print(f"{cursor.rowcount} teclas insertadas en la base de datos.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Cerrar la conexión
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada.")

    print("Teclas capturadas: ", teclas_presionadas)

# Ejemplo de uso
rango_usuario = int(input("Introduce el rango (1, 2, 3): "))
id_usuario = int(input("Introduce tu IdUsuario: "))
puerto_bd = int(input("Introduce el puerto para la base de datos: "))  # Solicitar el puerto
capturar_teclas(rango_usuario, id_usuario, puerto_bd)
