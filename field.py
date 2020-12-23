from random import randint, choice

import pygame as pg

from cell import *

# import pygame.examples.eventlist
# pygame.examples.eventlist.main()


class Field(pg.sprite.Sprite):
    def __init__(self, screen_size: tuple, group: pg.sprite.AbstractGroup):
        super(Field, self).__init__(group)
        screen_width, screen_height = screen_size
        self.image = pg.Surface((int(screen_width * 0.9), int(screen_height * 0.9)))
        self.rect = self.image.get_rect()
        self.rect.x = int(screen_width * 0.1)
        self.rect.y = int(screen_height * 0.1)
        self.cells = [[None] * 12 for _ in range(12)]
        options = {Cell: [0, 39],
                   Trap: [0, 30],
                   Health: [0, 20],
                   Task: [0, 30],
                   Teleport: [0, 25]}
        option = None
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                while (not option or (option and option in self.get_sibling_cells(i, j))
                       or (option and options[option][0] + 1 > options[option][1])):
                    option = choice(list(options.keys()))
                options[option][0] += 1
                self.cells[i][j] = option
                option = None
        self.current_cell = (0, 0)
        print(self.cells)

    def get_sibling_cells(self, i, j):
        cells = ['self.cells[i - 1][j - 1]', 'self.cells[i - 1][j]', 'self.cells[i - 1][j + 1]',
                 'self.cells[i][j - 1]', 'self.cells[i][j + 1]',
                 'self.cells[i + 1][j - 1]', 'self.cells[i + 1][j]', 'self.cells[i + 1][j + 1]']
        square = []
        for cell in cells:
            try:
                cell = eval(cell)
                square.append(cell)
            except IndexError:
                continue
        return_array = list(filter(lambda x: x, square))
        return list(filter(lambda x: x, square))

    def handle_move(self, event: pg.event.Event):
        if event.key == pg.K_UP or event.key == pg.K_w:
            print('up')
        elif event.key == pg.K_DOWN or event.key == pg.K_s:
            print('down')
        elif event.key == pg.K_LEFT or event.key == pg.K_a:
            print('left')
        elif event.key == pg.K_RIGHT or event.key == pg.K_d:
            print('right')


def main():
    pg.init()
    size = 700, 700
    screen = pg.display.set_mode(size)
    pg.display.set_caption('Goof the Game')
    all_sprites = pg.sprite.Group()
    field = Field(size, all_sprites)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                field.handle_move(event)
        pg.display.flip()
    pg.quit()


if __name__ == '__main__':
    main()