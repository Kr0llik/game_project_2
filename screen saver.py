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


def start_screen():
    # print(pygame.font.get_fonts())
    label_font = pygame.font.SysFont('mistral', 48)

    fon = pygame.transform.scale(load_image('test_fon.jpg'), (size[0], size[1]))
    screen.blit(fon, (0, 0))
    screen.blit(label_font.render(u'PLAY', 1, (210, 200, 200)), (585, 150))


    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('exit')
                quit()

            if event.type == pygame.MOUSEMOTION:
                print(event.pos)
                if 662 > event.pos[0] > 587 and 185 > event.pos[1] >152 :
                    screen.blit(label_font.render(u'PLAY', 1, (210, 0, 0)), (585, 150))
                else:
                    screen.blit(label_font.render(u'PLAY', 1, (210, 200, 200)), (585, 150))


                # return  # начинаем игру
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    start_screen()

pygame.quit()
