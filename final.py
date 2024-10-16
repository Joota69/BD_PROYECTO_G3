import pygame
import random
import pymysql
import pygame_gui
import time
from datetime import datetime, timedelta
import pygame.mixer

pygame.init()
pygame.mixer.music.load('plantillas\Audio de WhatsApp 2024-10-15 a las 11.43.18_e27bd3b6.mp3')  # Ruta a tu archivo de música
pygame.mixer.music.set_volume(0.7) 
pygame.mixer.music.play(-1) 

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

grid_size = 80
car_x = 4 * grid_size  # Ajustar la posición inicial del jugador
car_y = 4 * grid_size  # Ajustar la posición inicial del jugador
car_width = grid_size 
car_height = grid_size
velocidad = 40


def conectar_db():
    try:
        connection = pymysql.connect(
            host='junction.proxy.rlwy.net',  
            user='root',
            password='dDiAXNSAWEsOVhDfudxhyuqcfdHNxMog', 
            db='Diagrama_ER_BD',
            port=39036
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        return None
   #########################################################LOGIN#####################################################

def get_votacion_times():
    connection = conectar_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT start_votacion, end_votacion FROM Tiempodevotacion ORDER BY idtiempo DESC LIMIT 1;")
                result = cursor.fetchone()
                if result:
                    start_votacion, end_votacion = result
                    print(f"Tiempos obtenidos: inicio={start_votacion}, fin={end_votacion}")
                    return start_votacion, end_votacion
                else:
                    print("No se encontraron tiempos de votación.")
                    return None, None
        except pymysql.MySQLError as e:
            print(f"Error al obtener tiempos: {e}")
            return None, None
        finally:
            connection.close()
    else:
        print("No se pudo establecer la conexión a la base de datos.")
        return None, None
    


def registrar_eventos(eventos):
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Evento (IdUsuario, Tecla) VALUES (%s, %s)"
            cursor.executemany(sql, eventos)  # Inserta múltiples filas
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
    finally:
        connection.close()
        

def votar():
    eventos = []
    
    # Llamar a "start_voto" para actualizar los tiempos de votación
    connection = conectar_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL start_voto()")
                connection.commit()
                print("Procedimiento `start_voto` ejecutado con éxito.")
        except pymysql.MySQLError as e:
            print(f"Error ejecutando el procedimiento: {e}")
        finally:
            connection.close()
    
    # Ahora obtenemos los tiempos de votación actualizados
    start_votacion, end_votacion = get_votacion_times()
    if not start_votacion or not end_votacion:
        print("No se pudo obtener los tiempos de votación.")
        return
    
    current_time = datetime.now() + timedelta(hours=5)  # Ajustar zona horaria si es necesario
    remaining_time = (end_votacion - current_time).total_seconds()

    if remaining_time <= 0:
        remaining_time = 0
        print("La votación ya ha terminado.")
        return
    
    print(f"Comienza la votación. Tienes {int(remaining_time)} segundos para votar.")
    
    # Tiempo de votación
    start_time = time.time()
    
    while True:
        time_delta = clock.tick(30) / 1000.0
        screen.fill(WHITE)

        # Verificar si el tiempo restante ha terminado
        elapsed_time = time.time() - start_time
        if elapsed_time >= remaining_time:
            print("Tiempo de votación terminado.")
            break

        tecla = input("Ingrese tecla (o 'salir' para terminar la votación): ")
        if tecla == 'salir':
            break
        user_id = input("Ingrese ID de usuario: ")
        
        # Acumula los votos en la lista
        eventos.append((user_id, tecla))

    # Registrar todos los eventos en la base de datos al finalizar
    if eventos:
        registrar_eventos(eventos)
    else:
        print("No se registraron votos.")


def registrar_evento(tecla, user_id):
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO Evento (IdUsuario, Tecla) VALUES ({user_id}, '{tecla}')")
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
    finally:
        connection.close()

def crear_cuenta():
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return None

    running = True
    username = ""
    password = "" 

    screen_width = 900
    screen_height = 800

    # Cargar la imagen de fondo
    fondo = pygame.image.load('pngtree-retro-futuristic-sci-fi-retrowave-vj-videogame-image_13012267.jpg')  # Ruta a tu imagen de fondo
    fondo = pygame.transform.scale(fondo, (screen_width, screen_height))  # Ajustar la imagen al tamaño de la pantalla

    input_width = 300
    input_height = 40
    input_box_username = pygame.Rect((screen_width - input_width) // 2, 300, input_width, input_height)
    input_box_password = pygame.Rect((screen_width - input_width) // 2, 370, input_width, input_height)

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_username = color_inactive
    color_password = color_inactive
    active_username = False
    active_password = False

    # Cambiar tamaño y color del título "Crear Cuenta"
    font = pygame.font.SysFont(None, 65)  # Tamaño del título
    RED = (255, 0, 0)  # Color rojo para el título
    BLACK = (0, 0, 0)  # Color negro para el texto
    GREEN = (0, 255, 0)  # Color verde para el botón "Regresar"

    font_small = pygame.font.SysFont(None, 40)  # Tamaño más pequeño para los textos

    while running:
        screen.blit(fondo, (0, 0))  # Dibujar la imagen de fondo en la pantalla

        # Título "Crear Cuenta" centrado
        mensaje = font.render("Crear Cuenta", True, RED)
        mensaje_rect = mensaje.get_rect(center=(screen_width // 2, 100))
        screen.blit(mensaje, mensaje_rect)

        # Mostrar las etiquetas al lado de los cuadros de entrada
        label_username = font_small.render("Username:", True, BLACK)
        label_password = font_small.render("Password:", True, BLACK)

        # Colocar las etiquetas al lado de los cuadros de entrada
        label_username_rect = label_username.get_rect(midright=(input_box_username.x - 10, input_box_username.centery))
        label_password_rect = label_password.get_rect(midright=(input_box_password.x - 10, input_box_password.centery))

        screen.blit(label_username, label_username_rect)
        screen.blit(label_password, label_password_rect)

        # Dibujar los cuadros de entrada
        pygame.draw.rect(screen, color_username, input_box_username, 2)
        pygame.draw.rect(screen, color_password, input_box_password, 2)

        # Mostrar el texto ingresado en Username y Password dentro de los cuadros
        user_text = font_small.render(username, True, BLACK)  # Mostrar el texto del username
        pass_text = font_small.render('*' * len(password), True, BLACK)  # Mostrar la contraseña como asteriscos

        # Alinear el texto ingresado dentro de los cuadros
        screen.blit(user_text, (input_box_username.x + 10, input_box_username.y + 5))  # Mostrar dentro del cuadro de Username
        screen.blit(pass_text, (input_box_password.x + 10, input_box_password.y + 5))  # Mostrar dentro del cuadro de Password

        # Botón "Regresar" centrado
        regresar_text = font_small.render("Regresar", True, GREEN)
        regresar_rect = regresar_text.get_rect(center=(screen_width // 2, 450))
        screen.blit(regresar_text, regresar_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if active_username:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                if active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode
                if event.key == pygame.K_RETURN:
                    running = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si el usuario hace clic en el cuadro de entrada del nombre de usuario
                if input_box_username.collidepoint(event.pos):
                    active_username = not active_username
                else:
                    active_username = False
                # Si el usuario hace clic en el cuadro de entrada de la contraseña
                if input_box_password.collidepoint(event.pos):
                    active_password = not active_password
                else:
                    active_password = False
                # Cambiar el color de los cuadros de entrada según el enfoque
                color_username = color_active if active_username else color_inactive
                color_password = color_active if active_password else color_inactive

                # Comprobar si el usuario hace clic en el botón "Regresar"
                if regresar_rect.collidepoint(event.pos):
                    return

    selected_rank = select_rank()
    if not selected_rank:
        print("Ningun Rango Seleccionado")
        return None

    # Ensure selected rank is valid
    if selected_rank not in [1, 2, 3]:
        print("Rango seleccionado invalido")
        return None

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM Usuarios WHERE UserName='{username}'")
            if cursor.fetchone():
                print("Username already exists!")
                return None

            # Insert new user into the database
            cursor.execute(f"INSERT INTO Usuarios (UserName, Contraseña, idRango) VALUES ('{username}', '{password}', {selected_rank})")
            connection.commit()
            return username
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None



def login():
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return None

    # Cargar la imagen de fondo
    fondo = pygame.image.load('pngtree-retro-futuristic-sci-fi-retrowave-vj-videogame-image_13012267.jpg')
    fondo = pygame.transform.scale(fondo, (900, 800))  # Ajustar el tamaño de la imagen al tamaño de la pantalla

    running = True
    username = ""
    password = ""

    screen_width = 900
    screen_height = 800

    input_width = 300
    input_height = 40
    input_box_username = pygame.Rect((screen_width - input_width) // 2, 300, input_width, input_height)
    input_box_password = pygame.Rect((screen_width - input_width) // 2, 370, input_width, input_height)

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_username = color_inactive
    color_password = color_inactive
    active_username = False
    active_password = False

    # Cambiar tamaño y color del título "Login"
    font = pygame.font.SysFont(None, 70)  # Hacer el texto más grande
    RED = (255, 0, 0)  # Definir el color rojo para el título "Login"
    
    # Cambiar tamaño y color del texto "Username" y "Password"
    font_small = pygame.font.SysFont(None, 40)  # Hacer el texto más grande
    BLACK = (0, 0, 0)  # Definir el color negro para el texto
    
    # Cambiar color del botón "Crear Cuenta"
    GREEN = (0, 255, 0)  # Definir el color verde para "Crear Cuenta"

    while running:
        screen.blit(fondo, (0, 0))  # Dibujar la imagen de fondo en la pantalla

        # Título "Login"
        mensaje = font.render("Login", True, RED)  # Cambiar el color aquí
        mensaje_rect = mensaje.get_rect(center=(screen_width // 2, 200))  # Centrar el título en la parte superior
        screen.blit(mensaje, mensaje_rect)

        # Mostrar las etiquetas al lado de los cuadros de entrada
        user_label = font_small.render("Username:", True, BLACK)
        pass_label = font_small.render("Password:", True, BLACK)

        # Colocar las etiquetas al lado de los cuadros de entrada
        user_label_rect = user_label.get_rect(midright=(input_box_username.x - 10, input_box_username.centery))
        pass_label_rect = pass_label.get_rect(midright=(input_box_password.x - 10, input_box_password.centery))

        screen.blit(user_label, user_label_rect)
        screen.blit(pass_label, pass_label_rect)

        # Dibujar los cuadros de entrada centrados
        pygame.draw.rect(screen, color_username, input_box_username, 2)
        pygame.draw.rect(screen, color_password, input_box_password, 2)

        # Mostrar el texto ingresado en Username y Password dentro de los cuadros
        user_text = font_small.render(username, True, BLACK)  # Mostrar el texto del username
        pass_text = font_small.render('*' * len(password), True, BLACK)  # Mostrar el texto de la contraseña como asteriscos

        # Alinear el texto ingresado dentro de los cuadros
        screen.blit(user_text, (input_box_username.x + 10, input_box_username.y + 5))  # Mostrar dentro del cuadro de Username
        screen.blit(pass_text, (input_box_password.x + 10, input_box_password.y + 5))  # Mostrar dentro del cuadro de Password

        # Botón "Crear Cuenta" centrado
        crear_cuenta_text = font_small.render("Crear Cuenta", True, GREEN)  # Cambiar el color aquí
        crear_cuenta_rect = crear_cuenta_text.get_rect(center=(screen_width // 2, 450))
        screen.blit(crear_cuenta_text, crear_cuenta_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                # Si el cuadro de texto de username está activo, capturar la entrada
                if active_username:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]  # Eliminar el último carácter
                    else:
                        username += event.unicode  # Añadir el nuevo carácter
                # Si el cuadro de texto de password está activo, capturar la entrada
                if active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]  # Eliminar el último carácter
                    else:
                        password += event.unicode  # Añadir el nuevo carácter
                # Si el usuario presiona Enter, salir del login
                if event.key == pygame.K_RETURN:
                    running = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si el usuario hace clic en el cuadro de entrada del nombre de usuario
                if input_box_username.collidepoint(event.pos):
                    active_username = not active_username
                else:
                    active_username = False
                # Si el usuario hace clic en el cuadro de entrada de la contraseña
                if input_box_password.collidepoint(event.pos):
                    active_password = not active_password
                else:
                    active_password = False
                # Cambiar el color de los cuadros de entrada según el enfoque
                color_username = color_active if active_username else color_inactive
                color_password = color_active if active_password else color_inactive

                # Comprobar si el usuario hace clic en el botón "Crear Cuenta"
                if crear_cuenta_rect.collidepoint(event.pos):
                    crear_cuenta()

    try:
        with connection.cursor() as cursor:
            query = f"SELECT IdUsuario, Contraseña FROM Usuarios WHERE UserName='{username}' AND Contraseña='{password}'"
            cursor.execute(query)
            result = cursor.fetchone()
            if result and result[1] == password:
                return result[0]  # Return User ID
            else:
                return None
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None


def select_rank():
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return None

    running = True
    selected_rank = None
    screen_width = 900
    screen_height = 800

    # Cargar la imagen de fondo
    fondo = pygame.image.load('pngtree-retro-futuristic-sci-fi-retrowave-vj-videogame-image_13012267.jpg')  # Ruta a tu imagen de fondo
    fondo = pygame.transform.scale(fondo, (screen_width, screen_height))  # Ajustar la imagen al tamaño de la pantalla

    font = pygame.font.SysFont(None, 70)  # Fuente para el título
    font_small = pygame.font.SysFont(None, 50)  # Fuente más grande para las opciones
    BLACK = (0, 0, 0)  # Color negro para el texto de las opciones
    RED = (255, 0, 0)  # Color rojo para el título
    WHITE = (255, 255, 255)  # Color blanco para los rectángulos
    BLUE = (0, 0, 255)  # Color azul para los bordes de los rectángulos

    while running:
        screen.blit(fondo, (0, 0))  # Dibujar la imagen de fondo en la pantalla

        # Título "Select Rank" centrado en rojo
        mensaje = font.render("Select Rank", True, RED)
        mensaje_rect = mensaje.get_rect(center=(screen_width // 2, 100))
        screen.blit(mensaje, mensaje_rect)

        # Lista de rangos para seleccionar
        ranks = ["Presione 1: Noob", "Presione 2: Pro", "Presione 3: Hacker"]
        rect_width = 400
        rect_height = 60
        rect_margin = 20  # Espacio entre los rectángulos

        for i, rank in enumerate(ranks):
            # Dibujar un rectángulo detrás de cada opción
            rect_x = (screen_width - rect_width) // 2
            rect_y = 250 + i * (rect_height + rect_margin)  # Espacio entre los rectángulos
            rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            pygame.draw.rect(screen, WHITE, rect)  # Rellenar el rectángulo en blanco
            pygame.draw.rect(screen, BLUE, rect, 5)  # Bordes azules de 5 píxeles de grosor

            # Mostrar el texto de la opción dentro del rectángulo
            rank_text = font_small.render(rank, True, BLACK)
            rank_text_rect = rank_text.get_rect(center=rect.center)  # Centrar el texto dentro del rectángulo
            screen.blit(rank_text, rank_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_rank = 1 
                    running = False
                elif event.key == pygame.K_2:
                    selected_rank = 2  
                    running = False
                elif event.key == pygame.K_3:
                    selected_rank = 3  
                    running = False

    return selected_rank




                                ##############################Juego#######################################


def crear_matriz(filas, columnas):
    return [[0 for _ in range(columnas)] for _ in range(filas)]

def actualizar_matriz(matriz, obstaculos, valor):
    filas = len(matriz)
    columnas = len(matriz[0])
    for obstaculo in obstaculos:
        x, y = int(obstaculo[0] // grid_size), int(obstaculo[1] // grid_size)
        if 0 <= x < columnas and 0 <= y < filas:
            matriz[y][x] = valor


def seleccionar_modo():
    running = True
    modo = None
    screen_width = 900
    screen_height = 800

    # Cargar la imagen de fondo
    fondo = pygame.image.load('pngtree-retro-futuristic-sci-fi-retrowave-vj-videogame-image_13012267.jpg')  # Ruta a tu imagen de fondo
    fondo = pygame.transform.scale(fondo, (screen_width, screen_height))  # Ajustar la imagen al tamaño de la pantalla

    font = pygame.font.SysFont(None, 70)  # Fuente para el título
    font_small = pygame.font.SysFont(None, 50)  # Fuente para las opciones
    BLACK = (0, 0, 0)  # Color negro para el texto de las opciones
    RED = (255, 0, 0)  # Color rojo para el título
    WHITE = (255, 255, 255)  # Color blanco para los rectángulos
    BLUE = (0, 0, 255)  # Color azul para los bordes de los rectángulos

    while running:
        screen.blit(fondo, (0, 0))  # Dibujar la imagen de fondo en la pantalla

        # Título "Seleccionar Modo" centrado en rojo
        mensaje = font.render("Seleccionar Modo", True, RED)
        mensaje_rect = mensaje.get_rect(center=(screen_width // 2, 100))
        screen.blit(mensaje, mensaje_rect)

        # Opciones de modo para seleccionar
        modos = ["1. Visualizar", "2. Jugar"]
        rect_width = 400
        rect_height = 60
        rect_margin = 20  # Espacio entre los rectángulos

        for i, modo_texto in enumerate(modos):
            # Dibujar un rectángulo detrás de cada opción
            rect_x = (screen_width - rect_width) // 2
            rect_y = 250 + i * (rect_height + rect_margin)  # Espacio entre los rectángulos
            rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            pygame.draw.rect(screen, WHITE, rect)  # Rellenar el rectángulo en blanco
            pygame.draw.rect(screen, BLUE, rect, 5)  # Bordes azules de 5 píxeles de grosor

            # Mostrar el texto de la opción dentro del rectángulo
            modo_text = font_small.render(modo_texto, True, BLACK)
            modo_text_rect = modo_text.get_rect(center=rect.center)  # Centrar el texto dentro del rectángulo
            screen.blit(modo_text, modo_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    modo = "visualizar"
                    running = False
                elif event.key == pygame.K_2:
                    modo = "jugar"
                    pygame.mixer.music.set_volume(0.1)
                    running = False

    return modo




####################################################Juego#######################################################################
def start_game():
    global votaciones
    
    user_id = None
    while not user_id:
        user_id = login()

    # Inicializa los valores de `id_jugador` y `tecla_ganadora_orden`
    id_jugador = None  # Puedes obtener este valor más adelante
    tecla_ganadora_orden = None  # O obtener este valor después
    
    votaciones = 0  # Resetear el contador de votaciones

    while True:
        modo = seleccionar_modo()
        if modo == "visualizar":
            visualizar_juego()
        elif modo == "jugar":
            # Llamar al procedimiento almacenado `start_voto` al seleccionar "Jugar"
            connection = conectar_db()
            if connection is None:
                print("No se pudo establecer la conexión a la base de datos.")
                return

            try:
                with connection.cursor() as cursor:
                    # Ejecutar el procedimiento almacenado `start_voto`
                    cursor.execute("CALL start_voto()")
                    connection.commit()  # Confirmar cambios
                    print("Procedimiento almacenado `start_voto` ejecutado con éxito al seleccionar 'Jugar'.")
            except pymysql.MySQLError as e:
                print(f"Error al ejecutar el procedimiento almacenado: {e}")
            finally:
                connection.close()

            if id_jugador is None:
                id_jugador = user_id  # O de donde corresponda
            if tecla_ganadora_orden is None:
                tecla_ganadora_orden = 1  # O algún valor válido
            juego(user_id, id_jugador, tecla_ganadora_orden)  # Pasar los tres argumentos


def visualizar_juego():
    global car_x, car_y

    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT x, y FROM Jugador Limit 1")
            result = cursor.fetchone()
            if result:
                car_x = (result[0] - 1) * grid_size  # Ajustar según la cuadrícula
                car_y = (result[1] - 1) * grid_size  # Ajustar según la cuadrícula
            else:
                car_x = 4 * grid_size  # Valor por defecto si no hay registros
                car_y = 4 * grid_size  # Valor por defecto si no hay registros
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return
    finally:
        connection.close()

    tiempo_total = 0
    tiempo_envio = 0
    running = True
    crear_obstaculos()

    manager = pygame_gui.UIManager((900, 800))
    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((750, 10), (140, 50)),
                                               text='Regresar',
                                               manager=manager)

    area_exclusion = pygame.Rect(700, 0, 200, 800)

    filas, columnas = 10, 8  # Ajustar según el tamaño del mapa
    matriz = crear_matriz(filas, columnas)

    while running:
        time_delta = clock.tick(40) / 1000.0
        screen.fill(WHITE)
        dibujar_cuadricula()  # Dibujar la cuadrícula

        pygame.draw.line(screen, BLACK, (700, 0), (700, 800), 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        seleccionar_modo()
                        return

            manager.process_events(event)

        pygame.draw.rect(screen, RED, (car_x, car_y, car_width, car_height))

        tiempo_total += 1

        manejar_movimiento_obstaculos(tiempo_total)

        actualizar_matriz(matriz, obstaculos_verticales, 0)
        actualizar_matriz(matriz, obstaculos_horizontales, 0)

        for obstaculo in obstaculos_verticales:
            if not area_exclusion.colliderect(pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3])):
                pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

            if (car_y < obstaculo[1] + obstaculo[3] and
                car_y + grid_size > obstaculo[1] and
                car_x < obstaculo[0] + obstaculo[2] and
                car_x + grid_size > obstaculo[0]):
                print("¡Choque!")
                mostrar_pantalla_reinicio(None)
                running = False

        for obstaculo in obstaculos_horizontales:
            if not area_exclusion.colliderect(pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3])):
                pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

            if (car_y < obstaculo[1] + obstaculo[3] and
                car_y + grid_size > obstaculo[1] and
                car_x < obstaculo[0] + obstaculo[2] and
                car_x + grid_size > obstaculo[0]):
                print("¡Choque!")
                mostrar_pantalla_reinicio(None)
                running = False

        actualizar_matriz(matriz, obstaculos_verticales, 1)
        actualizar_matriz(matriz, obstaculos_horizontales, 1)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()
    
    connection.close()

# Cambiar las dimensiones del mapa en visualizar_juego
# Cambiar las dimensiones del mapa en visualizar_juego
def guardar_obstaculos_db():
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return

    try:
        with connection.cursor() as cursor:
            for i, obstaculo in enumerate(obstaculos_verticales + obstaculos_horizontales):
                tipo = 'vertical' if obstaculo in obstaculos_verticales else 'horizontal'
                x_celda = obstaculo[0] // grid_size
                y_celda = obstaculo[1] // grid_size
                cursor.execute(f"UPDATE Obstaculos SET x = {x_celda}, y = {y_celda}, tipo = '{tipo}' WHERE idObstaculos = {i + 1}")
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
    finally:
        connection.close()

def leer_obstaculos_db():
    global obstaculos_verticales, obstaculos_horizontales
    obstaculos_verticales = []
    obstaculos_horizontales = []

    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT x, y, tipo FROM Obstaculos")
            for row in cursor.fetchall():
                x_celda, y_celda, tipo = row
                x = x_celda * grid_size
                y = y_celda * grid_size
                if tipo == 'vertical':
                    obstaculos_verticales.append([x, y, grid_size, grid_size, grid_size / 10, 0])
                else:
                    obstaculos_horizontales.append([x, y, grid_size, grid_size, grid_size / 10, 0])
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
    finally:
        connection.close()

def crear_obstaculos():
    global obstaculos_verticales, obstaculos_horizontales
    leer_obstaculos_db()
    if not obstaculos_verticales and not obstaculos_horizontales:
        # Si no hay obstáculos en la base de datos, crear nuevos obstáculos y guardarlos
        obstaculos_verticales = [
            [1 * grid_size, 1 * grid_size, grid_size, grid_size, grid_size / 10, 0],
            [3 * grid_size, 2 * grid_size, grid_size, grid_size, grid_size / 10, 0],
            [5 * grid_size, 4 * grid_size, grid_size, grid_size, grid_size / 10, 0],
            [7 * grid_size, 6 * grid_size, grid_size, grid_size, grid_size / 10, 0]
        ]
        obstaculos_horizontales = [
            [2 * grid_size, 1 * grid_size, grid_size, grid_size, grid_size / 10, 0],
            [4 * grid_size, 3 * grid_size, grid_size, grid_size, grid_size / 10, 0],
            [6 * grid_size, 5 * grid_size, grid_size, grid_size, grid_size / 10, 0],
            [8 * grid_size, 7 * grid_size, grid_size, grid_size, grid_size / 10, 0]
        ]
        guardar_obstaculos_db()

def dibujar_obstaculos():
    global obstaculos_verticales, obstaculos_horizontales
    for obstaculo in obstaculos_verticales:
        pygame.draw.rect(screen, RED, obstaculo)
    for obstaculo in obstaculos_horizontales:
        pygame.draw.rect(screen, RED, obstaculo)

def mover_obstaculos(obstaculos, direccion):
    for obstaculo in obstaculos:
        if direccion == 'vertical':
            obstaculo[1] += grid_size
            if obstaculo[1] >= 800:
                obstaculo[1] = random.randint(-20, -2) * grid_size
        elif direccion == 'horizontal':
            obstaculo[0] += grid_size
            if obstaculo[0] >= 700:
                obstaculo[0] = random.randint(-20, -2) * grid_size

def manejar_movimiento_obstaculos(tiempo_total):
    if tiempo_total % 10 == 0:  # Ajustar la frecuencia del movimiento
        for obstaculo in obstaculos_verticales:
            obstaculo[1] += grid_size  # Mover obstáculo verticalmente en incrementos de grid_size
            if obstaculo[1] >= 800:  # Si el obstáculo sale de la pantalla, reiniciar su posición
                obstaculo[1] = 0
        for obstaculo in obstaculos_horizontales:
            obstaculo[0] += grid_size  # Mover obstáculo horizontalmente en incrementos de grid_size
            if obstaculo[0] >= 700:  # Si el obstáculo sale de la pantalla, reiniciar su posición
                obstaculo[0] = 0
        guardar_obstaculos_db()  # Guardar las posiciones actualizadas en la base de datos



def actualizar_posicion_jugador(user_id, x, y):
    print(f"Actualizando posición: IdJugador={user_id}, x={x}, y={y}")
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO Jugador (IdJugador, x, y) 
                VALUES ({user_id}, {x}, {y})
                ON DUPLICATE KEY UPDATE x = VALUES(x), y = VALUES(y)
            """)
            connection.commit()
            print("Inserción/Actualización exitosa")
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
    finally:
        connection.close()

def imprimir_posicion_carro(user_id):
    x_cuadricula = (car_x // grid_size) + 1
    y_cuadricula = (car_y // grid_size) + 1
    print(f"Posición del carro: x={x_cuadricula}, y={y_cuadricula}")
    actualizar_posicion_jugador(user_id, x_cuadricula, y_cuadricula)

def mover_carro(letra):
    global car_x, car_y
    if letra == "A" and car_x > 0:
        car_x -= grid_size
    elif letra == "D" and car_x < 660:
        car_x += grid_size
    elif letra == "W" and car_y > 0:
        car_y -= grid_size
    elif letra == "S" and car_y < 700:
        car_y += grid_size



def mostrar_pantalla_reinicio(user_id):
    global votaciones
    # Registrar la partida en la base de datos
    
    # Nueva conexión para ejecutar tiempofinal()
    connection = conectar_db()
    if connection:
        try:
            print("Enviando tiempo final a la base de datos")
            with connection.cursor() as cursor:
                cursor.execute("CALL tiempofinal() ")  # Llamar al procedimiento almacenado
                connection.commit()  # Asegurarse de que los cambios se guarden
                
                cursor.execute("CALL SPtiempo_total()")
                connection.commit()  # Confirmar cambios en la base de datos
                
                cursor.execute("CALL actualizarvotos(%s)", (votos_realizados,))
                connection.commit()
                
                cursor.execute("CALL operacionpuntuacion()")
                connection.commit()
                   
        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")
        finally:
            connection.close()
    registrar_partida()  
    resetear_posiciones()

    screen.fill(WHITE)
    fuente = pygame.font.SysFont(None, 55)
    mensaje = fuente.render("¡Perdiste!", True, BLACK)
    boton = fuente.render("Reiniciar", True, BLACK)
    screen.blit(mensaje, (120, 200))
    screen.blit(boton, (120, 300))
    pygame.display.update()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 120 <= mouse_x <= 280 and 300 <= mouse_y <= 355:
                    esperando = False
                    reiniciar_juego(user_id)
    resetear_posiciones()
    
    

def resetear_posiciones():
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return

    try:
        with connection.cursor() as cursor:
            # Actualizar los obstáculos a posiciones en los bordes del área de juego
            cursor.execute("UPDATE Obstaculos SET x = CASE idObstaculos "
                           "WHEN 1 THEN 0 "  # Borde izquierdo
                           "WHEN 2 THEN 7 "  # Borde derecho
                           "WHEN 3 THEN 0 "  # Borde izquierdo
                           "WHEN 4 THEN 7 END, "  # Borde derecho
                           "y = CASE idObstaculos "
                           "WHEN 1 THEN 0 "  # Borde superior
                           "WHEN 2 THEN 0 "  # Borde superior
                           "WHEN 3 THEN 7 "  # Borde inferior
                           "WHEN 4 THEN 7 END "  # Borde inferior
                           "WHERE idObstaculos IN (1, 2, 3, 4)")

            # Actualizar la posición del jugador a su posición original
            cursor.execute("UPDATE Jugador SET x = 4, y = 4 WHERE IdJugador = 1")

            connection.commit()  # Confirmar los cambios
            print("Posiciones de obstáculos y jugador reseteadas a sus valores originales.")
    except pymysql.MySQLError as e:
        print(f"Error ejecutando la consulta: {e}")
    finally:
        connection.close()

def registrar_partida():
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return
    try:
        with connection.cursor() as cursor:
            # Obtener el valor actual de la tecla ganadora
            cursor.execute("CALL historialpartida()")
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error ejecutando la consulta: {e}")
    finally:
        connection.close()



def reiniciar_juego(user_id):
    global car_x, car_y
    car_x = 4 * grid_size
    car_y = 4 * grid_size
    crear_obstaculos()  

    # Necesitas obtener o pasar los valores correctos de id_jugador y tecla_ganadora_orden
    id_jugador = user_id  # Asegúrate de que este valor esté disponible
    tecla_ganadora_orden = 1  # O usa el valor adecuado que corresponda en tu lógica
    
    # Llama a juego con los tres argumentos correctos
    juego(user_id, id_jugador, tecla_ganadora_orden)
    

def dibujar_botones(manager):
    botones = {
        "A": (750, 300),
        "W": (800, 250),
        "S": (800, 300),
        "D": (850, 300)
    }
    for letra, pos in botones.items():
        button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(pos[0], pos[1], 50, 50),
                                              text=letra,
                                              manager=manager)



def manejar_movimiento_obstaculos(tiempo_total):
    if tiempo_total % 10 == 0:  # Ajustar la frecuencia del movimiento
        for obstaculo in obstaculos_verticales:
            obstaculo[1] += grid_size  # Mover obstáculo verticalmente en incrementos de grid_size
            if obstaculo[1] >= 800:  # Si el obstáculo sale de la pantalla, reiniciar su posición
                obstaculo[1] = 0
        for obstaculo in obstaculos_horizontales:
            obstaculo[0] += grid_size  # Mover obstáculo horizontalmente en incrementos de grid_size
            if obstaculo[0] >= 700:  # Si el obstáculo sale de la pantalla, reiniciar su posición
                obstaculo[0] = 0
        guardar_obstaculos_db()  # Guardar las posiciones actualizadas en la base de datos


def mover_carro(letra):
    print(f"Moviendo el carro con la tecla: {letra}")
    global car_x, car_y, votos_realizados
    if letra == "A" and car_x > 0:
        car_x -= grid_size
        votos_realizados += 1
    elif letra == "D" and car_x < 660:
        car_x += grid_size
        votos_realizados += 1
    elif letra == "W" and car_y > 0:
        car_y -= grid_size
        votos_realizados += 1
    elif letra == "S" and car_y < 700:
        car_y += grid_size
        votos_realizados += 1
    

def dibujar_cuadricula():
    for x in range(0, 700, grid_size):
        pygame.draw.line(screen, GRAY, (x, 0), (x, 800))
    for y in range(0, 800, grid_size):
        pygame.draw.line(screen, GRAY, (0, y), (700, y))

def juego(user_id, id_jugador, tecla_ganadora_orden):
    global car_x, car_y
    # Nueva conexión para ejecutar tiempoinicial()
    connection = conectar_db()
    if connection:
        try:
            print("Enviando tiempo inicial a la base de datos")
            with connection.cursor() as cursor:
                cursor.execute("CALL tiempoinicial() ")  # Llamar al procedimiento almacenado
                
                connection.commit()  # Asegurarse de que los cambios se guarden
        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")
        finally:
            connection.close()


    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT x, y FROM Jugador LIMIT 1")
            result = cursor.fetchone()
            if result:
                car_x = (result[0] - 1) * grid_size  # Ajustar según la cuadrícula
                car_y = (result[1] - 1) * grid_size  # Ajustar según la cuadrícula
            else:
                car_x = 4 * grid_size  # Valor por defecto si no hay registros
                car_y = 4 * grid_size  # Valor por defecto si no hay registros
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return
    finally:
        connection.close()  # Cerramos la conexión después de cargar la posición del jugador

    tiempo_total = 0
    tiempo_envio = 0  # Variable para rastrear el tiempo transcurrido para el envío
    running = True
    crear_obstaculos()

    # Para recopilar votos
    votos = []  # Lista para almacenar los votos
    start_votacion, end_votacion = get_votacion_times()
    current_time = datetime.now() + timedelta(hours=5)
    remaining_time = (end_votacion - current_time).total_seconds()
    tiempo_inicio_votacion = time.time() # Tiempo de inicio de la votación

    manager = pygame_gui.UIManager((900, 800))
    dibujar_botones(manager)

    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((750, 10), (140, 50)),
                                               text='Regresar',
                                               manager=manager)

    area_botones = [
        pygame.Rect(750, 300, 50, 50),
        pygame.Rect(800, 250, 50, 50),
        pygame.Rect(800, 300, 50, 50),
        pygame.Rect(850, 300, 50, 50)
    ]

    area_exclusion = pygame.Rect(700, 0, 200, 800)

    filas, columnas = 10, 8  # (debo cambiarlo)
    matriz = crear_matriz(filas, columnas)

    while running:
        time_delta = clock.tick(30) / 1000.0
        screen.fill(WHITE)
        dibujar_cuadricula()  # Dibujar la cuadrícula

        pygame.draw.line(screen, BLACK, (700, 0), (700, 800), 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        seleccionar_modo()
                        return
                    # Aquí se registra el voto
                    votos.append(event.ui_element.text)  # Acumular el voto en la lista
                    print(f"Voto registrado: {event.ui_element.text}")  # Imprimir voto en la consola

            manager.process_events(event)

        pygame.draw.rect(screen, RED, (car_x, car_y, grid_size, grid_size))

        tiempo_total += 1
        tiempo_envio += time_delta  # Incrementar el tiempo transcurrido para el envío

        manejar_movimiento_obstaculos(tiempo_total)

        actualizar_matriz(matriz, obstaculos_verticales, 0)
        actualizar_matriz(matriz, obstaculos_horizontales, 0)

        for obstaculo in obstaculos_verticales:
            if not area_exclusion.colliderect(pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3])):
                pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

            if (car_y < obstaculo[1] + obstaculo[3] and
                car_y + grid_size > obstaculo[1] and
                car_x < obstaculo[0] + obstaculo[2] and
                car_x + grid_size > obstaculo[0]):
                print("¡Choque!")
                mostrar_pantalla_reinicio(user_id)
                running = False

        for obstaculo in obstaculos_horizontales:
            if not area_exclusion.colliderect(pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3])):
                pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

            if (car_y < obstaculo[1] + obstaculo[3] and
                car_y + grid_size > obstaculo[1] and
                car_x < obstaculo[0] + obstaculo[2] and
                car_x + grid_size > obstaculo[0]):
                print("¡Choque!")
                mostrar_pantalla_reinicio(user_id, id_jugador, tecla_ganadora_orden)
                running = False

        actualizar_matriz(matriz, obstaculos_verticales, 1)
        actualizar_matriz(matriz, obstaculos_horizontales, 1)

        # Verificar si han pasado 20 segundos para enviar los votos
        if (time.time() - tiempo_inicio_votacion) >= (remaining_time):
            print(f"Hora actual: {current_time}")
            print(f"Hora de inicio de votación: {start_votacion}")
            print(f"Hora de fin de votación: {end_votacion}")
            print(f"Tiempo restante para votar: {remaining_time} segundos")

            print("Tiempo de votación terminado. Enviando votos a la base de datos.")
            if votos:  # Solo registrar si hay votos
                registrar_eventos([(user_id, voto) for voto in votos])  # Registrar todos los votos en la base de datos

                # Nueva conexión para ejecutar ObtenerTeclaGanadora()
                connection = conectar_db()
                if connection:
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute("CALL ObtenerTeclaGanadora() ")  # Llamar al procedimiento almacenado
                            connection.commit()  # Asegurarse de que los cambios se guarden

                            cursor.execute("SELECT nk FROM Tecla_ganadora ORDER BY Orden DESC LIMIT 1")
                            result = cursor.fetchone()
                            if result:
                                tecla_ganadora = result[0]
                                print(f'Tecla ganadora es:{tecla_ganadora}')
                                mover_carro(tecla_ganadora)
                            else:
                                print("No se encontró ninguna tecla ganadora.")
                    except pymysql.MySQLError as e:
                        print(f"Error executing query: {e}")
                    finally:
                        connection.close()
            else:
                print("No se registraron votos.")

            # Reiniciar la votación
            votos.clear()  # Limpiar la lista de votos
            tiempo_inicio_votacion = time.time() # Reiniciar el tiempo de votacion
            start_votacion, end_votacion = get_votacion_times() # Obtener nuevo tiempo de votacion

        # Enviar posición del carro a la base de datos cada 4 segundos
        if tiempo_envio >= 5:  # Verificar si han pasado 4 segundos
            print("Enviando posición del carro a la base de datos")
            imprimir_posicion_carro(user_id)  # Enviar la posición del carro rojo a la base de datos
            tiempo_envio = 0  # Reiniciar el temporizador

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()


# Definiciones de variables y funciones auxiliares
votaciones = 0
votos_realizados = 0
obstaculos_verticales = []
obstaculos_horizontales = []
clock = pygame.time.Clock()
screen = pygame.display.set_mode((900, 800))
pygame.display.set_caption("PROYECTO")

# Inicia el juego
start_game()
pygame.quit()
