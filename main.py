import pygame
import sys
from constantes import *
from datos import lista  # Importar preguntas desde datos.py

# Helper function to check if a point is inside a rectangle
def is_inside_rect(point, rect):
    x, y = point
    return rect.left < x < rect.right and rect.top < y < rect.bottom

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Juego de Preguntas y Respuestas")

# Colores
white = (255, 255, 255)
blue = COLOR_AZUL
red = COLOR_ROJO
black = (0, 0, 0)

# Fuente de texto
font = pygame.font.Font(None, 36)

# Lista de preguntas y respuestas
preguntas = lista  # Utilizar las preguntas de datos.py

# Coordenadas y dimensiones del botón "Pregunta" y "Reiniciar"
boton_pregunta_rect = pygame.Rect(50, 500, 150, 50)
boton_reiniciar_rect = pygame.Rect(250, 500, 150, 50)

# Coordenadas y dimensiones de los botones de opciones
opcion_rects = [
    pygame.Rect(50, 150, 600, 50),
    pygame.Rect(50, 200, 600, 50),
    pygame.Rect(50, 250, 600, 50)
]

# Función para mostrar la pregunta y opciones
def mostrar_pregunta():
    #global preguntas  # Make the variable global
    screen.fill(white)  # Clear the screen
    if current_question_index < len(preguntas):
        pregunta_text = font.render(preguntas[current_question_index]['pregunta'], True, black)
        screen.blit(pregunta_text, (50, 50))

        opciones = [
            preguntas[current_question_index]["a"],
            preguntas[current_question_index]["b"],
            preguntas[current_question_index]["c"]
        ]
        opcion_rects = []  # Lista para almacenar los rectángulos de las opciones
        for i, opcion in enumerate(opciones):
            opcion_text = font.render(f"{i + 1}. {opcion}", True, black)
            opcion_rect = opcion_text.get_rect(topleft=(50, 150 + i * 50))
            screen.blit(opcion_text, opcion_rect.topleft)
            opcion_rects.append(opcion_rect)  # Agregar rectángulo a la lista

        pygame.draw.rect(screen, blue, boton_pregunta_rect)  # Redraw the buttons
        pygame.draw.rect(screen, red, boton_reiniciar_rect)
        texto_pregunta = font.render("Pregunta", True, white)
        texto_reiniciar = font.render("Reiniciar", True, white)
        screen.blit(texto_pregunta, (60, 515))
        screen.blit(texto_reiniciar, (260, 515))

        return opcion_rects
    else:
        # No hay más preguntas, volver a la primera pregunta
        reset_game()
        return mostrar_pregunta()

# Función para verificar la respuesta
def verificar_respuesta(opcion_seleccionada):
    if current_question_index < len(preguntas):
        respuesta_correcta = preguntas[current_question_index]['correcta']
        if opcion_seleccionada == respuesta_correcta:
            return True
    return False

# Función para reiniciar el juego
def reset_game():
    global current_question_index, score, chances
    current_question_index = 0
    score = 0
    chances = 2

# Inicializar variables
current_question_index = 0
score = 0
chances = 2  # Número de oportunidades para responder correctamente

# Initialize opcion_rects before the main game loop
opcion_rects = mostrar_pregunta()

# Variable para rastrear la respuesta seleccionada
opcion_seleccionada = None

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print("Mouse Clicked at:", mouse_pos)

            for i, opcion_rect in enumerate(opcion_rects):
                if is_inside_rect(mouse_pos, opcion_rect):
                    opcion_seleccionada = chr(97 + i)  # Convierte 0, 1 en 'a', 'b', 'c'
                    print("Opción seleccionada:", opcion_seleccionada)

                    if verificar_respuesta(opcion_seleccionada):
                        score += 10

                    current_question_index += 1
                    opcion_seleccionada = None  # Reiniciar la opción seleccionada

                    opcion_rects = mostrar_pregunta()  # Mostrar la siguiente pregunta

                elif is_inside_rect(mouse_pos, boton_reiniciar_rect):
                # Lógica para manejar el clic en el botón "Reiniciar"
                    reset_game()
                    opcion_seleccionada = None  # Reiniciar la opción seleccionada
                opcion_rects = mostrar_pregunta()  # Vuelve a mostrar la primera pregunta
                running = True


                if verificar_respuesta(opcion_seleccionada):
                    score += 10

                current_question_index += 1
                opcion_seleccionada = None  # Reiniciar la opción seleccionada

                opcion_rects = mostrar_pregunta()  # Mostrar la siguiente pregunta

            if is_inside_rect(mouse_pos, boton_pregunta_rect):
                # Lógica para manejar el clic en el botón "Pregunta"
                if current_question_index < len(preguntas) and chances > 0:
                    # Aquí deberías poner la lógica para mostrar la respuesta, como en tu código original.
                    pass

                # Después de mostrar la respuesta, puedes avanzar a la siguiente pregunta o realizar otras acciones.

    # Muestra el puntaje en el centro de la pantalla
    score_text = font.render(f"Score: {score}", True, black)
    score_text_rect = score_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    screen.blit(score_text, score_text_rect)

    pygame.display.flip()

# Esperar a que el usuario cierre la ventana
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()