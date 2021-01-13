import sys
import os
import pygame
from random import randint
import more_testing

view = 'right'
pygame.init()
size = width, height = 1300, 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Перемещение героя')
screen.fill((255, 255, 255))
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


def move(bot_p, move):
    x, y = bot_p.pos
    if move == 'up':
        if y > 0 and level_map[y - 1][x] in '.@':
            bot.move(x, y - 1, turn='up')

    elif move == 'down':
        if y < max_height - 1 and level_map[y + 1][x] in '.@':
            bot.move(x, y + 1, turn='down')

    elif move == 'left':
        if x > 0 and level_map[y][x - 1] in '.@':
            bot.move(x - 1, y, turn='left')

    elif move == 'right':
        if x < max_width - 1 and level_map[y][x + 1] in '.@':
            bot.move(x + 1, y, turn='right')


FPS = 50


def terminate():
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
                terminate()
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


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            # print(x, y)
            if level[y][x] in '@.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                new_player = Player_bot(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


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
        self.rect = pygame.Rect(tile_width * pos_x + 6, tile_height * pos_y + 6,
                                sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def move(self, x, y, turn='right'):
        print('AEAe')
        self.pos = (x, y)

        for i in range(tile_width):
            self.update(turn)
            if turn == 'right':
                self.rect = self.image.get_rect().move(tile_width * self.pos[0] - (tile_width - i),
                                                       tile_height
                                                       * self.pos[1])
                tiles_group.draw(screen)
                player_group.draw(screen)

                clock.tick(120)
                pygame.display.flip()

            elif turn == 'left':
                self.rect = self.image.get_rect().move(tile_width * self.pos[0] + (tile_width - i),
                                                       tile_height
                                                       * self.pos[1])
                tiles_group.draw(screen)
                player_group.draw(screen)

                clock.tick(120)
                pygame.display.flip()

            elif turn == 'up':
                self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                                       tile_height
                                                       * self.pos[1] + (tile_height - i))
                tiles_group.draw(screen)
                player_group.draw(screen)

                clock.tick(120)
                pygame.display.flip()

            elif turn == 'down':
                self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                                       tile_height
                                                       * self.pos[1] - (tile_height - i))
                tiles_group.draw(screen)
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


def bot_go(pos, level):
    s = randint(1, 4)
    if level[pos[1] - 1][pos[0]] != '#' and s == 1:
        move(bot, 'up')

    elif level[pos[1]][pos[0] - 1] != '#' and s == 2:
        move(bot, 'left')

    elif level[pos[1] + 1][pos[0]] != '#' and s == 3:
        move(bot, 'down')

    elif level[pos[1]][pos[0] + 1] != '#' and s == 4:
        move(bot, 'right')


if __name__ == '__main__':
    level_map = load_level("level1.txt")
    bot, level_x, level_y = generate_level(level_map)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        bot_go(bot.pos, level_map)

        # all_sprites.draw(screen)
        # tiles_group.draw(screen)
        # player_group.draw(screen)

        clock.tick(FPS)

        pygame.display.flip()

    pygame.quit()
