import pygame
import pygame_gui
import pymysql

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Teclado")

clock = pygame.time.Clock()

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

def registrar_evento(tecla, user_id=1):
    connection = conectar_db()
    if connection is None:
        print("Connection to database failed.")
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO Evento (IdUsuario, Tecla) VALUES ({user_id}, '{tecla}')")
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
    finally:
        connection.close()

def teclas():
    manager = pygame_gui.UIManager((400, 300))
    buttons = {"A": (50, 150), "W": (100, 100), "S": (100, 150), "D": (150, 150)}

    for letra, pos in buttons.items():
        pygame_gui.elements.UIButton(relative_rect=pygame.Rect(pos[0], pos[1], 50, 50), text=letra, manager=manager)

    running = True
    while running:
        time_delta = clock.tick(30) / 1000.0
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    registrar_evento(event.ui_element.text)

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

if __name__ == "__main__":
    teclas()
