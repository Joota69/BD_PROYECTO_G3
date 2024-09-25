import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Nave")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Posición del carro
car_width = 40
car_height = 80
car_x = 180
car_y = 500
velocidad = 5

# Obstáculos
obstaculo_ancho = 40
obstaculo_alto = 80
obstaculo_velocidad = 7
obstaculo_x = random.randint(0, 360)
obstaculo_y = -obstaculo_alto



# Reloj
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)
    
    # Eventos de control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento del carro (control por teclas)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and car_x > 0:
        car_x -= velocidad

    if keys[pygame.K_d] and car_x < 360:
        car_x += velocidad

    if keys[pygame.K_w] and car_y > 0:
        car_y -= velocidad  # Cambié el signo para mover hacia arriba

    if keys[pygame.K_s] and car_y < 520:
        car_y += velocidad  # Cambié el signo para mover hacia abajo

    # Dibujar el carro del jugador
    pygame.draw.rect(screen, RED, (car_x, car_y, car_width, car_height))

    # Movimiento del obstáculo
    obstaculo_y += obstaculo_velocidad
    if obstaculo_y > 600:
        obstaculo_y = -obstaculo_alto
        obstaculo_x = random.randint(0, 360)

    # Dibujar obstáculo
    pygame.draw.rect(screen, BLACK, (obstaculo_x, obstaculo_y, obstaculo_ancho, obstaculo_alto))

    # Comprobar colisiones
    if (car_y < obstaculo_y + obstaculo_alto and
        car_y + car_height > obstaculo_y and
        car_x < obstaculo_x + obstaculo_ancho and
        car_x + car_width > obstaculo_x):
        print("¡Choque!")
        running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
