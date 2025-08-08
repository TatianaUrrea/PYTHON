import pygame
import librosa
import random
import subprocess
import sys

pygame.init()

def pantallafinal(puntaje):
    import pantallafinal
    pantallafinal.main(puntaje)

def iniciar_juego(archivo_mp3):
    global beat_times, line_x_positions, line_colors, fondo_image, titulo_texto, titulo_posicion
    global game_x, game_y, game_width, game_height, buttons, area_1, area_2, area_3, area_4, area_5
    global valor_area_1, valor_area_2, valor_area_3, valor_area_4, valor_area_5
    global nota_radius, blanco, font

    window_width, window_height = 700, 650
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("P E R R E O  I N T E N S O ")

    fondo_image = pygame.image.load('Imagenes_Fondo/fondocanciones.jpg')
    fondo_image = pygame.transform.scale(fondo_image, (window_width, window_height))
    titulo_fuente = pygame.font.Font(None, 28)
    titulo_texto = titulo_fuente.render("R E P R O D U C I E N D O", True, (255, 255, 255))
    titulo_posicion = titulo_texto.get_rect(center=(window_width // 2, 70))

    game_width, game_height = 500, 450
    game_x, game_y = (window_width - game_width) // 2, (window_height - game_height) // 2

    y, sr = librosa.load(archivo_mp3)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = list(librosa.frames_to_time(beats, sr=sr))

    nota_radius = 20
    num_notas = 4
    nota_spacing = (game_width - nota_radius * 2 * num_notas) // (num_notas + 1)
    line_x_positions = [(i + 1) * nota_spacing + i * nota_radius * 2 + nota_radius + game_x for i in range(num_notas)]
    line_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    blanco = (255, 255, 255)

    area_1 = pygame.Rect(game_x, game_y, game_width, game_height // 4)
    area_2 = pygame.Rect(game_x, game_y + game_height // 4, game_width, game_height // 4)
    area_3 = pygame.Rect(game_x, game_y + (game_height // 4) * 2, game_width, game_height // 4)
    area_4 = pygame.Rect(game_x, game_y + (game_height // 4) * 3, game_width, game_height // 12)
    area_5 = pygame.Rect(game_x, game_y + (game_height // 4) * 3 + game_height // 12, game_width, game_height // 6)

    valor_area_1, valor_area_2, valor_area_3, valor_area_4, valor_area_5 = 0, 5, 10, 50, 5

    buttons = []
    for line_x in line_x_positions:
        buttons.extend([
            pygame.Rect(line_x - 10, game_y + (game_height // 4) * i + (game_height // (8 if i < 4 else 12)) - 10, 20, 20)
            for i in range(5)
        ])

    font = pygame.font.Font(None, 72)

    for i in range(3, 0, -1):
        window.blit(fondo_image, (0, 0))
        texto = font.render(str(i), True, blanco)
        rect = texto.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(texto, rect)
        pygame.display.flip()
        pygame.time.wait(1000)

    window.blit(fondo_image, (0, 0))
    texto = font.render("GO!", True, blanco)
    rect = texto.get_rect(center=(window_width // 2, window_height // 2))
    window.blit(texto, rect)
    pygame.display.flip()
    pygame.time.wait(800)

    pygame.mixer.music.stop()
    pygame.mixer.music.load(archivo_mp3)
    pygame.mixer.music.play()

    font = pygame.font.Font(None, 36)

    bucle_juego(archivo_mp3, window, window_width, window_height)

def bucle_juego(archivo_mp3, window, window_width, window_height):
    global beat_times, line_x_positions, line_colors, fondo_image, titulo_texto, titulo_posicion
    global game_x, game_y, game_width, game_height, buttons, area_1, area_2, area_3, area_4, area_5
    global valor_area_1, valor_area_2, valor_area_3, valor_area_4, valor_area_5
    global nota_radius, blanco, font

    teclas_lineas = {
        pygame.K_a: line_x_positions[0],
        pygame.K_s: line_x_positions[1],
        pygame.K_d: line_x_positions[2],
        pygame.K_f: line_x_positions[3]
    }

    fuente_botones = pygame.font.Font(None, 20)
    morado = (128, 0, 128)

    boton_volver = pygame.Rect(window_width - 110, 50, 100, 30)
    boton_playpause = pygame.Rect(window_width - 110, 90, 100, 30)
    boton_reiniciar = pygame.Rect(window_width - 110, 130, 100, 30)
    boton_finalizar = pygame.Rect(window_width - 110, 170, 100, 30)

    notas = []
    puntos = 0
    terminado = False
    cancion_terminada = False
    en_pausa = False

    velocidad_caida_ps = 300
    distancia_caida = area_4.top - game_y
    tiempo_caida = distancia_caida / velocidad_caida_ps

    notas_pendientes = beat_times.copy()

    clock = pygame.time.Clock()

    while not terminado:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminado = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return
            
                elif boton_playpause.collidepoint(event.pos):
                    if en_pausa:
                        pygame.mixer.music.unpause()
                        en_pausa = False
                    else:
                        pygame.mixer.music.pause()
                        en_pausa = True
                elif boton_reiniciar.collidepoint(event.pos):
                    # Para reiniciar correctamente, detén música y llama iniciar_juego con el mismo archivo
                    pygame.mixer.music.stop()
                    iniciar_juego(archivo_mp3)
                    return
                elif boton_finalizar.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    pantallafinal(puntos)
                    return
            elif event.type == pygame.KEYDOWN and event.key in teclas_lineas and not en_pausa:
                for nota in notas:
                    if abs(nota['x'] - teclas_lineas[event.key]) <= nota_radius:
                        if area_1.collidepoint(nota['x'], nota['y']):
                            puntos += valor_area_1
                        elif area_2.collidepoint(nota['x'], nota['y']):
                            puntos += valor_area_2
                        elif area_3.collidepoint(nota['x'], nota['y']):
                            puntos += valor_area_3
                        elif area_4.collidepoint(nota['x'], nota['y']):
                            puntos += valor_area_4
                        elif area_5.collidepoint(nota['x'], nota['y']):
                            puntos += valor_area_5
                        notas.remove(nota)
                        break

        if not en_pausa:
            tiempo_reproduccion = pygame.mixer.music.get_pos() / 1000.0

            while notas_pendientes and tiempo_reproduccion >= notas_pendientes[0] - tiempo_caida:
                nota_x = random.choice(line_x_positions)
                notas.append({'x': nota_x, 'y': float(game_y), 'color': line_colors[line_x_positions.index(nota_x)]})
                notas_pendientes.pop(0)

        window.blit(fondo_image, (0, 0))
        window.blit(titulo_texto, titulo_posicion)

        for rect, texto in [
            (boton_volver, "Volver"),
            (boton_playpause, "Pausa" if not en_pausa else "Play"),
            (boton_reiniciar, "Reiniciar"),
            (boton_finalizar, "Finalizar")
        ]:
            pygame.draw.rect(window, morado, rect, border_radius=8)
            label = fuente_botones.render(texto, True, blanco)
            window.blit(label, (rect.x + (rect.width - label.get_width()) // 2,
                                rect.y + (rect.height - label.get_height()) // 2))

        for line_x, line_color in zip(line_x_positions, line_colors):
            pygame.draw.line(window, line_color, (line_x, game_y), (line_x, game_y + game_height), 3)

        pygame.draw.line(window, blanco,
                         (game_x, area_4.top),
                         (game_x + game_width, area_4.top),
                         2)

        notas_final = []
        for nota in notas:
            if not en_pausa:
                nota['y'] += velocidad_caida_ps * dt
            if nota['y'] - nota_radius < game_y + game_height:
                notas_final.append(nota)
                pygame.draw.circle(window, nota['color'], (int(nota['x']), int(nota['y'])), nota_radius)
        notas = notas_final

        puntaje_texto = font.render("S C O R E " + str(puntos), True, blanco)
        puntaje_posicion = puntaje_texto.get_rect(midbottom=(window_width // 2, window_height - 15))
        window.blit(puntaje_texto, puntaje_posicion)

        pygame.display.flip()

        if not pygame.mixer.music.get_busy() and not en_pausa:
            cancion_terminada = True
        if cancion_terminada:
            pantallafinal(puntos)
            terminado = True  # salir del loop para evitar reinicio o múltiples pantallafinal

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    pygame.quit()


# Ejemplo para iniciar el juego:
