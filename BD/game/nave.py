import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configurar la ventana
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Nave Vertical")

# Colores
black = (0, 0, 0)
white = (255, 255, 255)

# Configuración de la nave
nave_width = 40
nave_height = 20
nave_x = screen_width // 2 - nave_width // 2
nave_y = screen_height // 2 - nave_height // 2
nave_speed = 5
projectiles = []
proyectil_speed = 10

# Bucle principal
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento de la nave (solo vertical)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and nave_y > 0:
        nave_y -= nave_speed
    if keys[pygame.K_DOWN] and nave_y < screen_height - nave_height:
        nave_y += nave_speed
    if keys[pygame.K_SPACE]:  # Disparar
        projectiles.append([nave_x + nave_width // 2, nave_y])

    # Actualizar proyectiles
    projectiles = [[x, y - proyectil_speed] for x, y in projectiles if y > 0]

    # D
