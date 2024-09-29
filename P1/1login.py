import pygame
import random
import pymysql

# Pygame Initialization
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

# En la función crear_cuenta: 

  
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
        ranks = ["1. Noob", "2. Pro", "3. Hacker"]
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

# Comienza el juego solo despues de login o crear cuenta
def start_game():
    user_id = None
    while not user_id:
        user_id = login()
        if not user_id:
            print("No se encontró usuario. Creando nueva cuenta...")
            continue

    if user_id:
        juego(user_id)  




########################################################JUEGO############################################################################
# Screen Setup
screen = pygame.display.set_mode((700, 800))
pygame.display.set_caption("PROYECTO")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Global Variables
car_width = 40
car_height = 80
car_x = 180
car_y = 500
velocidad = 70  # Player speed

# Obstacles
obstaculos_verticales = []
obstaculos_horizontales = []

# Clock
clock = pygame.time.Clock()

# Database connection

def crear_obstaculos():
    global obstaculos_verticales, obstaculos_horizontales
    obstaculos_verticales = []
    obstaculos_horizontales = []
    
    for i in range(6):  # 6 columnas
        obstaculo_x_1 = i * 120 + 40  # Espaciado de 120 píxeles
        obstaculo_y_1 = random.randint(-800, -80)  # Apariciones en diferentes posiciones
        obstaculo_velocidad_1 = 5
        obstaculos_verticales.append([obstaculo_x_1, obstaculo_y_1, car_width, car_height, obstaculo_velocidad_1, random.randint(0, 300)])

    for i in range(6):  # 6 filas
        obstaculo_x_2 = random.randint(-800, -80)  # Apariciones en diferentes posiciones
        obstaculo_y_2 = i * 120 + 40  # Espaciado de 120 píxeles
        obstaculo_velocidad_2 = 5
        obstaculos_horizontales.append([obstaculo_x_2, obstaculo_y_2, 80, 40, obstaculo_velocidad_2, random.randint(0, 300)])


def dibujar_obstaculos():
    global obstaculos_verticales, obstaculos_horizontales
    for obstaculo in obstaculos_verticales:
        pygame.draw.rect(screen, RED, obstaculo)
    for obstaculo in obstaculos_horizontales:
        pygame.draw.rect(screen, RED, obstaculo)

# Función para mostrar pantalla de reinicio
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

# Función para reiniciar el juego
def reiniciar_juego(user_id):
    global car_x, car_y
    car_x = 180
    car_y = 500
    crear_obstaculos()  

    juego(user_id)


def juego(user_id):
    global car_x, car_y
    tiempo_total = 0
    running = True
    crear_obstaculos()
    
    # Mantener la conexión abierta durante el juego
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return

    while running:
        screen.fill(WHITE)

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

                
                if connection:
                    try:
                        with connection.cursor() as cursor:
                            # Insert into Evento table
                            cursor.execute(f"INSERT INTO Evento (Tecla) VALUES ('{event.unicode}')")
                            evento_id = cursor.lastrowid
                            # Insert into Teclas table
                            cursor.execute(f"INSERT INTO Teclas (IdEvento, IdUsuario) VALUES ({evento_id}, {user_id})")
                            connection.commit()
                    except pymysql.MySQLError as e:
                        print(f"Error executing query: {e}")

        # Dibujar el carro del jugador
        pygame.draw.rect(screen, RED, (car_x, car_y, car_width, car_height))

        # Aumentar el tiempo total del juego
        tiempo_total += 1

        # Actualizar y dibujar los obstáculos verticales
        for obstaculo in obstaculos_verticales:
            if tiempo_total > obstaculo[5]:  # Solo dibuja el obstáculo después de su tiempo de aparición
                obstaculo[1] += obstaculo[4]  # Mover el obstáculo hacia abajo
                if obstaculo[1] > 800:  # Si el obstáculo sale de la pantalla, reiniciarlo
                    obstaculo[1] = random.randint(-800, -80)
                    obstaculo[0] = obstaculo[0]  # Mantiene la posición x
                pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

                # Comprobar colisiones con los obstáculos verticales
                if (car_y < obstaculo[1] + obstaculo[3] and
                    car_y + car_height > obstaculo[1] and
                    car_x < obstaculo[0] + obstaculo[2] and
                    car_x + car_width > obstaculo[0]):
                    print("¡Choque!")
                    mostrar_pantalla_reinicio(user_id)
                    running = False

        # Actualizar y dibujar los obstáculos horizontales
        for obstaculo in obstaculos_horizontales:
            if tiempo_total > obstaculo[5]:  # Solo dibuja el obstáculo después de su tiempo de aparición
                obstaculo[0] += obstaculo[4]  # Mover el obstáculo hacia la derecha
                if obstaculo[0] > 700:  # Si el obstáculo sale de la pantalla, reiniciarlo
                    obstaculo[0] = random.randint(-800, -80)
                    obstaculo[1] = obstaculo[1]  # Mantiene la posición y
                pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

                # Comprobar colisiones con los obstáculos horizontales
                if (car_y < obstaculo[1] + obstaculo[3] and
                    car_y + car_height > obstaculo[1] and
                    car_x < obstaculo[0] + obstaculo[2] and
                    car_x + car_width > obstaculo[0]):
                    print("¡Choque!")
                    mostrar_pantalla_reinicio(user_id)
                    running = False

        pygame.display.update()
        clock.tick(40)

    # Cerrar la conexión al final del juego
    connection.close()


# Iniciar el juego
start_game()
pygame.quit()