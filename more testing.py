import sys
import os
import pygame

pygame.init()
size = width, height = 500, 500

screen = pygame.display.set_mode(size)

pygame.display.set_caption('Перемещение героя')
screen.fill((255, 255, 255))

clock = pygame.time.Clock()


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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []

        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        print(self.image)
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (120, 120))
        # self.image = pygame.transform.flip(self.image, 90, 0)


# группы спрайтов

all_sprites = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':

    running = True
    dragon = AnimatedSprite(load_image("Run (32x32).png"), 12, 1, 150, 150)
    print(dragon)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        dragon.update()
        pygame.display.flip()
        clock.tick(10)

pygame.quit()
