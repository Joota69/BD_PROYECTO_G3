import pygame
import random
import pymysql
import pygame_gui
import time
from datetime import datetime, timedelta

pygame.init()

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
        cursor = connection.cursor()
        cursor.execute("SELECT start_votacion, end_votacion FROM Tiempodevotacion ORDER BY idtiempo DESC LIMIT 1;")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            start_votacion, end_votacion = result
            return start_votacion, end_votacion
        else:
            print("No se encontraron tiempos de votación.")
            return None, None
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

def votar(user_id):
    eventos = []
    start_votacion, end_votacion = get_votacion_times()
    
    if not start_votacion or not end_votacion:
        print("No se pudo obtener los tiempos de votación.")
        return

    # Obtener el tiempo actual y calcular el tiempo restante para votar
    current_time = datetime.now() + timedelta(hours=5)
    remaining_time = (end_votacion - current_time).total_seconds()
    
    if remaining_time <= 0:
        print("La votación ya ha terminado.")
        return

    print(f"Comienza la votación. Tienes {int(remaining_time)} segundos para votar.")
    
    # Tiempo de votación basado en el tiempo faltante
    start_time = time.time()

    # Interface buttons for voting
    manager = pygame_gui.UIManager((900, 800))
    button_a = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((750, 300), (50, 50)),
                                            text='A',
                                            manager=manager)
    button_w = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((800, 250), (50, 50)),
                                            text='W',
                                            manager=manager)
    button_s = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((800, 300), (50, 50)),
                                            text='S',
                                            manager=manager)
    button_d = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((850, 300), (50, 50)),
                                            text='D',
                                            manager=manager)

    while True:
        time_delta = clock.tick(30) / 1000.0
        screen.fill(WHITE)

        # Verificar si el tiempo restante ha terminado
        elapsed_time = time.time() - start_time
        if elapsed_time >= remaining_time:
            print("Tiempo de votación terminado.")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    # Registrar el voto en la lista
                    eventos.append((user_id, event.ui_element.text))
                    print(f"Voto registrado: {event.ui_element.text}")

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()

    # Registrar los votos al final
    if eventos:
        registrar_eventos(eventos)
        print("Votos registrados.")
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
    focus = "username"  

    input_box_username = pygame.Rect(226, 191, 140, 32)
    input_box_password = pygame.Rect(220, 242, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_username = color_inactive
    color_password = color_inactive
    active_username = False
    active_password = False

    while running:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 55)
        mensaje = font.render("Crear Cuenta", True, BLACK)
        screen.blit(mensaje, (120, 100))

        font_small = pygame.font.SysFont(None, 30)
        label_username = font_small.render("Username:", True, BLACK)
        label_password = font_small.render("Password:", True, BLACK)
        user_text = font_small.render(username, True, BLACK)
        pass_text = font_small.render('*' * len(password), True, BLACK)
        
        # Render the labels and current text.
        screen.blit(label_username, (120, 200))
        screen.blit(label_password, (120, 250))
        screen.blit(user_text, (input_box_username.x+5, input_box_username.y+5))
        screen.blit(pass_text, (input_box_password.x+5, input_box_password.y+5))
        
        # Draw the input boxes.
        pygame.draw.rect(screen, color_username, input_box_username, 2)
        pygame.draw.rect(screen, color_password, input_box_password, 2)

        regresar_text = font_small.render("Regresar", True, BLACK)
        screen.blit(regresar_text, (120, 300))
        
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
                # If the user clicked on the input_box_username rect.
                if input_box_username.collidepoint(event.pos):
                    active_username = not active_username
                else:
                    active_username = False
                # If the user clicked on the input_box_password rect.
                if input_box_password.collidepoint(event.pos):
                    active_password = not active_password
                else:
                    active_password = False
                # Change the current color of the input boxes.
                color_username = color_active if active_username else color_inactive
                color_password = color_active if active_password else color_inactive

                if 120 <= event.pos[0] <= 280 and 300 <= event.pos[1] <= 330:
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
    
    running = True
    username = ""
    password = ""
    focus = "username"  

    input_box_username = pygame.Rect(226, 191, 140, 32)
    input_box_password = pygame.Rect(221, 242, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_username = color_inactive
    color_password = color_inactive
    active_username = False
    active_password = False

    while running:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 55)
        mensaje = font.render("Login", True, BLACK)
        screen.blit(mensaje, (120, 100))

        font_small = pygame.font.SysFont(None, 30)
        user_text = font_small.render(f"Username: {username}", True, BLACK)
        pass_text = font_small.render(f"Password: {'*' * len(password)}", True, BLACK)

        screen.blit(user_text, (120, 200))
        screen.blit(pass_text, (120, 250))
        
        pygame.draw.rect(screen, color_username, input_box_username, 2)
        pygame.draw.rect(screen, color_password, input_box_password, 2)

        # Botón para crear cuenta
        crear_cuenta_text = font_small.render("Crear Cuenta", True, BLACK)
        screen.blit(crear_cuenta_text, (120, 300))
        
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
                # If the user clicked on the input_box_username rect.
                if input_box_username.collidepoint(event.pos):
                    active_username = not active_username
                else:
                    active_username = False
                # If the user clicked on the input_box_password rect.
                if input_box_password.collidepoint(event.pos):
                    active_password = not active_password
                else:
                    active_password = False
                # Change the current color of the input boxes.
                color_username = color_active if active_username else color_inactive
                color_password = color_active if active_password else color_inactive
                # Check if the user clicked on the "Crear Cuenta" button.
                if 120 <= event.pos[0] <= 280 and 300 <= event.pos[1] <= 330:
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

    while running:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 55)
        mensaje = font.render("Select Rank", True, BLACK)
        screen.blit(mensaje, (120, 100))

        font_small = pygame.font.SysFont(None, 30)
        ranks = ["Preione 1: Noob", "Presione 2: Pro", "Presione 3: Hacker"]
        for i, rank in enumerate(ranks):
            rank_text = font_small.render(rank, True, BLACK)
            screen.blit(rank_text, (120, 200 + i * 50))

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

