import pygame
import random
import pymysql
import pygame_gui

pygame.init()


clock = pygame.time.Clock()

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



                                ##############################Juego#######################################


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
    global matriz, juego_terminado
    tiempo_total = 0
    running = True
    crear_obstaculos()

    manager = pygame_gui.UIManager((900, 800))
    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((750, 10), (140, 50)),
                                               text='Regresar',
                                               manager=manager)

    area_exclusion = pygame.Rect(700, 0, 200, 800)

    while running:
        time_delta = clock.tick(40) / 1000.0
        screen.fill(WHITE)

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

        dibujar_matriz(matriz)

        tiempo_total += 1

        if tiempo_total % 25 == 0:
            mover_obstaculos(matriz)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()

def crear_obstaculos():
    global obstaculos, obstaculos_horizontales, obstaculos_activos, tiempo_creacion_obstaculos
    obstaculos = [None] * 10
    obstaculos_horizontales = []
    obstaculos_activos = 0
    tiempo_creacion_obstaculos = pygame.time.get_ticks()

def dibujar_matriz(matriz):
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            x = columna * TAMANO_CELDA
            y = fila * TAMANO_CELDA
            if matriz[fila][columna] == 1:
                pygame.draw.rect(screen, BLUE, (x, y, TAMANO_CELDA, TAMANO_CELDA))  # Personaje
            elif matriz[fila][columna] == 2:
                pygame.draw.rect(screen, RED, (x, y, TAMANO_CELDA, TAMANO_CELDA))  # Obstáculo
            else:
                pygame.draw.rect(screen, WHITE, (x, y, TAMANO_CELDA, TAMANO_CELDA))  # Espacio vacío
            pygame.draw.rect(screen, BLACK, (x, y, TAMANO_CELDA, TAMANO_CELDA), 1)  # Bordes

def mostrar_pantalla_reinicio(user_id):
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

def reiniciar_juego(user_id):
    global matriz, juego_terminado
    matriz = [[0 for _ in range(10)] for _ in range(10)]
    matriz[5][5] = 1
    crear_obstaculos()
    juego_terminado = False
    juego(user_id)

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

def mover_carro(letra):
    global matriz, juego_terminado
    if letra == "A":
        juego_terminado = mover_personaje(matriz, 'a')
    elif letra == "D":
        juego_terminado = mover_personaje(matriz, 'd')
    elif letra == "W":
        juego_terminado = mover_personaje(matriz, 'w')
    elif letra == "S":
        juego_terminado = mover_personaje(matriz, 's')

def mover_personaje(matriz, direccion):
    x, y = None, None

    for i, fila in enumerate(matriz):
        if 1 in fila:
            x, y = i, fila.index(1)
            break

    if x is None or y is None:
        return False

    matriz[x][y] = 0

    if direccion == 'w' and x > 0:
        x -= 1
    elif direccion == 's' and x < len(matriz) - 1:
        x += 1
    elif direccion == 'a' and y > 0:
        y -= 1
    elif direccion == 'd' and y < len(matriz[0]) - 1:
        y += 1

    if matriz[x][y] != 2:
        matriz[x][y] = 1
    else:
        return True

