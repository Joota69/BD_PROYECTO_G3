import pygame
import random
import pymysql
import pygame_gui


pygame.init()

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
            if id_jugador is None:
                # Aquí obtén el valor de `id_jugador` si es necesario
                id_jugador = user_id  # O de donde corresponda
            if tecla_ganadora_orden is None:
                # Aquí obtén el valor de `tecla_ganadora_orden` si es necesario
                tecla_ganadora_orden = 1  # O algún valor válido
            juego(user_id, id_jugador, tecla_ganadora_orden)  # Pasar los tres argumentos


# Cambiar las dimensiones del mapa en visualizar_juego
# Cambiar las dimensiones del mapa en visualizar_juego
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

'''def crear_obstaculos():
    global obstaculos_verticales, obstaculos_horizontales
    obstaculos_verticales = []
    obstaculos_horizontales = []
    
    for i in range(6):
        obstaculo_x_1 = random.randint(0, 16) * grid_size  # Ajustar el rango para cubrir toda el área de juego
        obstaculo_y_1 = random.randint(0, 19) * grid_size  # Ajustar el rango para cubrir toda el área de juego
        obstaculo_velocidad_1 = grid_size / 10  # Reducir la velocidad
        obstaculos_verticales.append([obstaculo_x_1, obstaculo_y_1, grid_size, grid_size, obstaculo_velocidad_1, random.randint(0, 300)])

    for i in range(6):
        obstaculo_x_2 = random.randint(0, 16) * grid_size  # Ajustar el rango para cubrir toda el área de juego
        obstaculo_y_2 = random.randint(0, 19) * grid_size  # Ajustar el rango para cubrir toda el área de juego
        obstaculo_velocidad_2 = grid_size / 10  # Reducir la velocidad
        obstaculos_horizontales.append([obstaculo_x_2, obstaculo_y_2, grid_size, grid_size, obstaculo_velocidad_2, random.randint(0, 300)])'''

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

'''def crear_obstaculos():
    global obstaculos_verticales, obstaculos_horizontales
    obstaculos_verticales = []
    obstaculos_horizontales = []

    # Definir posiciones fijas para los obstáculos verticales
    posiciones_verticales = [
        (1, 1),  # (x, y) en términos de celdas de la cuadrícula
        (3, 2),
        (5, 4),
        (7, 6)
    ]

    # Definir posiciones fijas para los obstáculos horizontales
    posiciones_horizontales = [
        (2, 1),
        (4, 3),
        (6, 5),
        (8, 7)
    ]

    # Crear obstáculos verticales en posiciones fijas
    for pos in posiciones_verticales:
        obstaculo_x = pos[0] * grid_size
        obstaculo_y = pos[1] * grid_size
        obstaculo_velocidad = grid_size / 10  # Velocidad fija
        obstaculos_verticales.append([obstaculo_x, obstaculo_y, grid_size, grid_size, obstaculo_velocidad, 0])

    # Crear obstáculos horizontales en posiciones fijas
    for pos in posiciones_horizontales:
        obstaculo_x = pos[0] * grid_size
        obstaculo_y = pos[1] * grid_size
        obstaculo_velocidad = grid_size / 10  # Velocidad fija
        obstaculos_horizontales.append([obstaculo_x, obstaculo_y, grid_size, grid_size, obstaculo_velocidad, 0])'''

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

def dibujar_cuadricula():
    for x in range(0, 700, grid_size):
        pygame.draw.line(screen, GRAY, (x, 0), (x, 800))
    for y in range(0, 800, grid_size):
        pygame.draw.line(screen, GRAY, (0, y), (700, y))

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

def mostrar_pantalla_reinicio(user_id, id_jugador, tecla_ganadora_orden):
    global votaciones
    # Registrar la partida en la base de datos
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

'''def manejar_movimiento_obstaculos(tiempo_total):
    if tiempo_total % 10 == 0:  # Mover los obstáculos cada 10 ticks
        mover_obstaculos(obstaculos_verticales, 'vertical')
        mover_obstaculos(obstaculos_horizontales, 'horizontal')'''

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
    global car_x, car_y
    if letra == "A" and car_x > 0:
        car_x -= grid_size
    elif letra == "D" and car_x < 660:
        car_x += grid_size
    elif letra == "W" and car_y > 0:
        car_y -= grid_size
    elif letra == "S" and car_y < 700:
        car_y += grid_size


# Cambiar las dimensiones del mapa en juego
def juego(user_id, id_jugador, tecla_ganadora_orden):
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
    tiempo_envio = 0  # Variable para rastrear el tiempo transcurrido para el envío
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

    area_botones = [
        pygame.Rect(750, 300, 50, 50),
        pygame.Rect(800, 250, 50, 50),
        pygame.Rect(800, 300, 50, 50),
        pygame.Rect(850, 300, 50, 50)
    ]

    area_exclusion = pygame.Rect(700, 0, 200, 800)

    filas, columnas = 10, 8  # Ajustar según el tamaño del mapa
    matriz = crear_matriz(filas, columnas)

    while running:
        time_delta = clock.tick(30) / 1000.0
        screen.fill(WHITE)
        dibujar_cuadricula()  # Dibujar la cuadrícula

        pygame.draw.line(screen, BLACK, (700, 0), (700, 800), 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            """ if event.type == pygame.KEYDOWN:  #en caso de emergencias papu
                if event.key == pygame.K_a and car_x > 0:
                    car_x -= grid_size
                    registrar_evento('A', user_id)
                if event.key == pygame.K_d and car_x < 660:
                    car_x += grid_size
                    registrar_evento('D', user_id)
                if event.key == pygame.K_w and car_y > 0:
                    car_y -= grid_size
                    registrar_evento('W', user_id)
                if event.key == pygame.K_s and car_y < 700:
                    car_y += grid_size
                    registrar_evento('S', user_id)"""# para mover con las teclas

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        seleccionar_modo()
                        return
                        #mover_carro(event.ui_element.text)
                    registrar_evento(event.ui_element.text, user_id)

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
                mostrar_pantalla_reinicio(user_id, id_jugador, tecla_ganadora_orden)
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

        if tiempo_envio >= 4:  # Verificar si han pasado 4 segundos
            print("Enviando posición del carro a la base de datos")
            imprimir_posicion_carro(user_id)  # Enviar la posición del carro rojo a la base de datos
            tiempo_envio = 0  # Reiniciar el temporizador

            try:
                with connection.cursor() as cursor:
                    cursor.execute("CALL ObtenerTeclaGanadora() ")  # Llamar al procedimiento almacenado
                    connection.commit()  # Asegurarse de que los cambios se guarden

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

votaciones = 0

obstaculos_verticales = []
obstaculos_horizontales = []

clock = pygame.time.Clock()

screen = pygame.display.set_mode((900, 800))
pygame.display.set_caption("PROYECTO")

start_game()
pygame.quit()