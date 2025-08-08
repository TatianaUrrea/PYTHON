import pygame
import sys
pygame.init()

pantalla=pygame.display.set_mode((500,400))
pygame.display.set_caption('Mi primer juego :D')
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()


    













