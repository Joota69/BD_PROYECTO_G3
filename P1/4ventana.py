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

def crear_cuenta():
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return None

    running = True
    username = ""
    password = ""
    focus = "username"  

    while running:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 55)
        mensaje = font.render("Crear Cuenta", True, BLACK)
        screen.blit(mensaje, (120, 100))

        font_small = pygame.font.SysFont(None, 30)
        user_text = font_small.render(f"Username: {username}", True, BLACK)
        pass_text = font_small.render(f"Password: {'*' * len(password)}", True, BLACK)
        screen.blit(user_text, (120, 200))
        screen.blit(pass_text, (120, 250))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    focus = "password" if focus == "username" else "username"
                elif event.key == pygame.K_BACKSPACE:
                    if focus == "username" and len(username) > 0:
                        username = username[:-1]
                    elif focus == "password" and len(password) > 0:
                        password = password[:-1]
                elif event.key == pygame.K_RETURN:
                    running = False
                else:
                    if focus == "username" and event.unicode.isalnum():
                        username += event.unicode
                    elif focus == "password" and event.unicode.isalnum():
                        password += event.unicode

    selected_rank = select_rank()
    if not selected_rank:
        print("No rank selected.")
        return None

    if selected_rank not in [1, 2, 3]:
        print("Invalid rank selected!")
        return None

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM Usuarios WHERE UserName='{username}'")
            if cursor.fetchone():
                print("Username already exists!")
                return None

            cursor.execute(f"INSERT INTO Usuarios (UserName, Contraseña, Rango_idRango) VALUES ('{username}', '{password}', {selected_rank})")
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
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    focus = "password" if focus == "username" else "username"
                elif event.key == pygame.K_BACKSPACE:
                    if focus == "username" and len(username) > 0:
                        username = username[:-1]
                    elif focus == "password" and len(password) > 0:
                        password = password[:-1]
                elif event.key == pygame.K_RETURN:
                    running = False
                else:
                    if focus == "username" and event.unicode.isalnum():
                        username += event.unicode
                    elif focus == "password" and event.unicode.isalnum():
                        password += event.unicode

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
        ranks = ["Noob", "Pro", "Hacker"]
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

    modo = seleccionar_modo()
    if modo == "visualizar":
        visualizar_juego()
    elif modo == "jugar":
        juego(user_id)

def visualizar_juego():
    global car_x, car_y
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
                        start_game()
                        return

            manager.process_events(event)

        pygame.draw.rect(screen, RED, (car_x, car_y, car_width, car_height))

        tiempo_total += 1

        for obstaculo in obstaculos_verticales:
            if tiempo_total > obstaculo[5]:
                obstaculo[1] += obstaculo[4]
                if obstaculo[1] > 800:
                    obstaculo[1] = random.randint(-800, -80)
                    obstaculo[0] = obstaculo[0]
                if not area_exclusion.colliderect(pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3])):
                    pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

                if (car_y < obstaculo[1] + obstaculo[3] and
                    car_y + car_height > obstaculo[1] and
                    car_x < obstaculo[0] + obstaculo[2] and
                    car_x + car_width > obstaculo[0]):
                    print("¡Choque!")
                    mostrar_pantalla_reinicio(None)
                    running = False

        for obstaculo in obstaculos_horizontales:
            if tiempo_total > obstaculo[5]:
                obstaculo[0] += obstaculo[4]
                if obstaculo[0] > 700:
                    obstaculo[0] = random.randint(-800, -80)
                    obstaculo[1] = obstaculo[1]
                if not area_exclusion.colliderect(pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3])):
                    pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

                if (car_y < obstaculo[1] + obstaculo[3] and
                    car_y + car_height > obstaculo[1] and
                    car_x < obstaculo[0] + obstaculo[2] and
                    car_x + car_width > obstaculo[0]):
                    print("¡Choque!")
                    mostrar_pantalla_reinicio(None)
                    running = False

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()

def crear_obstaculos():
    global obstaculos_verticales, obstaculos_horizontales
    obstaculos_verticales = []
    obstaculos_horizontales = []
    
    for i in range(6):
        obstaculo_x_1 = i * 120 + 40
        obstaculo_y_1 = random.randint(-800, -80)
        obstaculo_velocidad_1 = 5
        obstaculos_verticales.append([obstaculo_x_1, obstaculo_y_1, car_width, car_height, obstaculo_velocidad_1, random.randint(0, 300)])

    for i in range(6):
        obstaculo_x_2 = random.randint(-800, -80)
        obstaculo_y_2 = i * 120 + 40
        obstaculo_velocidad_2 = 5
        obstaculos_horizontales.append([obstaculo_x_2, obstaculo_y_2, 80, 40, obstaculo_velocidad_2, random.randint(0, 300)])

