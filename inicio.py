import pygame
import sys
import importlib

pygame.init()

try:
    pygame.mixer.init()
except Exception:
    pass

# ---------------- CONFIGURACIÓN VENTANA ----------------
window_size = (700, 650)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("¿PREPARADO PARA MOVER LA CADERA?")
clock = pygame.time.Clock()

# ---------------- FUNCIONES ----------------
def iniciar_juego(archivo_mp3):
    try:
        juego = importlib.import_module("juego")
        importlib.reload(juego)
        if hasattr(juego, "iniciar_juego"):
            juego.iniciar_juego(archivo_mp3)
        else:
            print("El módulo 'juego' no contiene iniciar_juego(archivo_mp3)")
    except ModuleNotFoundError:
        print("Error: no se encontró 'juego.py'.")
    except Exception as e:
        print(f"Error al iniciar juego: {e}")

def terminar_juego(_=None):
    pygame.quit()
    sys.exit()

def reproducir_cancion(ruta_mp3):
    try:
        pygame.mixer.music.load(ruta_mp3)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error al reproducir {ruta_mp3}: {e}")

# ---------------- DATOS CANCIONES ----------------
canciones = [
    ("ROMPE - DADDY YANKEE", "Canciones/rompe.mp3"),
    ("EL PÁJARO AMARILLO", "Canciones/Los50dejoselito.mp3"),
    ("EL NEGRITO DE LA SALSA", "Canciones/El negrito de la Salsa.mp3"),
    ("VIRTUAL DIVA - DON OMAR", "Canciones/Virtual Diva.mp3"),
    ("LA MORENA", "Canciones/La Morena.mp3")
]

# ---------------- FUENTE Y FONDO ----------------
font = pygame.font.Font(None, 25)
try:
    imagendefondo = pygame.image.load("Imagenes_Fondo/fondo.png")
    imagendefondo = pygame.transform.scale(imagendefondo, window_size)
except Exception:
    imagendefondo = pygame.Surface(window_size)
    imagendefondo.fill((0, 0, 0))

# ---------------- CLASE BOTÓN ----------------
class Button:
    def __init__(self, x, y, image, action, arg):
        self.rect = image.get_rect(topleft=(x, y))
        self.image = image
        self.action = action
        self.arg = arg

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.arg is None:
                    self.action()
                else:
                    self.action(self.arg)

# ---------------- FUNCIÓN CARGAR IMAGEN ----------------
def cargar_imagen(path, tamaño=None):
    try:
        img = pygame.image.load(path)
        if tamaño:
            img = pygame.transform.scale(img, tamaño)
        return img
    except Exception:
        surf = pygame.Surface(tamaño if tamaño else (50, 50))
        surf.fill((100, 100, 100))
        return surf

# ---------------- TAMAÑOS ----------------
button_C_width, button_C_height = 50, 50
button_cancion_width, button_cancion_height = 120, 50
button_width, button_height = 150, 50

# ---------------- IMÁGENES ----------------
boton_reproducir_image = cargar_imagen("Imagenes_Letras/reproducir.jpg", (button_C_width, button_C_height))
boton_inicio_image = cargar_imagen("Imagenes_Letras/inicio.jpg", (button_cancion_width, button_cancion_height))
end_button_image = cargar_imagen("Imagenes_Letras/exit.png", (button_width, button_height))

# ---------------- CREAR BOTONES ----------------
botones = []
y_pos = 100  # posición inicial
for nombre, archivo in canciones:
    # Botón reproducir a la izquierda
    botones.append(Button(80, y_pos + 20, boton_reproducir_image, reproducir_cancion, archivo))
    # Botón iniciar a la derecha
    botones.append(Button(180, y_pos + 20, boton_inicio_image, iniciar_juego, archivo))
    y_pos += 90  # más espacio entre filas

# Botón salida al final
button_salida = Button(window_size[0] // 2 - button_width // 2, window_size[1] - 70, end_button_image, terminar_juego, None)
screen = pygame.display.set_mode(window_size)

# ---------------- BUCLE PRINCIPAL ----------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for boton in botones:
            boton.handle_event(event)
        button_salida.handle_event(event)

    # Fondo
    screen.blit(imagendefondo, (0, 0))
    

    # Dibujar canciones con sus botones
    y_text = 100
    for i, (nombre, archivo) in enumerate(canciones):
        txt_surface = font.render(nombre, True, (255, 255, 255))
        txt_rect = txt_surface.get_rect(center=(window_size[0] // 2, y_text))
        screen.blit(txt_surface, txt_rect)

        botones[i * 2].draw(screen)       # Reproducir
        botones[i * 2 + 1].draw(screen)   # Iniciar

        y_text += 90  # coincidir con el espaciado

    # Dibujar botón de salida
    button_salida.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
