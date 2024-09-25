import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
screen = pygame.display.set_mode((700, 800))
pygame.display.set_caption("Nave")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Variables globales
car_width = 40
car_height = 80
car_x = 180
car_y = 500
velocidad = 70  # Velocidad del jugador

# Obstáculos
obstaculos_verticales = []  # Lista para almacenar múltiples obstáculos verticales
obstaculos_horizontales = []  # Lista para almacenar múltiples obstáculos horizontales

# Crear obstáculos en filas y columnas
def crear_obstaculos():
    global obstaculos_verticales, obstaculos_horizontales
    obstaculos_verticales = []
    obstaculos_horizontales = []
    
    # Crear obstáculos verticales
    for i in range(6):  # 6 columnas
        obstaculo_x_1 = i * 120 + 40  # Espaciado de 120 píxeles
        obstaculo_y_1 = random.randint(-800, -80)  # Apariciones en diferentes posiciones
        obstaculo_velocidad_1 = 5
        obstaculos_verticales.append([obstaculo_x_1, obstaculo_y_1, car_width, car_height, obstaculo_velocidad_1, random.randint(0, 300)])

    # Crear obstáculos horizontales
    for i in range(6):  # 6 filas
        obstaculo_x_2 = random.randint(-800, -80)  # Apariciones en diferentes posiciones
        obstaculo_y_2 = i * 120 + 40  # Espaciado de 120 píxeles
        obstaculo_velocidad_2 = 5
        obstaculos_horizontales.append([obstaculo_x_2, obstaculo_y_2, 80, 40, obstaculo_velocidad_2, random.randint(0, 300)])

# Reloj
clock = pygame.time.Clock()

# Función para mostrar pantalla de reinicio
def mostrar_pantalla_reinicio():
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
                    reiniciar_juego()

# Función para reiniciar el juego
def reiniciar_juego():
    global car_x, car_y
    car_x = 180
    car_y = 500
    crear_obstaculos()  # Llama a la nueva función para crear obstáculos

    juego()

# Función principal del juego
def juego():
    global car_x, car_y
    tiempo_total = 0  # Contador de tiempo para gestionar la aparición de obstáculos
    running = True
    while running:
        screen.fill(WHITE)

        # Eventos de control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # Solo responde cuando se presiona una tecla
                if event.key == pygame.K_a and car_x > 0:
                    car_x -= velocidad
                if event.key == pygame.K_d and car_x < 660:
                    car_x += velocidad
                if event.key == pygame.K_w and car_y > 0:
                    car_y -= velocidad
                if event.key == pygame.K_s and car_y < 700:
                    car_y += velocidad

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
                    mostrar_pantalla_reinicio()
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
                    mostrar_pantalla_reinicio()
                    running = False

        pygame.display.update()
        clock.tick(40)

# Iniciar el juego
crear_obstaculos()  # Llama a crear obstáculos antes de iniciar
juego()

pygame.quit()