def dibujar_obstaculos():
    global obstaculos_verticales, obstaculos_horizontales
    for obstaculo in obstaculos_verticales:
        pygame.draw.rect(screen, RED, obstaculo)
    for obstaculo in obstaculos_horizontales:
        pygame.draw.rect(screen, RED, obstaculo)

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
    global car_x, car_y
    car_x = 180
    car_y = 500
    crear_obstaculos()  

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
    global car_x, car_y
    if letra == "A" and car_x > 0:
        car_x -= velocidad
    elif letra == "D" and car_x < 660:
        car_x += velocidad
    elif letra == "W" and car_y > 0:
        car_y -= velocidad
    elif letra == "S" and car_y < 700:
        car_y += velocidad

def juego(user_id):
    global car_x, car_y
    tiempo_total = 0
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

    while running:
        time_delta = clock.tick(40) / 1000.0
        screen.fill(WHITE)

        pygame.draw.line(screen, BLACK, (700, 0), (700, 800), 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and car_x > 0:
                    car_x -= velocidad
                if event.key == pygame.K_d and car_x < 660:
                    car_x += velocidad
                if event.key == pygame.K_w and car_y > 0:
                    car_y -= velocidad
                if event.key == pygame.K_s and car_y < 700:
                    car_y += velocidad
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        start_game()
                        return
                    mover_carro(event.ui_element.text)

            manager.process_events(event)

        pygame.draw.rect(screen, RED, (car_x, car_y, car_width, car_height))

        tiempo_total += 1

        for obstaculo in obstaculos_verticales:
            if tiempo_total > obstaculo[5]:
                obstaculo[1] += obstaculo[4]
                if obstaculo[1] > 800:
                    obstaculo[1] = random.randint(-800, -80)
                    obstaculo[0] = obstaculo[0]
                if not area_exclusion.colliderect(pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3])):
                    pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

                if (car_y < obstaculo[1] + obstaculo[3] and
                    car_y + car_height > obstaculo[1] and
                    car_x < obstaculo[0] + obstaculo[2] and
                    car_x + car_width > obstaculo[0]):
                    print("¡Choque!")
                    mostrar_pantalla_reinicio(user_id)
                    running = False

        for obstaculo in obstaculos_horizontales:
            if tiempo_total > obstaculo[5]:
                obstaculo[0] += obstaculo[4]
                if obstaculo[0] > 700:
                    obstaculo[0] = random.randint(-800, -80)
                    obstaculo[1] = obstaculo[1]
                if not area_exclusion.colliderect(pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3])):
                    pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

                if (car_y < obstaculo[1] + obstaculo[3] and
                    car_y + car_height > obstaculo[1] and
                    car_x < obstaculo[0] + obstaculo[2] and
                    car_x + car_width > obstaculo[0]):
                    print("¡Choque!")
                    mostrar_pantalla_reinicio(user_id)
                    running = False

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()

    connection.close()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

car_width = 40
car_height = 80
car_x = 180
car_y = 500
velocidad = 70

obstaculos_verticales = []
obstaculos_horizontales = []

clock = pygame.time.Clock()

screen = pygame.display.set_mode((900, 800))
pygame.display.set_caption("PROYECTO")

def visualizar_juego():
    global car_x, car_y
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
                        start_game()
                        return

            manager.process_events(event)

        pygame.draw.rect(screen, RED, (car_x, car_y, car_width, car_height))

        tiempo_total += 1

        for obstaculo in obstaculos_verticales:
            if tiempo_total > obstaculo[5]:
                obstaculo[1] += obstaculo[4]
                if obstaculo[1] > 800:
                    obstaculo[1] = random.randint(-800, -80)
                    obstaculo[0] = obstaculo[0]
                if not area_exclusion.colliderect(pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3])):
                    pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

                if (car_y < obstaculo[1] + obstaculo[3] and
                    car_y + car_height > obstaculo[1] and
                    car_x < obstaculo[0] + obstaculo[2] and
                    car_x + car_width > obstaculo[0]):
                    print("¡Choque!")
                    mostrar_pantalla_reinicio(None)
                    running = False

        for obstaculo in obstaculos_horizontales:
            if tiempo_total > obstaculo[5]:
                obstaculo[0] += obstaculo[4]
                if obstaculo[0] > 700:
                    obstaculo[0] = random.randint(-800, -80)
                    obstaculo[1] = obstaculo[1]
                if not area_exclusion.colliderect(pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3])):
                    pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

                if (car_y < obstaculo[1] + obstaculo[3] and
                    car_y + car_height > obstaculo[1] and
                    car_x < obstaculo[0] + obstaculo[2] and
                    car_x + car_width > obstaculo[0]):
                    print("¡Choque!")
                    mostrar_pantalla_reinicio(None)
                    running = False

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()

start_game()
pygame.quit()
