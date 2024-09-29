import pygame
import random
import pymysql

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
screen = pygame.display.set_mode((700, 800))
pygame.display.set_caption("Nave")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)

# Variables globales
car_width = 40
car_height = 80
car_x = 180
car_y = 500
velocidad = 10  # Velocidad del jugador

# Obstáculos
obstaculos_verticales = []
obstaculos_horizontales = []

# Reloj
clock = pygame.time.Clock()

# Conexión a la base de datos
def conectar_db():
    try:
        connection = pymysql.connect(
            host='autorack.proxy.rlwy.net',
            user='Nilson',
            password='1234',
            db='Diagrama_ER_BD',
            port=42773
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        return None

# Función para registrar evento
def registrar_evento(tecla):
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO Evento (Tecla) VALUES ('{tecla}')")
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
    finally:
        connection.close()

# Función para crear cuenta
def crear_cuenta():
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return None

    running = True
    username = ""
    password = ""
    idRango = ""
    focus = "username"

    while running:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 55)
        mensaje = font.render("Crear Cuenta", True, BLACK)
        screen.blit(mensaje, (120, 100))

        # Crear rectángulos donde se escriben el username, password y categoría
        pygame.draw.rect(screen, GRAY, (120, 200, 300, 40), 0, 5)
        pygame.draw.rect(screen, GRAY, (120, 250, 300, 40), 0, 5)
        pygame.draw.rect(screen, GRAY, (120, 300, 300, 40), 0, 5)

        # Texto dentro de los rectángulos
        font_small = pygame.font.SysFont(None, 30)
        user_text = font_small.render(f"Username: {username}", True, BLACK)
        pass_text = font_small.render(f"Password: {'*' * len(password)}", True, BLACK)
        cat_text = font_small.render(f"Categoría (1, 2, 3): {idRango}", True, BLACK)
        screen.blit(user_text, (130, 210))
        screen.blit(pass_text, (130, 260))
        screen.blit(cat_text, (130, 310))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    if focus == "username":
                        focus = "password"
                    elif focus == "password":
                        focus = "idRango"
                    else:
                        focus = "username"
                elif event.key == pygame.K_BACKSPACE:
                    if focus == "username" and len(username) > 0:
                        username = username[:-1]
                    elif focus == "password" and len(password) > 0:
                        password = password[:-1]
                    elif focus == "idRango" and len(idRango) > 0:
                        idRango = idRango[:-1]
                elif event.key == pygame.K_RETURN:
                    running = False
                else:
                    if focus == "username" and event.unicode.isalnum():
                        username += event.unicode
                    elif focus == "password" and event.unicode.isalnum():
                        password += event.unicode
                    elif focus == "idRango" and event.unicode.isdigit() and len(idRango) < 1:
                        idRango += event.unicode

    if idRango not in ['1', '2', '3']:
        print("Categoría no válida. Inténtalo de nuevo.")
        return None

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM Usuarios WHERE UserName='{username}'")
            if cursor.fetchone():
                print("Username already exists!")
                return None

            # Insertar nuevo usuario en la base de datos
            cursor.execute(f"INSERT INTO Usuarios (UserName, Contraseña, idRango) VALUES ('{username}', '{password}', '{idRango}')")
            connection.commit()
            return username
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None

# Función para iniciar sesión
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

        # Crear rectángulos donde se escriben el username y password
        pygame.draw.rect(screen, GRAY, (120, 200, 300, 40), 0, 5)
        pygame.draw.rect(screen, GRAY, (120, 250, 300, 40), 0, 5)

        # Texto dentro de los rectángulos
        font_small = pygame.font.SysFont(None, 30)
        user_text = font_small.render(f"Username: {username}", True, BLACK)
        pass_text = font_small.render(f"Password: {'*' * len(password)}", True, BLACK)
        screen.blit(user_text, (130, 210))
        screen.blit(pass_text, (130, 260))

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
            query = f"SELECT IdUsuario, Contraseña FROM Usuarios WHERE UserName='{username}'"
            cursor.execute(query)
            result = cursor.fetchone()
            if result and result[1] == password:
                return result[0]  # Retorna el ID del usuario
            else:
                print("Invalid username or password.")
                return None
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None

