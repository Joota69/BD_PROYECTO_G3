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

# Inicializar obstáculos
obstaculos = [None] * 10  # Lista para almacenar las posiciones de los obstáculos verticales
obstaculos_horizontales = []  # Lista para los obstáculos que vienen de los lados
obstaculos_activos = 0  # Contador de obstáculos activos
max_obstaculos = 5  # Máximo de obstáculos simultáneos
tiempo_creacion_obstaculos = pygame.time.get_ticks()

# Variables para el movimiento del personaje y obstáculos
tiempo_ultimo_movimiento = pygame.time.get_ticks()
intervalo_movimiento = 100  # Milisegundos entre movimientos (100 ms)
intervalo_obstaculos = 1000  # Mover los obstáculos cada 1000 ms (más lento)
tiempo_ultimo_dibujo = pygame.time.get_ticks()

# Variable para controlar el estado del juego
juego_terminado = False

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
    # Buscar la posición actual del personaje
    x, y = None, None  # Inicializar variables x e y

    for i, fila in enumerate(matriz):
        if 1 in fila:
            x, y = i, fila.index(1)
            break

    if x is None or y is None:  # Verifica si el personaje fue encontrado
        return False  # Si no se encontró, no hay colisión

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
        # Colisión con un obstáculo
        return True  # Indicar que el juego ha terminado
# Función para mover los obstáculos y generar nuevos

def mover_obstaculos(matriz):
    global obstaculos, obstaculos_horizontales, tiempo_creacion_obstaculos, obstaculos_activos
    nuevas_posiciones = []
    
    tiempo_actual = pygame.time.get_ticks()
    
    # Generar nuevos obstáculos solo si hay menos de 5 activos
    if obstaculos_activos < max_obstaculos and tiempo_actual - tiempo_creacion_obstaculos > 2000:
        for i in range(len(obstaculos)):
            if obstaculos_activos >= max_obstaculos:
                break  # No generar más de 5 obstáculos

            if obstaculos[i] is None and random.random() < 0.1:  # Probabilidad del 10% de generar un obstáculo vertical
                obstaculos[i] = (0, i)  # Generar en la fila 0 (vertical)
                obstaculos_activos += 1

            if random.random() < 0.1 and obstaculos_activos < max_obstaculos:  # Probabilidad del 10% de generar obstáculos laterales
                lado = random.choice(["izquierda", "derecha"])  # Generar a la izquierda o derecha
                if lado == "izquierda":
                    obstaculos_horizontales.append((i, 0, "derecha"))  # Obstáculo moviéndose hacia la derecha
                else:
                    obstaculos_horizontales.append((i, len(matriz[0]) - 1, "izquierda"))  # Obstáculo moviéndose hacia la izquierda
                obstaculos_activos += 1
        tiempo_creacion_obstaculos = tiempo_actual

    # Mover los obstáculos verticales existentes hacia abajo
    for i in range(len(obstaculos)):
        if obstaculos[i] is not None:
            x, y = obstaculos[i]
            matriz[x][y] = 0  # Limpiar la posición anterior del obstáculo

            # Mover obstáculo hacia abajo
            if x < len(matriz) - 1:
                nuevas_posiciones.append((x + 1, y))
            else:
                nuevas_posiciones.append(None)  # Eliminar obstáculo si llega al final
                obstaculos_activos -= 1  # Liberar espacio para un nuevo obstáculo
        else:
            nuevas_posiciones.append(None)

    # Mover los obstáculos horizontales hacia el centro
    for obstaculo in obstaculos_horizontales:
        if obstaculo is not None:
            x, y, direccion = obstaculo
            matriz[x][y] = 0  # Limpiar la posición anterior del obstáculo

            # Mover hacia la derecha o hacia la izquierda
            if direccion == "derecha" and y < len(matriz[0]) - 1:
                obstaculos_horizontales[obstaculos_horizontales.index(obstaculo)] = (x, y + 1, direccion)
            elif direccion == "izquierda" and y > 0:
                obstaculos_horizontales[obstaculos_horizontales.index(obstaculo)] = (x, y - 1, direccion)
            else:
                obstaculos_horizontales[obstaculos_horizontales.index(obstaculo)] = None  # Eliminar si llega al borde opuesto
                obstaculos_activos -= 1  # Liberar espacio para un nuevo obstáculo

    # Actualizar la matriz con las nuevas posiciones de los obstáculos
    for nueva_pos in nuevas_posiciones:
        if nueva_pos is not None:
            x, y = nueva_pos
            matriz[x][y] = 2  # Colocar el obstáculo en la nueva posición

    for obstaculo in obstaculos_horizontales:
        if obstaculo is not None:
            x, y, _ = obstaculo
            matriz[x][y] = 2  # Colocar el obstáculo horizontal en la nueva posición

    obstaculos = nuevas_posiciones

# Bucle principal del juego
corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        elif event.type == pygame.KEYDOWN and not juego_terminado:
            if event.key == pygame.K_w:
                juego_terminado = mover_personaje(matriz, 'w')
            elif event.key == pygame.K_s:
                juego_terminado = mover_personaje(matriz, 's')
            elif event.key == pygame.K_a:
                juego_terminado = mover_personaje(matriz, 'a')
            elif event.key == pygame.K_d:
                juego_terminado = mover_personaje(matriz, 'd')

    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - tiempo_ultimo_movimiento > intervalo_obstaculos:
        mover_obstaculos(matriz)
        tiempo_ultimo_movimiento = tiempo_actual

    if tiempo_actual - tiempo_ultimo_dibujo > 100:  # Actualiza la pantalla cada 100 ms
        pantalla.fill(NEGRO)
        dibujar_matriz(matriz)
        
        if juego_terminado:
            # Mostrar el mensaje de Game Over
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, NEGRO)
            pantalla.blit(text, (ANCHO // 2 - text.get_width() // 2, ALTO // 2 - text.get_height() // 2))
        
        pygame.display.flip()
        tiempo_ultimo_dibujo = tiempo_actual

    pygame.time.delay(50)  # Ajusta el delay entre iteraciones

# Cerrar Pygame
pygame.quit()
