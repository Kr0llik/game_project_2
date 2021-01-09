import sys
import os
import pygame

pygame.init()
size = 300, 300
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Спрайты')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


if __name__ == '__main__':
    screen.fill((255, 255, 255))
    all_sprites = pygame.sprite.Group()

    hero_image = load_image('0_Reaper_Man_Throwing_011.png')

    hero_image = pygame.transform.scale(hero_image, (75, 75))

    print(hero_image)

    hero = pygame.sprite.Sprite(all_sprites)
    hero.image = hero_image
    hero.rect = hero.image.get_rect()
    hero.rect.topleft = (1, 1)

    step = 10

    running = True
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN]:
                hero.rect.top += step

            if key[pygame.K_UP]:
                hero.rect.top -= step

            if key[pygame.K_LEFT]:
                hero.rect.left -= step

            if key[pygame.K_RIGHT]:
                hero.rect.left += step

        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
