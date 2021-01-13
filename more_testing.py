import sys
import os
import pygame
import time

# from random import randint
# import and_testing

view = 'right'
pygame.init()
size = width, height = 1300, 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption('game')
# screen.fill((255, 255, 255))
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


# группы спрайтов
walls = []

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

player = pygame.image.load("data/tiles.png")
player = pygame.transform.scale(player, (500, 500))

cropped = pygame.Surface((75, 75))

cropped.blit(player, (-5, -25))

tile_images = {
    'wall': load_image('box.png'),
    'empty': cropped
}
player_image = load_image('Run (32x32).png')
bot_image = load_image('Run (322x32).png')

tile_width = tile_height = 50
max_height = height // tile_height
max_width = width // tile_width


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cut_sheet(player_image, 12, 1, pos_x, pos_y)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.pos = (pos_x, pos_y)

    def cut_sheet(self, sheet, columns, rows, pos_x, pos_y):
        self.rect = pygame.Rect(pos_x, pos_y, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def move(self, x, y, turn='right'):
        self.pos = (x, y)

        for i in range(tile_width):
            self.update(turn)
            if turn == 'right':
                self.rect = self.image.get_rect().move(tile_width * self.pos[0] - (tile_width - i),
                                                       tile_height
                                                       * self.pos[1])
                tiles_group.draw(screen)
                and_testing.tiles_group.draw(screen)
                player_group.draw(screen)
                and_testing.player_group.draw(screen)

                clock.tick(120)
                pygame.display.flip()

            elif turn == 'left':
                self.rect = self.image.get_rect().move(tile_width * self.pos[0] + (tile_width - i),
                                                       tile_height
                                                       * self.pos[1])
                tiles_group.draw(screen)
                and_testing.tiles_group.draw(screen)
                player_group.draw(screen)
                and_testing.player_group.draw(screen)

                clock.tick(120)
                pygame.display.flip()

            elif turn == 'up':
                self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                                       tile_height
                                                       * self.pos[1] + (tile_height - i))
                tiles_group.draw(screen)
                and_testing.tiles_group.draw(screen)
                player_group.draw(screen)
                and_testing.player_group.draw(screen)

                clock.tick(120)
                pygame.display.flip()

            elif turn == 'down':

                self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                                       tile_height
                                                       * self.pos[1] - (tile_height - i))
                tiles_group.draw(screen)
                and_testing.tiles_group.draw(screen)
                player_group.draw(screen)
                and_testing.player_group.draw(screen)

                clock.tick(120)
                pygame.display.flip()

    def update(self, turn):
        global view
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (35, 35))
        if turn == 'left' or view == 'left' and turn != 'right':
            view = 'left'
            self.image = pygame.transform.flip(self.frames[self.cur_frame], 90, 0)
        elif turn == 'right' or view == 'right' and turn != 'left':
            view = 'right'
            self.image = self.frames[self.cur_frame]


class Player_bot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cut_sheet(bot_image, 12, 1, pos_x, pos_y)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.pos = (pos_x, pos_y)

    def cut_sheet(self, sheet, columns, rows, pos_x, pos_y):
        self.rect = pygame.Rect(pos_x, pos_y,
                                sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def move(self, x, y, turn='right'):
        self.pos = (x, y)

        for i in range(tile_width):
            self.update(turn)
            if turn == 'right':
                self.rect = self.image.get_rect().move(tile_width * self.pos[0] - (tile_width - i),
                                                       tile_height
                                                       * self.pos[1])
                tiles_group.draw(screen)
                and_testing.player_group.draw(screen)
                player_group.draw(screen)

                clock.tick(120)
                pygame.display.flip()

            elif turn == 'left':
                self.rect = self.image.get_rect().move(tile_width * self.pos[0] + (tile_width - i),
                                                       tile_height
                                                       * self.pos[1])
                tiles_group.draw(screen)
                and_testing.player_group.draw(screen)
                player_group.draw(screen)

                clock.tick(120)
                pygame.display.flip()

            elif turn == 'up':
                self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                                       tile_height
                                                       * self.pos[1] + (tile_height - i))
                tiles_group.draw(screen)
                and_testing.player_group.draw(screen)
                player_group.draw(screen)

                clock.tick(120)
                pygame.display.flip()

            elif turn == 'down':
                self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                                       tile_height
                                                       * self.pos[1] - (tile_height - i))
                tiles_group.draw(screen)
                and_testing.player_group.draw(screen)
                player_group.draw(screen)

                clock.tick(120)
                pygame.display.flip()

    def update(self, turn):
        global view
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (35, 35))
        if turn == 'left' or view == 'left' and turn != 'right':
            view = 'left'
            self.image = pygame.transform.flip(self.frames[self.cur_frame], 90, 0)
        elif turn == 'right' or view == 'right' and turn != 'left':
            view = 'right'
            self.image = self.frames[self.cur_frame]


