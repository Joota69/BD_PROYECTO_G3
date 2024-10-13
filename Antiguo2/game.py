import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
ANCHO, ALTO = 400, 400  # Ajustar para una matriz más pequeña
TAMANO_CELDA = ANCHO // 7  # Matriz de 7x7

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)  # Color rojo para obstáculos horizontales
MORADO = (128, 0, 128)  # Color morado para obstáculos verticales
AZUL = (0, 0, 255)  # Color azul para el personaje

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Esquivar Carritos")

# Matriz del juego: 0 es vacío, 1 es el personaje, 2 son obstáculos
matriz = [[0 for _ in range(7)] for _ in range(7)]  # Cambiar a matriz de 7x7
matriz[3][3] = 1  # Inicializar el personaje en el centro

# Inicializar obstáculos
obstaculos = []
tiempo_ultimo_obstaculo = pygame.time.get_ticks()

# Variables para el movimiento del personaje y obstáculos
tiempo_ultimo_movimiento = pygame.time.get_ticks()
intervalo_obstaculos = 1500  # Intervalo de movimiento de obstáculos (en ms)
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
                # Dibuja los obstáculos según su tipo
                if any(o[0] == fila and o[1] == columna and o[2] == "vertical" for o in obstaculos):
                    pygame.draw.rect(pantalla, MORADO, (x, y, TAMANO_CELDA, TAMANO_CELDA))  # Obstáculo vertical
                elif any(o[0] == fila and o[1] == columna and o[2] == "horizontal" for o in obstaculos):
                    pygame.draw.rect(pantalla, ROJO, (x, y, TAMANO_CELDA, TAMANO_CELDA))  # Obstáculo horizontal
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
    global obstaculos, tiempo_ultimo_obstaculo
    tiempo_actual = pygame.time.get_ticks()

    # Mover obstáculos existentes
    for obstaculo in obstaculos[:]:  # Usar una copia para evitar modificación durante la iteración
        x, y, tipo = obstaculo
        matriz[x][y] = 0  # Limpiar la posición anterior del obstáculo

        # Mover obstáculo
        if tipo == "horizontal":  # Mover horizontalmente
            if y < len(matriz[0]) - 1:
                obstaculo[1] += 1  # Mover hacia la derecha
                matriz[x][y + 1] = 2  # Colocar el obstáculo en la nueva posición
            else:
                obstaculos.remove(obstaculo)  # Eliminar obstáculo si llega al final
        elif tipo == "vertical":  # Mover verticalmente
            if x < len(matriz) - 1:
                obstaculo[0] += 1  # Mover hacia abajo
                matriz[x + 1][y] = 2  # Colocar el obstáculo en la nueva posición
            else:
                obstaculos.remove(obstaculo)  # Eliminar obstáculo si llega al final

    # Generar nuevos obstáculos aleatoriamente
    if tiempo_actual - tiempo_ultimo_obstaculo > random.randint(250, 1000):  # Aumentar la velocidad de aparición
        tipo = random.choice(["horizontal", "vertical"])  # Elegir aleatoriamente el tipo de obstáculo
        
        if tipo == "horizontal":
            fila = random.randint(0, 6)  # Cambiar el rango a 6 para filas de 0 a 6
            # Comprobar si ya hay un obstáculo en esa fila
            if not any(o[0] == fila and o[2] == "horizontal" for o in obstaculos):
                obstaculos.append([fila, 0, "horizontal"])  # Añadir un nuevo obstáculo horizontal
                matriz[fila][0] = 2  # Colocar el obstáculo en la matriz
        elif tipo == "vertical":
            columna = random.randint(0, 6)  # Cambiar el rango a 6 para columnas de 0 a 6
            # Comprobar si ya hay un obstáculo en esa columna
            if not any(o[1] == columna and o[2] == "vertical" for o in obstaculos):
                obstaculos.append([0, columna, "vertical"])  # Añadir un nuevo obstáculo vertical
                matriz[0][columna] = 2  # Colocar el obstáculo en la matriz

        tiempo_ultimo_obstaculo = tiempo_actual  # Actualizar el tiempo del último obstáculo

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
