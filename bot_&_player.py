import pygame

pygame.init()
size = width, height = 1300, 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption('game')
screen.fill((255, 255, 255))


player = pygame.image.load("data/pol.png")

cropped = pygame.Surface((500, 500))

cropped.blit(player, (-25, -25))

while True:
    screen.blit(cropped, (250, 206))
    pygame.display.flip()
