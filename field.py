from random import choice
from cell import *
from hero import *
from dice import *

# import pygame.examples.eventlist
# pygame.examples.eventlist.main()


class Field(pg.sprite.Sprite):
    def __init__(self, screen):
        super(Field, self).__init__()
        self.cells = [[None] * 12 for _ in range(12)]
        self.screen = screen
        screen_width, screen_height = screen.get_size()
        self.cell_size = 50
        self.left = screen_width // 2 - len(self.cells[0]) * self.cell_size // 2
        self.top = screen_height // 2 - len(self.cells) * self.cell_size // 2.25
        self.distribution_of_cells()
        self.current_cell = [0, 0]

    def distribution_of_cells(self) -> None:
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

    def get_sibling_cells(self, i, j) -> list:
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

    def handle_move(self, event: pg.event.Event) -> None:
        i, j = self.current_cell
        if event.key == pg.K_UP or event.key == pg.K_w:
            if self.current_cell[1] != 0:
                self.be_way(i, j)
                self.current_cell[1] -= 1
        elif event.key == pg.K_DOWN or event.key == pg.K_s:
            if self.current_cell[1] != 11:
                self.be_way(i, j)
                self.current_cell[1] += 1
        elif event.key == pg.K_LEFT or event.key == pg.K_a:
            if self.current_cell[0] != 0:
                self.be_way(i, j)
                self.current_cell[0] -= 1
        elif event.key == pg.K_RIGHT or event.key == pg.K_d:
            if self.current_cell[0] != 11:
                self.be_way(i, j)
                self.current_cell[0] += 1

    def be_way(self, i, j) -> None:
        self.cells[i][j] = 'way'

    def get_size(self):
        return self.cell_size * len(self.cells[0]), self.cell_size * len(self.cells)

    def get_indent(self):
        return self.left, self.top

    def render(self, screen):
        screen.fill('black')
        for i in range(12):
            for j in range(12):
                if str(self.cells[i][j]) == "finish":
                    screen.fill(pg.Color('red'), (self.left + self.cell_size * i, self.top + self.cell_size * j,
                                                  self.cell_size, self.cell_size))
                if str(self.cells[i][j]) == "way":
                    screen.fill(pg.Color('lightgreen'), (self.left + self.cell_size * i,
                                                         self.top + self.cell_size * j,
                                                         self.cell_size, self.cell_size))
                pg.draw.rect(screen, 'white', (self.left + self.cell_size * i, self.top + self.cell_size * j,
                                               self.cell_size, self.cell_size), 2)

    def get_current_cell(self) -> list:
        return self.current_cell


def main():
    pg.init()
    size = 760, 760
    screen = pg.display.set_mode(size)
    pg.display.set_caption('Goof the Game')
    all_sprites = pg.sprite.Group()
    field = Field(screen)
    hero = Hero(all_sprites)
    dice = Dice(field.get_size(), field.get_indent(), all_sprites)
    running = True
    clock = pg.time.Clock()
    fps = 30
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                field.handle_move(event)
                clock.tick(fps)
            field.render(screen)
            hero.move_hero(field.get_current_cell(), field.get_indent())
        all_sprites.update()
        all_sprites.draw(screen)
        pg.display.flip()
    pg.quit()


if __name__ == '__main__':
    main()
