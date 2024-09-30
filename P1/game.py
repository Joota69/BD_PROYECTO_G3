import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
ANCHO, ALTO = 400, 400  # Ajustar para una matriz más pequeña
TAMANO_CELDA = ANCHO // 10  # Matriz de 10x10

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Esquivar Carritos")

# Matriz del juego: 0 es vacío, 1 es el personaje, 2 son obstáculos
matriz = [[0 for _ in range(10)] for _ in range(10)]
matriz[5][5] = 1  # Inicializar el personaje en el centro

# Inicializar obstáculos en posiciones de la parte superior de cada columna
obstaculos = [(0, col) for col in range(10)]  # Un obstáculo en cada columna en la fila 0
obstaculos_tiempos = [random.randint(1000, 3000) for _ in range(10)]  # Temporizadores para cada columna

# Marcar los obstáculos en la matriz
for x, y in obstaculos:
    matriz[x][y] = 2

# Variables para el movimiento del personaje y obstáculos
tiempo_ultimo_movimiento = pygame.time.get_ticks()
intervalo_movimiento = 1000  # Milisegundos entre movimientos (1 segundo)
tiempo_ultimo_dibujo = pygame.time.get_ticks()

# Función para dibujar la matriz
def dibujar_matriz(matriz):
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            x = columna * TAMANO_CELDA
            y = fila * TAMANO_CELDA
            if matriz[fila][columna] == 1:
                pygame.draw.rect(pantalla, AZUL, (x, y, TAMANO_CELDA, TAMANO_CELDA))  # Personaje
            elif matriz[fila][columna] == 2:
                pygame.draw.rect(pantalla, ROJO, (x, y, TAMANO_CELDA, TAMANO_CELDA))  # Obstáculo
            else:
                pygame.draw.rect(pantalla, BLANCO, (x, y, TAMANO_CELDA, TAMANO_CELDA))  # Espacio vacío
            pygame.draw.rect(pantalla, NEGRO, (x, y, TAMANO_CELDA, TAMANO_CELDA), 1)  # Bordes

# Función para mover al personaje
def mover_personaje(matriz, direccion):
    for i, fila in enumerate(matriz):
        if 1 in fila:
            x, y = i, fila.index(1)
            break
    
    matriz[x][y] = 0  # Borra la posición anterior del personaje
    
    if direccion == 'w' and x > 0:
        x -= 1
    elif direccion == 's' and x < len(matriz) - 1:
        x += 1
    elif direccion == 'a' and y > 0:
        y -= 1
    elif direccion == 'd' and y < len(matriz[0]) - 1:
        y += 1
    
    if matriz[x][y] != 2:  # Mover solo si no hay obstáculo
        matriz[x][y] = 1
    else:
        matriz[x][y] = 1  # Si hay obstáculo, no se mueve

# Función para mover los obstáculos verticalmente y generar nuevos obstáculos
def mover_obstaculos(matriz):
    global obstaculos
    nuevas_posiciones = []
    
    for i in range(len(obstaculos)):
        x, y = obstaculos[i]
        matriz[x][y] = 0  # Limpiar la posición anterior del obstáculo

        # Mover obstáculo hacia abajo
        if x < len(matriz) - 1:
            nuevas_posiciones.append((x + 1, y))
        else:
            nuevas_posiciones.append((x, y))  # Mantener posición si llega al final

        # Generar un nuevo obstáculo en la parte superior con su temporizador
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - obstaculos_tiempos[i] > random.randint(1000, 3000):  # Esperar entre 1 y 3 segundos
            nuevas_posiciones[i] = (0, y)  # Nuevo obstáculo en la fila 0
            obstaculos_tiempos[i] = tiempo_actual  # Reiniciar el temporizador

    # Actualizar la matriz con las nuevas posiciones de los obstáculos
    for x, y in nuevas_posiciones:
        matriz[x][y] = 2  # Colocar el obstáculo en la nueva posición

    obstaculos = nuevas_posiciones

# Bucle principal del juego
corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                mover_personaje(matriz, 'w')
            elif event.key == pygame.K_s:
                mover_personaje(matriz, 's')
            elif event.key == pygame.K_a:
                mover_personaje(matriz, 'a')
            elif event.key == pygame.K_d:
                mover_personaje(matriz, 'd')

    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - tiempo_ultimo_movimiento > intervalo_movimiento:
        mover_obstaculos(matriz)
        tiempo_ultimo_movimiento = tiempo_actual

    if tiempo_actual - tiempo_ultimo_dibujo > 100:  # Actualiza la pantalla cada 100 ms
        pantalla.fill(NEGRO)
        dibujar_matriz(matriz)
        pygame.display.flip()
        tiempo_ultimo_dibujo = tiempo_actual

    pygame.time.delay(50)  # Ajusta el delay entre iteraciones

# Cerrar Pygame
pygame.quit()