# Crear obstáculos
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

# Crear botones
def crear_botones():
    botones = {
        'arriba': pygame.Rect(300, 650, 100, 50),
        'abajo': pygame.Rect(300, 750, 100, 50),
        'izquierda': pygame.Rect(200, 700, 100, 50),
        'derecha': pygame.Rect(400, 700, 100, 50)
    }
    return botones

# Mover nave
def mover_nave(direction):
    global car_x, car_y
    if direction == 'izquierda' and car_x > 0:
        car_x -= velocidad
    elif direction == 'derecha' and car_x < 700 - car_width:
        car_x += velocidad
    elif direction == 'arriba' and car_y > 0:
        car_y -= velocidad
    elif direction == 'abajo' and car_y < 800 - car_height:
        car_y += velocidad

# Función principal del juego
def game_loop():
    global car_x, car_y
    game_exit = False
    crear_obstaculos()
    botones = crear_botones()

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Detectar clic en botones
                if botones['arriba'].collidepoint(pos):
                    mover_nave('arriba')
                    registrar_evento('W')
                elif botones['abajo'].collidepoint(pos):
                    mover_nave('abajo')
                    registrar_evento('S')
                elif botones['izquierda'].collidepoint(pos):
                    mover_nave('izquierda')
                    registrar_evento('A')
                elif botones['derecha'].collidepoint(pos):
                    mover_nave('derecha')
                    registrar_evento('D')

        # Limpiar pantalla
        screen.fill(LIGHT_BLUE)

        # Dibujar la nave
        pygame.draw.rect(screen, RED, (car_x, car_y, car_width, car_height))

        # Dibujar obstáculos
        for obstaculo in obstaculos_verticales:
            obstaculo[1] += obstaculo[4]  # Mover hacia abajo
            pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

            if obstaculo[1] > 800:  # Si el obstáculo se sale de la pantalla
                obstaculo[1] = random.randint(-800, -80)  # Reiniciar posición
                obstaculo[0] = obstaculo[5]  # Reaparecer en una nueva posición

        for obstaculo in obstaculos_horizontales:
            obstaculo[0] += obstaculo[4]  # Mover hacia la derecha
            pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

            if obstaculo[0] > 800:  # Si el obstáculo se sale de la pantalla
                obstaculo[0] = random.randint(-800, -80)  # Reiniciar posición
                obstaculo[1] = obstaculo[5]  # Reaparecer en una nueva posición

        # Dibujar botones
        for boton in botones:
            pygame.draw.rect(screen, BLACK, botones[boton])
            font = pygame.font.SysFont(None, 30)
            if boton == 'arriba':
                texto = font.render("W", True, WHITE)
            elif boton == 'abajo':
                texto = font.render("S", True, WHITE)
            elif boton == 'izquierda':
                texto = font.render("A", True, WHITE)
            elif boton == 'derecha':
                texto = font.render("D", True, WHITE)
            screen.blit(texto, (botones[boton].x + 20, botones[boton].y + 10))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Función de inicio
def main():
    while True:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 55)
        mensaje = font.render("Bienvenido", True, BLACK)
        screen.blit(mensaje, (180, 100))
        
        # Opciones para crear cuenta o iniciar sesión
        font_small = pygame.font.SysFont(None, 30)
        crear_cuenta_texto = font_small.render("Presiona C para crear cuenta", True, BLACK)
        iniciar_sesion_texto = font_small.render("Presiona L para iniciar sesión", True, BLACK)
        
        screen.blit(crear_cuenta_texto, (150, 300))
        screen.blit(iniciar_sesion_texto, (150, 350))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    username = crear_cuenta()
                    if username:
                        print(f"Cuenta creada: {username}")
                        game_loop()
                elif event.key == pygame.K_l:
                    user_id = login()
                    if user_id:
                        print(f"Sesión iniciada: ID {user_id}")
                        game_loop()

if __name__ == "__main__":
    main()