import pygame
import sys

pygame.init()
window_size = (700, 650)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("JUEGO EQUIPO 4 ")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 50)
imagendefondo = pygame.image.load("Imagenes_Fondo/fondojuego.png")
imagendefondo = pygame.transform.scale(imagendefondo, window_size)

class Button:
    def __init__(self, x, y, image, action):
        self.rect = image.get_rect(topleft=(x, y))
        self.image = image
        self.action = action

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

def reiniciar_juego():
    import inicio
    inicio.main()

def terminar_juego():
    pygame.quit()
    sys.exit()

# Cargar imágenes y escalar botones
boton_reinicio_image = pygame.image.load("Imagenes_Letras/inicio.jpg")
end_button_image = pygame.image.load("Imagenes_Letras/exit.jpg")

button_width = 200
button_height = 100
boton_inicio_image = pygame.transform.scale(boton_reinicio_image, (button_width, button_height))
end_button_image = pygame.transform.scale(end_button_image, (button_width, button_height))

button_inicio = Button(410, 200, boton_inicio_image, reiniciar_juego)
button_salida = Button(410, 380, end_button_image, terminar_juego)

def main(puntaje):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            button_inicio.handle_event(event)
            button_salida.handle_event(event)

        screen.fill((0, 0, 0))
        screen.blit(imagendefondo, (0, 0))

        # Mostrar puntaje
        texto_puntaje = font.render(f"Tu puntaje fue: {puntaje}", True, (255, 255, 255))
        texto_rect = texto_puntaje.get_rect(center=(window_size[0] // 2, 100))
        screen.blit(texto_puntaje, texto_rect)

        button_inicio.draw(screen)
        button_salida.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
