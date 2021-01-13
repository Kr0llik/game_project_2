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
label_font = pygame.font.SysFont('mistral', 48)


def settings():
    screen.blit(fon, (0, 0))
    screen.blit(label_font.render(u'Назад', 1, (210, 200, 200)), (580, 650))


def select_level():
    screen.blit(fon, (0, 0))
    for i in range(1, 11):
        screen.blit(label_font.render(str(i), 1, (210, 200, 200)), (350 + 50 * i, 250))
    screen.blit(label_font.render(u'Назад', 1, (210, 200, 200)), (580, 650))

    # pygame.draw.rect(screen, (210, 200, 200),
    #                  (175, 225, 50, 50), 1)


def new_game_f():
    screen.blit(fon, (0, 0))
    screen.blit(label_font.render(u'Вы действительно хотите начать новую игру?', 1, (210, 200, 200)), (325, 250))
    screen.blit(label_font.render(u'Да', 1, (210, 200, 200)), (465, 350))
    screen.blit(label_font.render(u'Нет', 1, (210, 200, 200)), (635, 350))
    screen.blit(label_font.render(u'Назад', 1, (210, 200, 200)), (580, 650))


def menu():
    screen.blit(fon, (0, 0))
    screen.blit(label_font.render(u'Играть', 1, (210, 200, 200)), (585, 250))
    screen.blit(label_font.render(u'Новая игра', 1, (210, 200, 200)), (565, 350))
    screen.blit(label_font.render(u'Выбор уровня', 1, (210, 200, 200)), (555, 450))
    screen.blit(label_font.render(u'Настройки', 1, (210, 200, 200)), (555, 550))
    screen.blit(label_font.render(u'Выход', 1, (210, 200, 200)), (585, 650))


def start_screen():
    screen.blit(fon, (0, 0))

    flag_select_level, flag_new_game, flag_settings = False, False, False

    menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('exit')
                quit()

            if not flag_select_level and not flag_new_game \
                    and not flag_settings:
                if event.type == pygame.MOUSEMOTION:
                    if 700 > event.pos[0] > 587 and 285 > event.pos[1] > 252:
                        screen.blit(label_font.render(u'Играть', 1, (47, 79, 79)), (585, 250))
                    elif 732 > event.pos[0] > 567 and 385 > event.pos[1] > 352:
                        screen.blit(label_font.render(u'Новая игра', 1, (47, 79, 79)), (565, 350))
                    elif 782 > event.pos[0] > 537 and 495 > event.pos[1] > 442:
                        screen.blit(label_font.render(u'Выбор уровня', 1, (47, 79, 79)), (555, 450))
                    elif 732 > event.pos[0] > 577 and 585 > event.pos[1] > 552:
                        screen.blit(label_font.render(u'Настройки', 1, (47, 79, 79)), (555, 550))
                    elif 700 > event.pos[0] > 587 and 685 > event.pos[1] > 652:
                        screen.blit(label_font.render(u'Выход', 1, (47, 79, 79)), (585, 650))
                    else:
                        menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 700 > event.pos[0] > 587 and 285 > event.pos[1] > 252:
                        return
                    elif 732 > event.pos[0] > 567 and 385 > event.pos[1] > 352:
                        new_game_f()
                        flag_new_game = True
                    elif 782 > event.pos[0] > 537 and 485 > event.pos[1] > 452:
                        select_level()
                        flag_select_level = True
                    elif 732 > event.pos[0] > 577 and 585 > event.pos[1] > 552:
                        settings()
                        flag_settings = True
                    elif 700 > event.pos[0] > 587 and 685 > event.pos[1] > 652:
                        quit()

                    # return  # начинаем игру

            elif flag_select_level:
                if event.type == pygame.MOUSEMOTION:
                    if 662 > event.pos[0] > 582 and 685 > event.pos[1] > 652:
                        screen.blit(label_font.render(u'Назад', 1, (47, 79, 79)), (580, 650))
                    elif 425 >= event.pos[0] >= 352 \
                            and 290 >= event.pos[1] >= 252:
                        screen.blit(label_font.render(u'1', 1, (47, 79, 79)), (400, 250))
                    else:
                        select_level()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 662 > event.pos[0] > 582 and 685 > event.pos[1] > 652:
                        flag_select_level = False
                        menu()

            elif flag_new_game:
                if event.type == pygame.MOUSEMOTION:
                    if 662 > event.pos[0] > 582 \
                            and 685 > event.pos[1] > 652:
                        screen.blit(label_font.render(u'Назад', 1, (47, 79, 79)), (580, 650))
                    elif 512 >= event.pos[0] >= 467 \
                            and 380 >= event.pos[1] >= 352:
                        screen.blit(label_font.render(u'Да', 1, (47, 79, 79)), (465, 350))
                    elif 700 >= event.pos[0] >= 637 \
                            and 380 >= event.pos[1] >= 352:
                        screen.blit(label_font.render(u'Нет', 1, (47, 79, 79)), (635, 350))
                    else:
                        new_game_f()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 662 > event.pos[0] > 582 and 685 > event.pos[1] > 652 \
                            or (512 >= event.pos[0] >= 467\
                                and 380 >= event.pos[1] >= 352)\
                            or (700 >= event.pos[0] >= 637\
                                and 380 >= event.pos[1] >= 352):
                        flag_new_game = False
                        menu()

            elif flag_settings:
                if event.type == pygame.MOUSEMOTION:
                    if 662 > event.pos[0] > 582 \
                            and 685 > event.pos[1] > 652:
                        screen.blit(label_font.render(u'Назад', 1, (47, 79, 79)), (580, 650))
                    else:
                        settings()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 662 > event.pos[0] > 582 \
                            and 685 > event.pos[1] > 652:
                        flag_settings = False
                        menu()

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    start_screen()

pygame.quit()
