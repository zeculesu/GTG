from random import choice
from cell import *


# import pygame.examples.eventlist
# pygame.examples.eventlist.main()


class Field(pg.sprite.Sprite):
    hero = pg.image.load('itachi.jpg')
    hero = pg.transform.scale(hero, (60, 60))
    hero.set_colorkey((255, 255, 255))

    def __init__(self, screen_size: tuple, screen, group: pg.sprite.AbstractGroup):
        super(Field, self).__init__(group)
        screen_width, screen_height = screen_size
        self.image = pg.Surface((int(screen_width * 0.9), int(screen_height * 0.9)))
        self.rect = self.image.get_rect()
        self.rect.x = int(screen_width * 0.1)
        self.rect.y = int(screen_height * 0.1)
        self.cells = [[None] * 12 for _ in range(12)]
        self.screen = screen
        options = {Cell: [0, 78],
                   Trap: [0, 60],
                   Health: [0, 40],
                   Task: [0, 60],
                   Teleport: [0, 50]}
        for i in range(12):
            for j in range(12):
                if i == 0 and j == 0:
                    continue
                elif i == 11 and j == 11:
                    self.cells[i][j] = 'finish'
                    break
                option = choice(list(options.keys()))
                while option in self.get_sibling_cells(i, j) or options[option][0] + 1 > options[option][1]:
                    option = choice(list(options.keys()))
                options[option][0] += 1
                self.cells[i][j] = option
                if options[option][1] <= options[option][0]:
                    del options[option]
        self.current_cell = [0, 0]
        # print(self.cells)
        self.move_hero()

    def move_hero(self):
        Field.hero_rect = Field.hero.get_rect(
            bottomright=(60 * (self.current_cell[0] + 1), 60 * (self.current_cell[1] + 1)))
        self.screen.blit(Field.hero, Field.hero_rect)

    def get_sibling_cells(self, i, j):
        cells = ['self.cells[i - 1][j - 1]', 'self.cells[i - 1][j]', 'self.cells[i - 1][j + 1]',
                 'self.cells[i][j - 1]', 'self.cells[i][j + 1]',
                 'self.cells[i + 1][j - 1]', 'self.cells[i + 1][j]', 'self.cells[i + 1][j + 1]']
        square = []
        for cell in cells:
            try:
                square.append(eval(cell))
            except IndexError:
                continue
        return square

    def handle_move(self, event: pg.event.Event):
        i, j = self.current_cell
        if event.key == pg.K_UP or event.key == pg.K_w:
            if self.current_cell[1] != 0:
                self.cells[i][j] = 'way'
                self.current_cell[1] -= 1
        elif event.key == pg.K_DOWN or event.key == pg.K_s:
            if self.current_cell[1] != 11:
                self.cells[i][j] = 'way'
                self.current_cell[1] += 1
        elif event.key == pg.K_LEFT or event.key == pg.K_a:
            if self.current_cell[0] != 0:
                self.cells[i][j] = 'way'
                self.current_cell[0] -= 1
        elif event.key == pg.K_RIGHT or event.key == pg.K_d:
            if self.current_cell[0] != 11:
                self.cells[i][j] = 'way'
                self.current_cell[0] += 1

    def render(self, screen):
        screen.fill('black')
        cell_size = 60
        for i in range(12):
            for j in range(12):
                if str(self.cells[i][j]) == "finish":
                    screen.fill(pg.Color('red'), (cell_size * i, cell_size * j,
                                                  cell_size, cell_size))
                if str(self.cells[i][j]) == "way":
                    screen.fill(pg.Color('lightgreen'), (cell_size * i, cell_size * j,
                                                  cell_size, cell_size))
                # elif str(self.cells[i][j]) == "<class 'cell.Task'>":
                #     screen.fill(pg.Color('#536dfe'), (cell_size * i, cell_size * j,
                #                                   cell_size, cell_size))
                # elif str(self.cells[i][j]) == "<class 'cell.Health'>":
                #     screen.fill(pg.Color('#00e676'), (cell_size * i, cell_size * j,
                #                                     cell_size, cell_size))
                # elif str(self.cells[i][j]) == "<class 'cell.Trap'>":
                #     screen.fill(pg.Color('#ff9100'), (cell_size * i, cell_size * j,
                #                                      cell_size, cell_size))
                # elif str(self.cells[i][j]) == "<class 'cell.Teleport'>":
                #     screen.fill(pg.Color('#9d46ff'), (cell_size * i, cell_size * j,
                #                                      cell_size, cell_size))
                pg.draw.rect(screen, 'white', (cell_size * i, cell_size * j, cell_size, cell_size), 2)


def main():
    pg.init()
    size = 760, 760
    screen = pg.display.set_mode(size)
    pg.display.set_caption('Goof the Game')
    all_sprites = pg.sprite.Group()
    field = Field(size, screen, all_sprites)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                field.handle_move(event)
            field.render(screen)
            field.move_hero()
        pg.display.flip()
    pg.quit()


if __name__ == '__main__':
    main()