def generate_level(level):
    new_player, new_player1, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x * tile_width, y * tile_height)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def generate_level_bot(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            # print(x, y)
            if level[y][x] in '@.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '!':
                print(x, y)
                Tile('empty', x, y)
                new_player = Player_bot(x * tile_width, y * tile_height)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def move(player, move):
    x, y = player.pos
    if move == 'up':
        if y > 0 and level_map[y - 1][x] in '.@!':
            player.move(x, y - 1, turn='up')

    elif move == 'down':
        if y < max_height - 1 and level_map[y + 1][x] in '.@!':
            player.move(x, y + 1, turn='down')

    elif move == 'left':
        if x > 0 and level_map[y][x - 1] in '.@!':
            player.move(x - 1, y, turn='left')

    elif move == 'right':
        if x < max_width - 1 and level_map[y][x + 1] in '.@!':
            player.move(x + 1, y, turn='right')


FPS = 50


def terminate1():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (size[0], size[1]))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('exit')
                terminate1()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def get_next_pos_bot(pos, level):
    list_of_pos = [(player.pos[0] // tile_width, player.pos[1] // tile_height)]
    bot_pos = (pos[0] // tile_width, pos[1] // tile_height)
    while True:
        size_list_of_pos = len(list_of_pos)
        # print(list_of_pos)
        for i in range(len(list_of_pos)):
            # print(list_of_pos[i])
            if (list_of_pos[i][0] + 1, list_of_pos[i][1]) == bot_pos \
                    or (list_of_pos[i][0] - 1, list_of_pos[i][1]) == bot_pos \
                    or (list_of_pos[i][0], list_of_pos[i][1] - 1) == bot_pos \
                    or (list_of_pos[i][0], list_of_pos[i][1] + 1) == bot_pos:
                # print(list_of_pos[i][0] * tile_width, list_of_pos[i][1] * tile_height, 1)
                return (list_of_pos[i][0] * tile_width, list_of_pos[i][1] * tile_height)
            else:
                # print(list_of_pos[i], list_of_pos[i][0] + 1, list_of_pos[i][1], max_height, max_width)
                # print(level[list_of_pos[i][0] + 1][list_of_pos[i][1]])
                if list_of_pos[i][0] < max_height - 1:
                    # print(list_of_pos[i][0], max_height - 1)
                    if level[list_of_pos[i][1]][list_of_pos[i][0] + 1] == '.' \
                            and (list_of_pos[i][0] + 1, list_of_pos[i][1]) not in list_of_pos:
                        list_of_pos.append((list_of_pos[i][0] + 1, list_of_pos[i][1]))

                if list_of_pos[i][1] < max_width - 1 and level[list_of_pos[i][1] + 1][list_of_pos[i][0]] == '.' \
                        and (list_of_pos[i][0], list_of_pos[i][1] + 1) not in list_of_pos:
                    list_of_pos.append((list_of_pos[i][0], list_of_pos[i][1] + 1))

                print((list_of_pos[i][0], list_of_pos[i][1] - 1), level[list_of_pos[i][0]][list_of_pos[i][1] - 1])
                if list_of_pos[i][1] > 0 and level[list_of_pos[i][1] - 1][list_of_pos[i][0]] == '.' \
                        and (list_of_pos[i][0], list_of_pos[i][1] - 1) not in list_of_pos:
                    list_of_pos.append((list_of_pos[i][0], list_of_pos[i][1] - 1))

                if list_of_pos[i][0] > 0 and level[list_of_pos[i][1]][list_of_pos[i][0] - 1] == '.' \
                        and (list_of_pos[i][0] - 1, list_of_pos[i][1]) not in list_of_pos:
                    list_of_pos.append((list_of_pos[i][0] - 1, list_of_pos[i][1]))

        if size_list_of_pos == len(list_of_pos):
            print(pos, 2)
            return pos


def bot_go(pos, level, turn):
    if not turn is None:
        if (pos[0] % tile_width == 0
                and pos[1] % tile_height == 0):
            turn = None
            # print(pos)
        else:
            if turn == 'down':
                bot.update(turn='down')
                bot.rect = bot.rect.move(0, 2)
                bot.pos = (bot.pos[0], bot.pos[1] + 2)

            elif turn == 'up':
                bot.update(turn='up')
                bot.rect = bot.rect.move(0, -2)
                bot.pos = (bot.pos[0], bot.pos[1] - 2)


            elif turn == 'left':
                bot.update(turn='left')
                bot.rect = bot.rect.move(-2, 0)
                bot.pos = (bot.pos[0] - 2, bot.pos[1])

            elif turn == 'right':
                bot.update(turn='right')
                bot.rect = bot.rect.move(2, 0)
                bot.pos = (bot.pos[0] + 2, bot.pos[1])


    else:

        x, y = player.pos[0] - pos[0], player.pos[1] - pos[1]
        x_wall, y_wall = pos[0] // tile_width, pos[1] // tile_height

        # print(player.pos[0], pos[0], player.pos[1], pos[1], x_wall, y_wall)
        # print(level[17][9], (x_wall, y_wall))
        # if (x_wall, y_wall) == (15, 9):
        #     time.sleep(20)

        if level[y_wall - 1][x_wall] in '.@!' and y < 0:
            # print(level[y_wall - 1][x_wall], x_wall, y_wall, x, y)
            turn = 'up'
            bot.update(turn='up')
            bot.rect = bot.rect.move(0, -2)
            bot.pos = (bot.pos[0], bot.pos[1] - 2)

        elif level[y_wall][x_wall - 1] in '.@!' and x < 0:
            # print(level[y_wall][x_wall - 1], x_wall, y_wall, x, y)
            turn = 'left'
            bot.update(turn='left')
            bot.rect = bot.rect.move(-2, 0)
            bot.pos = (bot.pos[0] - 2, bot.pos[1])

        elif level[y_wall + 1][x_wall] in '.@!' and y > 0:
            # print(level[y_wall + 1][x_wall], x_wall, y_wall, x, y)
            turn = 'down'
            bot.update(turn='down')
            bot.rect = bot.rect.move(0, 2)
            bot.pos = (bot.pos[0], bot.pos[1] + 2)

        elif level[y_wall][x_wall + 1] in '.@!' and x > 0:
            # print(level[y_wall][x_wall + 1], x_wall, y_wall, x, y)
            turn = 'right'
            bot.update(turn='right')
            bot.rect = bot.rect.move(2, 0)
            bot.pos = (bot.pos[0] + 2, bot.pos[1])

    clock.tick(80)
    return turn


def bot_go_2(pos, level, turn):

    if not turn is None:
        if (pos[0] % tile_width == 0
                and pos[1] % tile_height == 0):
            turn = None
        else:
            bot.update(turn='down')
            bot.rect = bot.rect.move(2 * turn[0], 2 * turn[1])
            bot.pos = (bot.pos[0] + (2 * turn[0]), bot.pos[1] + (2 * turn[1]))



    else:
        new_pos = get_next_pos_bot(pos, level)

        print(new_pos, turn)

        if new_pos[0] - pos[0] > 0:
            x = 1
        elif new_pos[0] - pos[0] < 0:
            x = -1
        else:
            x = 0

        if new_pos[1] - pos[1] > 0:
            y = 1
        elif new_pos[1] - pos[1] < 0:
            y = -1
        else:
            y = 0

        bot.update(turn='down')
        bot.rect = bot.rect.move(2 * x, 2 * y)
        bot.pos = (bot.pos[0] + (2 * x), bot.pos[1] + (2 * y))
        turn = (x, y)

    clock.tick(80)
    return turn


def check_go(move):
    x, y = player.pos[0] // tile_width, player.pos[1] // tile_height

    if move == 'up':
        # print(level_map[y - 1][x], (y - 1, x))
        if y > 0 and level_map[y - 1][x] in '.@!':
            return True

    elif move == 'down':
        # print(level_map[y + 1][x], (y + 1, x))
        if y < max_height - 1 and level_map[y + 1][x] in '.@!':
            return True

    elif move == 'left':
        # print(level_map[y][x - 1], (y, x - 1))
        if x > 0 and level_map[y][x - 1] in '.@!':
            return True

    elif move == 'right':
        # print(level_map[x + 1][y], (y, x + 1))
        if x < max_width - 1 and level_map[y][x + 1] in '.@!':
            return True

    # print(player.pos[0] // tile_width + 1, player.pos[1] // tile_height + 1)
    # print((x, y), move, player.pos)
    return False


if __name__ == '__main__':
    start_screen()

    level_map = load_level('level1.txt')
    bot, level_x, level_y = generate_level_bot(level_map)
    # print(level_x, level_y)
    player, level_x, level_y = generate_level(level_map)
    # print(level_x, level_y)

    # print(walls)

    # print(walls)

    # print(bot in and_testing.player_group)
    running = True

    flag = False

    tec_time = time.time()

    turn, turn_2 = None, None

    while running:
        # get_next_pos_bot(bot.pos, level_map)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # print(bot.pos)

        # if time.time() - tec_time > 0.5:
        turn_2 = bot_go_2(bot.pos, level_map, turn_2)
        # print(turn_2)
        # tec_time = time.time()

        if not turn is None:
            if (player.pos[0] % tile_width == 0
                    and player.pos[1] % tile_height == 0):
                turn = None
            else:
                if turn == 'down':
                    player.update(turn='down')
                    player.rect = player.rect.move(0, 2)
                    player.pos = (player.pos[0], player.pos[1] + 2)

                elif turn == 'up':
                    player.update(turn='up')
                    player.rect = player.rect.move(0, -2)
                    player.pos = (player.pos[0], player.pos[1] - 2)


                elif turn == 'left':
                    player.update(turn='left')
                    player.rect = player.rect.move(-2, 0)
                    player.pos = (player.pos[0] - 2, player.pos[1])


                elif turn == 'right':
                    player.update(turn='right')
                    player.rect = player.rect.move(2, 0)
                    player.pos = (player.pos[0] + 2, player.pos[1])

        else:
            key = pygame.key.get_pressed()

            if key[pygame.K_DOWN]:
                if check_go('down'):
                    turn = 'down'
                    player.update(turn='down')
                    player.rect = player.rect.move(0, 2)
                    player.pos = (player.pos[0], player.pos[1] + 2)

            elif key[pygame.K_UP]:
                if check_go('up'):
                    turn = 'up'
                    player.update(turn='up')
                    player.rect = player.rect.move(0, -2)
                    player.pos = (player.pos[0], player.pos[1] - 2)

            elif key[pygame.K_LEFT]:
                if check_go('left'):
                    turn = 'left'
                    player.update(turn='left')
                    player.rect = player.rect.move(-2, 0)
                    player.pos = (player.pos[0] - 2, player.pos[1])

            elif key[pygame.K_RIGHT]:
                if check_go('right'):
                    turn = 'right'
                    player.update(turn='right')
                    player.rect = player.rect.move(2, 0)
                    player.pos = (player.pos[0] + 2, player.pos[1])

        # print(player.pos)

        # print(proc.is_alive(), 3)

        # if time.time() - tec_time > 0.3:
        # proc.terminate()
        # if not proc.is_alive():f
        # print(proc.is_alive(), 4)
        # proc.run()
        # Thread(target=func).start()
        # flag_move

        # flag_move = None
        # proc.join()
        # print(proc.is_alive()), 5
        # tec_time = time.time()
        # flag_move

        all_sprites.draw(screen)
        tiles_group.draw(screen)
        # and_testing.all_sprites.draw(screen)
        # and_testing.player_group.draw(screen)
        player_group.draw(screen)

        clock.tick(80)
        pygame.display.flip()

pygame.quit()
