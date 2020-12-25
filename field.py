from random import choice
import pygame as pg
import os
from img_loader import ImageLoader
from cell import *
from hero import *
from dice import *


class Field(pg.sprite.Sprite, ImageLoader):

    def __init__(self, screen):
        super(Field, self).__init__()
        self.cells, self.screen, self.cell_size, self.left, self.top = None, None, None, None, None
        self.current_cell, self.frozen, self.finished = None, None, None
        self.start(screen)

    def start(self, screen, hero=None, dice=None):
        self.cells = [[None] * 12 for _ in range(12)]
        self.screen = screen
        screen_width, screen_height = screen.get_size()
        self.cell_size = 50
        self.left = screen_width // 2 - len(self.cells[0]) * self.cell_size // 2
        self.top = screen_height // 2 - len(self.cells) * self.cell_size // 2.25
        self.distribution_of_cells()
        self.current_cell = [0, 0]
        self.frozen = True
        self.finished = False
        if hero and dice:
            hero.start(self.current_cell, (self.left, self.top))
            dice.start()

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

    def at_finish(self):
        return (self.current_cell[0] == len(self.cells) - 1
                and self.current_cell[1] == len(self.cells) - 1)

    def is_finished(self):
        return self.finished

    def check_move(self):
        pass

    def end_screen(self, hero: Hero):
        img = pg.Surface((100, 100))
        print('cell passed: %d' % hero.get_passed_cells())

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
                    if callback == 'show-dice' and not self.at_finish():
                        self.show_dice(dice)
                if self.at_finish():
                    self.froze()
                    self.finished = True
                    self.end_screen(hero)

    def be_way(self, i, j) -> None:
        if str(self.cells[i][j]) != "finish":
            self.cells[i][j] = 'way'

    def get_size(self):
        return self.cell_size * len(self.cells[0]), self.cell_size * len(self.cells)

    def get_indent(self):
        return self.left, self.top

    def render(self, screen, moves, lives):
        screen.fill((20, 18, 32))
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
                    pg.draw.rect(screen, '#88001b', (self.left + self.cell_size * i, self.top + self.cell_size * j,
                                                 self.cell_size, self.cell_size))
                if str(self.cells[i][j]) != "finish":
                    screen.fill('#b4e9ff', (self.left + self.cell_size * i,
                                                         self.top + self.cell_size * j,
                                                         self.cell_size, self.cell_size))
                if str(self.cells[i][j]) == "way":
                    screen.fill(pg.Color('lightgreen'), (self.left + self.cell_size * i,
                                                         self.top + self.cell_size * j,
                                                         self.cell_size, self.cell_size))
                pg.draw.rect(screen, '#0a2fa2', (self.left + self.cell_size * i, self.top + self.cell_size * j,
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


def start_screen():
    pg.init()
    size = 700, 436
    screen = pg.display.set_mode(size)

    fon = ImageLoader.load_image('fon.png')
    screen.blit(fon, (0, 0))
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                pg.quit()
                return


def main():
    start_screen()
    pg.init()
    size = 760, 760
    screen = pg.display.set_mode(size)
    pg.display.set_caption('Goof the Game')
    all_sprites = pg.sprite.Group()
    field = Field(screen)
    hero = Hero((0, 0), field.get_indent(), all_sprites)
    dice = Dice(field.get_size(), field.get_indent(), all_sprites)
    field.start(screen, hero, dice)
    running = True
    clock = pg.time.Clock()
    fps = 30
    screen.fill((50, 41, 88))
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if hero.get_moves() == 0:
                        field.show_dice(dice)
                        moves = dice.handle_rotating()
                        if moves:
                            hero.add_moves(moves)
                    elif field.is_finished():
                        field.start(screen, hero, dice)
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