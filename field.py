from random import choice
import pygame as pg
from img_loader import ImageLoader
from cell import *
from hero import *
from dice import *


class Field(pg.sprite.Sprite, ImageLoader):
    # img_filename = 'grass.png'

    def __init__(self, screen):
        super(Field, self).__init__()
        # self.image = self.load_image(Field.img_filename)
        # self.image = pg.transform.scale(self.image, (25, 25))
        self.cells = [[None] * 12 for _ in range(12)]
        self.screen = screen
        screen_width, screen_height = screen.get_size()
        self.cell_size = 50
        self.left = screen_width // 2 - len(self.cells[0]) * self.cell_size // 2
        self.top = screen_height // 2 - len(self.cells) * self.cell_size // 2.25
        self.distribution_of_cells()
        self.current_cell = [0, 0]
        self.frozen = True

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

    def check_move(self):
        pass

    def handle_move(self, event: pg.event.Event, hero: Hero, dice: Dice) -> None:
        if not self.frozen:
            i, j = self.current_cell
            move_allowed = False
            if hero.get_moves() > 0:
                if event.key == pg.K_UP or event.key == pg.K_w:
                    if self.current_cell[1] != 0:
                        move_allowed = True
                        self.be_way(i, j)
                        self.current_cell[1] -= 1
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    if self.current_cell[1] != len(self.cells[0]) - 1:
                        move_allowed = True
                        self.be_way(i, j)
                        self.current_cell[1] += 1
                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    if self.current_cell[0] != 0:
                        move_allowed = True
                        self.be_way(i, j)
                        self.current_cell[0] -= 1
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    if self.current_cell[0] != len(self.cells) - 1:
                        move_allowed = True
                        self.be_way(i, j)
                        self.current_cell[0] += 1
                if move_allowed:
                    callback = hero.move_hero(self.current_cell, (self.left, self.top))
                    if callback == 'show-dice':
                        self.show_dice(dice)
                if self.current_cell[0] == len(self.cells) - 1 and self.current_cell[1] == len(self.cells) - 1:
                    print('finish')

    def be_way(self, i, j) -> None:
        if str(self.cells[i][j]) != "finish":
            self.cells[i][j] = 'way'

    def get_size(self):
        return self.cell_size * len(self.cells[0]), self.cell_size * len(self.cells)

    def get_indent(self):
        return self.left, self.top

    def render(self, screen, moves, lives):
        screen.fill('black')
        pg.font.init()
        font = pg.font.Font('font/Special Elite.ttf', 36)
        move = font.render(f'Moves - {moves}', True,
                          '#80deea')
        live = font.render(f'Lives - {lives}', True,
                          '#80deea')
        screen.blit(move, (self.left, 50))
        screen.blit(live, (self.left + font.size(f'Количество ходов - {moves}')[0] + 150, 50))
        for i in range(12):
            for j in range(12):
                if str(self.cells[i][j]) == "finish":
                    screen.fill(pg.Color('red'), (self.left + self.cell_size * i, self.top + self.cell_size * j,
                                                  self.cell_size, self.cell_size))
                if str(self.cells[i][j]) == "way":
                    screen.fill(pg.Color('lightgreen'), (self.left + self.cell_size * i,
                                                         self.top + self.cell_size * j,
                                                         self.cell_size, self.cell_size))
                    # rect = self.image.get_rect(
                    #     bottomright=(self.left + 45 * (i + 1),
                    #                  self.top + 45 * (j + 1)))
                    # screen.blit(self.image, rect)
                pg.draw.rect(screen, '#e8eaf6', (self.left + self.cell_size * i, self.top + self.cell_size * j,
                                                 self.cell_size, self.cell_size), 2)

    def get_current_cell(self) -> list:
        return self.current_cell

    def froze(self):
        self.frozen = not self.frozen

    def is_frozen(self):
        return self.frozen

    def show_dice(self, dice):
        self.froze()
        dice.visibled()
        dice.rotating = True


def main():
    pg.init()
    #pg.key.set_repeat(200, 120)
    size = 760, 760
    screen = pg.display.set_mode(size)
    pg.display.set_caption('Goof the Game')
    all_sprites = pg.sprite.Group()
    field = Field(screen)
    hero = Hero((0, 0), field.get_indent(), all_sprites)
    dice = Dice(field.get_size(), field.get_indent(), all_sprites)
    running = True
    clock = pg.time.Clock()
    fps = 30
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and hero.get_moves() == 0:
                    field.show_dice(dice)
                    moves = dice.handle_rotating()
                    if moves:
                        hero.add_moves(moves)
                else:
                    field.handle_move(event, hero, dice)
                    clock.tick(fps)
            field.render(screen, hero.get_moves(), hero.get_live())
        if dice.is_rotating():
            dice.rotate()
        all_sprites.update()
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(10)
    pg.quit()


if __name__ == '__main__':
    main()
