import pygame
import pymysql
import random
import pygame_gui

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

grid_size = 40
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

def dibujar_cuadricula():
    for x in range(0, 700, grid_size):
        pygame.draw.line(screen, GRAY, (x, 0), (x, 800))
    for y in range(0, 800, grid_size):
        pygame.draw.line(screen, GRAY, (0, y), (700, y))

def crear_obstaculos():
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
        obstaculos_horizontales.append([obstaculo_x_2, obstaculo_y_2, grid_size, grid_size, obstaculo_velocidad_2, random.randint(0, 300)])

def juego():
    global car_x, car_y
    tiempo_total = 0
    crear_obstaculos()
    running = True

    while running:
        time_delta = clock.tick(30) / 1000.0
        screen.fill(WHITE)
        dibujar_cuadricula()  # Dibujar la cuadrícula
        pygame.draw.line(screen, BLACK, (700, 0), (700, 800), 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.draw.rect(screen, RED, (car_x, car_y, car_width, car_height))
        tiempo_total += 1

        for obstaculo in obstaculos_verticales:
            pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

        for obstaculo in obstaculos_horizontales:
            pygame.draw.rect(screen, BLACK, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))

        pygame.display.update()

if __name__ == "__main__":
    juego()
