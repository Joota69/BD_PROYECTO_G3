import pygame
import pymysql

# Configuración de la conexión a la base de datos MySQL
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

# Verificar el inicio de sesión del usuario en la base de datos
def verificar_usuario(username, password):
    connection = conectar_db()
    if connection is None:
        print("No se pudo conectar a la base de datos.")
        return None
    
    try:
        with connection.cursor() as cursor:
            query = "SELECT IdUsuario FROM Usuarios WHERE UserName=%s AND Contraseña=%s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            if result:
                return result[0]  # Devuelve el IdUsuario
            else:
                return None
    except pymysql.MySQLError as e:
        print(f"Error ejecutando la consulta: {e}")
        return None
    finally:
        connection.close()

# Función para verificar si el usuario ya votó
def verificar_voto(IdUsuario):
    connection = conectar_db()
    if connection is None:
        print("No se pudo conectar a la base de datos.")
        return False
    
    try:
        with connection.cursor() as cursor:
            query = "SELECT COUNT(*) FROM Evento WHERE IdUsuario=%s"
            cursor.execute(query, (IdUsuario,))
            result = cursor.fetchone()
            if result[0] > 0:
                return True  # Devuelve True si ya ha votado
            return False  # Devuelve False si no ha votado
    except pymysql.MySQLError as e:
        print(f"Error al verificar el voto: {e}")
        return False
    finally:
        connection.close()

# Registrar el voto del usuario
def registrar_voto(IdUsuario, Tecla):
    connection = conectar_db()
    if connection is None:
        print("No se pudo conectar a la base de datos.")
        return
    
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Evento (IdUsuario, Tecla) VALUES (%s, %s)"
            cursor.execute(sql, (IdUsuario, Tecla))
            connection.commit()
            print(f"Voto registrado: {Tecla}")
    except pymysql.MySQLError as e:
        print(f"Error al registrar el voto: {e}")
    finally:
        connection.close()

# Almacenar la tecla ganadora
def almacenar_tecla_ganadora(tecla_ganadora):
    connection = conectar_db()
    if connection is None:
        print("No se pudo conectar a la base de datos.")
        return
    
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Tecla_ganadora (nk) VALUES (%s)"
            cursor.execute(sql, (tecla_ganadora,))
            connection.commit()
            print(f"Tecla ganadora registrada: {tecla_ganadora}")
    except pymysql.MySQLError as e:
        print(f"Error al registrar la tecla ganadora: {e}")
    finally:
        connection.close()

# Eliminar los votos de la tabla Evento
def eliminar_votos():
    connection = conectar_db()
    if connection is None:
        print("No se pudo conectar a la base de datos.")
        return
    
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM Evento"
            cursor.execute(sql)
            connection.commit()
            print("Votos eliminados de la tabla Evento.")
    except pymysql.MySQLError as e:
        print(f"Error al eliminar votos: {e}")
    finally:
        connection.close()

# Pygame setup
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Dimensiones de la pantalla
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Login y Votación en Pygame")

# Fuentes
font = pygame.font.Font(None, 36)

# Variables de entrada
username_text = ''
password_text = ''
active_input = 'username'  # Controla qué cuadro de texto está activo
login_success = False
error_message = ""
id_usuario_actual = None
tecla_ganadora = ""

# Rectángulos de entrada
username_rect = pygame.Rect(200, 150, 250, 40)
password_rect = pygame.Rect(200, 220, 250, 40)

# Estado de los votos
teclas_votos = {'A': 0, 'W': 0, 'S': 0, 'D': 0}
tiempo_restante = 10  # Tiempo para votar (segundos)

# Función para dibujar texto
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    surface.blit(textobj, (x, y))

# Función para el login
def login(username, password):
    global login_success, error_message, id_usuario_actual
    id_usuario = verificar_usuario(username, password)
    
    if id_usuario:
        login_success = True
        id_usuario_actual = id_usuario
        error_message = f"Bienvenido, usuario {username} (ID: {id_usuario})"
    else:
        login_success = False
        error_message = "Credenciales incorrectas. Inténtalo de nuevo."

# Función para manejar el sistema de votación
def votar(tecla):
    global teclas_votos, id_usuario_actual
    if not verificar_voto(id_usuario_actual):
        teclas_votos[tecla] += 1
        registrar_voto(id_usuario_actual, tecla)
        print(f"Voto registrado: {tecla}")
    else:
        print("Ya has votado en esta ronda.")

# Ciclo principal
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    if not login_success:
        # Pantalla de login
        draw_text("Nombre de usuario:", font, BLACK, screen, 50, 150)
        draw_text("Contraseña:", font, BLACK, screen, 50, 220)
        pygame.draw.rect(screen, GREEN if active_input == 'username' else BLACK, username_rect, 2)
        pygame.draw.rect(screen, GREEN if active_input == 'password' else BLACK, password_rect, 2)
        draw_text(username_text, font, BLACK, screen, username_rect.x + 10, username_rect.y + 5)
        draw_text('*' * len(password_text), font, BLACK, screen, password_rect.x + 10, password_rect.y + 5)
        if error_message:
            draw_text(error_message, font, RED if not login_success else GREEN, screen, 50, 300)
    else:
        # Pantalla de votación
        draw_text("Vota por una tecla (A, W, S, D):", font, BLACK, screen, 50, 50)
        draw_text(f"Tiempo restante: {tiempo_restante} segundos", font, BLACK, screen, 50, 100)
        draw_text(f"Tecla ganadora: {tecla_ganadora}", font, BLACK, screen, 50, 150)

        # Si el tiempo de votación se ha agotado
        if tiempo_restante <= 0:
            tecla_ganadora = max(teclas_votos, key=teclas_votos.get)
            almacenar_tecla_ganadora(tecla_ganadora)
            eliminar_votos()
            teclas_votos = {'A': 0, 'W': 0, 'S': 0, 'D': 0}
            tiempo_restante = 10  # Reiniciar el tiempo para la siguiente votación

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if username_rect.collidepoint(event.pos):
                active_input = 'username'
            elif password_rect.collidepoint(event.pos):
                active_input = 'password'

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                active_input = 'password' if active_input == 'username' else 'username'
            elif event.key == pygame.K_BACKSPACE:
                if active_input == 'username':
                    username_text = username_text[:-1]
                else:
                    password_text = password_text[:-1]
            elif event.key == pygame.K_RETURN and not login_success:
                login(username_text, password_text)
            elif event.key in [pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d] and login_success:
                votar(event.unicode.upper())
            else:
                if active_input == 'username':
                    username_text += event.unicode
                elif active_input == 'password':
                    password_text += event.unicode

    if login_success:
        # Reducir el tiempo restante para votar
        if tiempo_restante > 0:
            tiempo_restante -= clock.get_time() / 1000  # Convertir milisegundos a segundos

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