def mover_obstaculos(matriz):
    global obstaculos, obstaculos_horizontales, tiempo_creacion_obstaculos, obstaculos_activos
    nuevas_posiciones = []
    
    tiempo_actual = pygame.time.get_ticks()
    
    if obstaculos_activos < MAX_OBSTACULOS and tiempo_actual - tiempo_creacion_obstaculos > 2000:
        for i in range(len(obstaculos)):
            if obstaculos_activos >= MAX_OBSTACULOS:
                break

            if obstaculos[i] is None and random.random() < 0.1:
                obstaculos[i] = (0, i)
                obstaculos_activos += 1

            if random.random() < 0.1 and obstaculos_activos < MAX_OBSTACULOS:
                lado = random.choice(["izquierda", "derecha"])
                if lado == "izquierda":
                    obstaculos_horizontales.append((i, 0, "derecha"))
                else:
                    obstaculos_horizontales.append((i, len(matriz[0]) - 1, "izquierda"))
                obstaculos_activos += 1
        tiempo_creacion_obstaculos = tiempo_actual

    for i in range(len(obstaculos)):
        if obstaculos[i] is not None:
            x, y = obstaculos[i]
            matriz[x][y] = 0

            if x < len(matriz) - 1:
                nuevas_posiciones.append((x + 1, y))
            else:
                nuevas_posiciones.append(None)
                obstaculos_activos -= 1
        else:
            nuevas_posiciones.append(None)

    for obstaculo in obstaculos_horizontales:
        if obstaculo is not None:
            x, y, direccion = obstaculo
            matriz[x][y] = 0

            if direccion == "derecha" and y < len(matriz[0]) - 1:
                obstaculos_horizontales[obstaculos_horizontales.index(obstaculo)] = (x, y + 1, direccion)
            elif direccion == "izquierda" and y > 0:
                obstaculos_horizontales[obstaculos_horizontales.index(obstaculo)] = (x, y - 1, direccion)
            else:
                obstaculos_horizontales[obstaculos_horizontales.index(obstaculo)] = None
                obstaculos_activos -= 1

    for nueva_pos in nuevas_posiciones:
        if nueva_pos is not None:
            x, y = nueva_pos
            matriz[x][y] = 2

    for obstaculo in obstaculos_horizontales:
        if obstaculo is not None:
            x, y, _ = obstaculo
            matriz[x][y] = 2

    obstaculos = nuevas_posiciones

def juego(user_id):
    global matriz, obstaculos, obstaculos_horizontales, obstaculos_activos, tiempo_creacion_obstaculos
    matriz = [[0 for _ in range(10)] for _ in range(10)]
    matriz[5][5] = 1
    obstaculos = [None] * 10
    obstaculos_horizontales = []
    obstaculos_activos = 0
    tiempo_creacion_obstaculos = pygame.time.get_ticks()
    juego_terminado = False

    tiempo_ultimo_movimiento = pygame.time.get_ticks()
    tiempo_ultimo_dibujo = pygame.time.get_ticks()
    intervalo_movimiento = 100  # Milisegundos entre movimientos (100 ms)
    intervalo_obstaculos = 1000  # Mover los obstáculos cada 1000 ms (más lento)

    while not juego_terminado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    juego_terminado = mover_personaje(matriz, 'w')
                    registrar_evento('W', user_id)
                elif event.key == pygame.K_s:
                    juego_terminado = mover_personaje(matriz, 's')
                    registrar_evento('S', user_id)
                elif event.key == pygame.K_a:
                    juego_terminado = mover_personaje(matriz, 'a')
                    registrar_evento('A', user_id)
                elif event.key == pygame.K_d:
                    juego_terminado = mover_personaje(matriz, 'd')
                    registrar_evento('D', user_id)

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultimo_movimiento > intervalo_obstaculos:
            mover_obstaculos(matriz)
            tiempo_ultimo_movimiento = tiempo_actual

        if tiempo_actual - tiempo_ultimo_dibujo > 100:
            screen.fill(BLACK)
            dibujar_matriz(matriz)

            if juego_terminado:
                font = pygame.font.Font(None, 74)
                text = font.render("Game Over", True, BLACK)
                screen.blit(text, (ANCHO // 2 - text.get_width() // 2, ALTO // 2 - text.get_height() // 2))

            pygame.display.flip()
            tiempo_ultimo_dibujo = tiempo_actual

        pygame.time.delay(50)

# Definición de constantes
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)  # Definición del color azul

ANCHO, ALTO = 400, 400
TAMANO_CELDA = ANCHO // 10
MAX_OBSTACULOS = 5  # Definición del máximo de obstáculos simultáneos

screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PROYECTO")

start_game()
pygame.quit()