# ############################################ Juego #######################################
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

    while running:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 55)
        mensaje = font.render("Seleccionar Modo", True, BLACK)
        screen.blit(mensaje, (120, 100))

        font_small = pygame.font.SysFont(None, 30)
        modo_texto_1 = font_small.render("1. Visualizar", True, BLACK)
        modo_texto_2 = font_small.render("2. Jugar", True, BLACK)
        screen.blit(modo_texto_1, (120, 200))
        screen.blit(modo_texto_2, (120, 250))

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
                    running = False

    return modo

# ########################################### Votación y juego #######################################
def start_game():
    global votaciones
    
    user_id = None
    while not user_id:
        user_id = login()

    votaciones = 0  # Resetear el contador de votaciones

    while True:
        modo = seleccionar_modo()
        if modo == "visualizar":
            visualizar_juego()
        elif modo == "jugar":
            juego(user_id)

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
    running = True
    crear_obstaculos()

    manager = pygame_gui.UIManager((900, 800))
    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((750, 10), (140, 50)),
                                               text='Regresar',
                                               manager=manager)

    while running:
        time_delta = clock.tick(40) / 1000.0
        screen.fill(WHITE)
        dibujar_cuadricula()

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

        manejar_movimiento_obstaculos(tiempo_total)
        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()
    
    connection.close()

def crear_obstaculos():
    global obstaculos_verticales, obstaculos_horizontales
    obstaculos_verticales = [
        [1 * grid_size, 1 * grid_size, grid_size, grid_size],
        [3 * grid_size, 2 * grid_size, grid_size, grid_size],
        [5 * grid_size, 4 * grid_size, grid_size, grid_size],
        [7 * grid_size, 6 * grid_size, grid_size, grid_size]
    ]
    obstaculos_horizontales = [
        [2 * grid_size, 1 * grid_size, grid_size, grid_size],
        [4 * grid_size, 3 * grid_size, grid_size, grid_size],
        [6 * grid_size, 5 * grid_size, grid_size, grid_size],
        [8 * grid_size, 7 * grid_size, grid_size, grid_size]
    ]

def manejar_movimiento_obstaculos(tiempo_total):
    if tiempo_total % 10 == 0:  # Ajustar la frecuencia del movimiento
        for obstaculo in obstaculos_verticales:
            obstaculo[1] += grid_size
            if obstaculo[1] >= 800:
                obstaculo[1] = 0
        for obstaculo in obstaculos_horizontales:
            obstaculo[0] += grid_size
            if obstaculo[0] >= 700:
                obstaculo[0] = 0

def juego(user_id):
    global car_x, car_y
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT x, y FROM Jugador LIMIT 1")
            result = cursor.fetchone()
            if result:
                car_x = (result[0] - 1) * grid_size
                car_y = (result[1] - 1) * grid_size
            else:
                car_x = 4 * grid_size
                car_y = 4 * grid_size
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return
    finally:
        connection.close()

    tiempo_total = 0
    running = True
    crear_obstaculos()

    # Para recopilar votos
    votos = []  
    tiempo_votacion = 6  
    tiempo_inicio_votacion = pygame.time.get_ticks() 

    manager = pygame_gui.UIManager((900, 800))
    dibujar_botones(manager)

    while running:
        time_delta = clock.tick(30) / 1000.0
        screen.fill(WHITE)
        dibujar_cuadricula()

        pygame.draw.line(screen, BLACK, (700, 0), (700, 800), 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    votos.append(event.ui_element.text)
                    print(f"Voto registrado: {event.ui_element.text}")

            manager.process_events(event)

        pygame.draw.rect(screen, RED, (car_x, car_y, grid_size, grid_size))

        tiempo_total += 1
        manejar_movimiento_obstaculos(tiempo_total)

        if (pygame.time.get_ticks() - tiempo_inicio_votacion) >= (tiempo_votacion * 1000):
            print("Tiempo de votación terminado. Enviando votos a la base de datos.")
            if votos:
                registrar_eventos([(user_id, voto) for voto in votos])
            else:
                print("No se registraron votos.")

            votos.clear()  
            tiempo_inicio_votacion = pygame.time.get_ticks()  

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()

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

def dibujar_cuadricula():
    for x in range(0, 700, grid_size):
        pygame.draw.line(screen, GRAY, (x, 0), (x, 800))
    for y in range(0, 800, grid_size):
        pygame.draw.line(screen, GRAY, (0, y), (700, y))

# Definiciones de variables y funciones auxiliares
votaciones = 0
clock = pygame.time.Clock()
screen = pygame.display.set_mode((900, 800))
pygame.display.set_caption("PROYECTO")

# Inicia el juego
start_game()
pygame.quit()
