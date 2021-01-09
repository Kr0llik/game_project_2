import sys
import os
import pygame

pygame.init()

size = width, height = 500, 500
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Перемещение героя')
screen.fill((255, 255, 255))
all_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()

player = pygame.image.load("data/0_Reaper_Man_Throwing_011.png")

player = pygame.transform.scale(player, (150, 150))

player = pygame.transform.flip(player, 90, 0)



if __name__ == '__main__':
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        screen.blit(player, (80, 80))
        all_sprites.draw(screen)

        pygame.display.flip()
    pygame.quit()
