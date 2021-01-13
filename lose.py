import sys
import os
import pygame

pygame.init()
size = width, height = 1300, 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption('game_screen')
clock = pygame.time.Clock()
player = None


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


fon = pygame.transform.scale(load_image('test_fon.jpg'), (size[0], size[1]))
label_font_looser = pygame.font.SysFont('mistral', 148)
label_font_menu = pygame.font.SysFont('mistral', 48)


def menu_lose():
    screen.blit(fon, (0, 0))
    screen.blit(label_font.render(u'Вы проиграли', 1, (210, 200, 200)), (335, 250))
    screen.blit(label_font1.render(u'В меню', 1, (210, 200, 200)), (565, 550))


def screen_lose():
    screen.blit(fon, (0, 0))

    menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('exit')
                quit()

            if event.type == pygame.MOUSEMOTION:
                if 700 > event.pos[0] > 587 and 585 > event.pos[1] > 552:
                    screen.blit(label_font1.render(u'В меню', 1, (47, 79, 79)), (565, 550))
                else:
                    menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 700 > event.pos[0] > 587 and 585 > event.pos[1] > 552:
                    print(3)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    start_screen()

pygame.quit()
