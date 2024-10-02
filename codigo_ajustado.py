import pygame
import random
import pymysql
import pygame_gui


pygame.init()

def conectar_db():
    try:
        connection = pymysql.connect(
            host='autorack.proxy.rlwy.net',  
            user='root',
            password='vCuAhonHujKoXRDoFxnNDIMdKmbKpJHX', 
            db='Diagrama_ER_BD',
            port=42773
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        return None

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
        
        screen.blit(label_username, (120, 200))
        screen.blit(label_password, (120, 250))
        screen.blit(user_text, (input_box_username.x+5, input_box_username.y+5))
        screen.blit(pass_text, (input_box_password.x+5, input_box_password.y+5))
        
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
                if input_box_username.collidepoint(event.pos):
                    active_username = not active_username
                else:
                    active_username = False
                if input_box_password.collidepoint(event.pos):
                    active_password = not active_password
                else:
                    active_password = False
                color_username = color_active if active_username else color_inactive
                color_password = color_active if active_password else color_inactive

                if 120 <= event.pos[0] <= 280 and 300 <= event.pos[1] <= 330:
                    return 

    selected_rank = select_rank()
    if not selected_rank:
        print("Ningun Rango Seleccionado")
        return None

    if selected_rank not in [1, 2, 3]:
        print("Rango seleccionado invalido")
        return None

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM Usuarios WHERE UserName='{username}'")
            if cursor.fetchone():
                print("Username already exists!")
                return None

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
                if input_box_username.collidepoint(event.pos):
                    active_username = not active_username
                else:
                    active_username = False
                if input_box_password.collidepoint(event.pos):
                    active_password = not active_password
                else:
                    active_password = False
                color_username = color_active if active_username else color_inactive
                color_password = color_active if active_password else color_inactive
                if 120 <= event.pos[0] <= 280 and 300 <= event.pos[1] <= 330:
                    crear_cuenta()

    try:
        with connection.cursor() as cursor:
            query = f"SELECT IdUsuario, Contraseña FROM Usuarios WHERE UserName='{username}' AND Contraseña='{password}'"
            cursor.execute(query)
            result = cursor.fetchone()
            if result and result[1] == password:
                return result[0]
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


def start_game():
    user_id = None
    while not user_id:
        user_id = login()

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

    manager = pygame_gui.UIManager((900, 800))
    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((750, 10), (140, 50)),
                                               text='Regresar',
                                               manager=manager)

    area_exclusion = pygame.Rect(700, 0, 200, 800)
    filas, columnas = 10, 8
    matriz = crear_matriz(filas, columnas)

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
        tiempo_total += 1

        manejar_movimiento_obstaculos(tiempo_total)
        actualizar_matriz(matriz, obstaculos_verticales, 0)
        actualizar_matriz(matriz, obstaculos_horizontales, 0)

        for obstaculo in obstaculos_verticales:
            if not area_exclusion.colliderect(pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3])):
                pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

            if (car_y < obstaculo[1] + obstaculo[3] and car_y + grid_size > obstaculo[1] and
                car_x < obstaculo[0] + obstaculo[2] and car_x + grid_size > obstaculo[0]):
                print("¡Choque!")
                mostrar_pantalla_reinicio(None)
                running = False

        for obstaculo in obstaculos_horizontales:
            if not area_exclusion.colliderect(pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3])):
                pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

            if (car_y < obstaculo[1] + obstaculo[3] and car_y + grid_size > obstaculo[1] and
                car_x < obstaculo[0] + obstaculo[2] and car_x + grid_size > obstaculo[0]):
                print("¡Choque!")
                mostrar_pantalla_reinicio(None)
                running = False

        actualizar_matriz(matriz, obstaculos_verticales, 1)
        actualizar_matriz(matriz, obstaculos_horizontales, 1)
        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()
    
    connection.close()

def juego(user_id):
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
    tiempo_envio = 0
    running = True
    crear_obstaculos()

    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return

    manager = pygame_gui.UIManager((900, 800))
    dibujar_botones(manager)

    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((750, 10), (140, 50)),
                                               text='Regresar',
                                               manager=manager)

    filas, columnas = 10, 8
    matriz = crear_matriz(filas, columnas)

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
                    if event.ui_element == back_button:
                        seleccionar_modo()
                        return
                    registrar_evento(event.ui_element.text, user_id)

            manager.process_events(event)

        pygame.draw.rect(screen, RED, (car_x, car_y, grid_size, grid_size))
        tiempo_total += 1
        tiempo_envio += time_delta

        manejar_movimiento_obstaculos(tiempo_total)
        actualizar_matriz(matriz, obstaculos_verticales, 0)
        actualizar_matriz(matriz, obstaculos_horizontales, 0)

        for obstaculo in obstaculos_verticales:
            if not area_exclusion.colliderect(pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3])):
                pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

            if (car_y < obstaculo[1] + obstaculo[3] and car_y + grid_size > obstaculo[1] and
                car_x < obstaculo[0] + obstaculo[2] and car_x + grid_size > obstaculo[0]):
                print("¡Choque!")
                mostrar_pantalla_reinicio(user_id)
                running = False

        actualizar_matriz(matriz, obstaculos_verticales, 1)
        actualizar_matriz(matriz, obstaculos_horizontales, 1)

        if tiempo_envio >= 4:
            imprimir_posicion_carro(user_id)
            tiempo_envio = 0

            try:
                with connection.cursor() as cursor:
                    cursor.execute("CALL ObtenerTeclaGanadora() ")
                    connection.commit()

                    cursor.execute("SELECT nk FROM Tecla_ganadora ORDER BY Orden DESC LIMIT 1")
                    result = cursor.fetchone()
                    if result:
                        tecla_ganadora = result[0]
                        mover_carro(tecla_ganadora)
            except pymysql.MySQLError as e:
                print(f"Error executing query: {e}")

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()

    connection.close()

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

obstaculos_verticales = []
obstaculos_horizontales = []

clock = pygame.time.Clock()

screen = pygame.display.set_mode((900, 800))
pygame.display.set_caption("PROYECTO")

start_game()
pygame.quit()
