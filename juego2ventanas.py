import multiprocessing
import pygame
import pymysql

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRID_SIZE = 40

# Ventana del Juego
def ventana_juego(user_id):
    pygame.init()
    screen = pygame.display.set_mode((700, 600))
    pygame.display.set_caption("Juego")
    car_x, car_y = 4 * GRID_SIZE, 4 * GRID_SIZE  # Posición inicial

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        # Dibuja el carro
        pygame.draw.rect(screen, RED, (car_x, car_y, GRID_SIZE, GRID_SIZE))

        # Actualiza la pantalla del juego
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Ventana de Input
def ventana_input(user_id):
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Input de Teclas")
    
    font = pygame.font.SysFont(None, 55)
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)
        # Dibuja las opciones de teclas
        texto = font.render("Presiona W, A, S, D", True, BLACK)
        screen.blit(texto, (50, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print("Tecla W presionada")
                elif event.key == pygame.K_a:
                    print("Tecla A presionada")
                elif event.key == pygame.K_s:
                    print("Tecla S presionada")
                elif event.key == pygame.K_d:
                    print("Tecla D presionada")

        # Actualiza la pantalla de input
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Proceso Principal
if __name__ == '__main__':
    user_id = 1  # Supongamos que ya has obtenido el user_id

    # Crea dos procesos
    proceso_juego = multiprocessing.Process(target=ventana_juego, args=(user_id,))
    proceso_input = multiprocessing.Process(target=ventana_input, args=(user_id,))

    # Inicia ambos procesos
    proceso_juego.start()
    proceso_input.start()

    # Espera a que ambos procesos terminen
    proceso_juego.join()
    proceso_input.join()
