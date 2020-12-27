import pygame as pg
from random import choice
from typing import Union

from img_loader import ImageLoader
from hero import Hero
from dice import Dice
from cell import Cell, Trap, Health, Task, Teleport
from savers import EndScreen


class Field(pg.sprite.Sprite, ImageLoader):
    def __init__(self, screen: pg.Surface, group):
        super(Field, self).__init__()
        self.cells, self.screen, self.cell_size, self.left, self.top = None, None, None, None, None
        self.current_cell, self.frozen, self.finished = None, None, None
        self.group = group
        self.start(screen)

    def start(self, screen, hero=None, dice=None):
        self.cells = [[None] * 12 for _ in range(12)]
        self.true_false_cell = [[None] * 12 for _ in range(12)]
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
        options = {Cell: [0, 58],
                   Trap: [0, 30],
                   Health: [0, 40],
                   Task: [0, 100],
                   Teleport: [0, 60]}
        for i in range(12):
            for j in range(12):
                if i == 0 and j == 0:
                    continue
                elif i == len(self.cells[i]) - 1 and j == len(self.cells[i]) - 1:
                    self.cells[i][j] = 'finish'
                    break
                option = choice(list(options.keys()))
                while option in self.get_sibling_cells(i, j) or options[option][0] + 1 > options[option][1]:
                    option = choice(list(options.keys()))
                options[option][0] += 1
                self.cells[i][j] = option
                if options[option][1] <= options[option][0]:
                    del options[option]

    def get_sibling_cells(self, i: int, j: int) -> list:
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

    def at_finish(self) -> bool:
        return (self.current_cell[0] == len(self.cells) - 1
                and self.current_cell[1] == len(self.cells) - 1)

    def is_finished(self) -> bool:
        return self.finished

    def handle_move(self, event: pg.event.Event, hero: Hero, dice: Dice) -> Union[str, None]:
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
                    if hero.get_moves() == 0:
                        self.paint(hero)
                        if hero.get_live() == 0:
                            self.froze()
                            EndScreen(hero, self.group)
                            callback = None
                    if callback == 'show-dice' and not self.at_finish():
                        self.show_dice(dice)
                if self.at_finish():
                    self.froze()
                    self.finished = True
                    print(hero.get_quantity())
                    return 'end-screen'
            return None

    def paint(self, hero):
        i, j = self.current_cell
        self.true_false_cell[i][j] = True
        if str(self.cells[i][j]) == "<class 'cell.Teleport'>":
            cell = Teleport(i, j, hero, self.top, self.left)
            i_new, j_new = cell.teleportation()
            self.current_cell = [i_new, j_new]
        if str(self.cells[i][j]) == "<class 'cell.Health'>":
            cell = Health(hero)
            cell.add_health()
        if str(self.cells[i][j]) == "<class 'cell.Trap'>":
            cell = Trap(hero)
            cell.minus_health()

    def be_way(self, i, j) -> None:
        if str(self.cells[i][j]) != "finish" and not self.true_false_cell[i][j]:
            self.cells[i][j] = 'way'

    def get_size(self) -> tuple:
        return self.cell_size * len(self.cells[0]), self.cell_size * len(self.cells)

    def get_indent(self) -> tuple:
        return self.left, self.top

    def render(self, screen: pg.Surface, moves: int, lives: int) -> None:
        screen.fill((20, 18, 32))
        pg.font.init()
        font = pg.font.Font('font/Special Elite.ttf', 36)
        move = font.render('Moves - %d' % moves, True, pg.Color('#80deea'))
        live = font.render('Lives - %d' % lives, True, pg.Color('#80deea'))
        screen.blit(move, (self.left, 50))
        screen.blit(live, (self.left + font.size('Количество ходов - %d' % moves)[0] + 150, 50))
        translate = {"<class 'cell.Task'>": 'yellow',
                     "<class 'cell.Teleport'>": 'purple',
                     "<class 'cell.Health'>": 'green',
                     "<class 'cell.Trap'>": 'orange',
                     "<class 'cell.Cell'>": 'black'}
        for i in range(12):
            for j in range(12):
                screen.fill('#b4e9ff', (self.left + self.cell_size * i,
                                        self.top + self.cell_size * j,
                                        self.cell_size, self.cell_size))
                if str(self.cells[i][j]) == "finish":
                    pg.draw.rect(screen, '#fe1f18', (self.left + self.cell_size * i, self.top + self.cell_size * j,
                                                     self.cell_size, self.cell_size))
                elif str(self.cells[i][j]) == "way":
                    screen.fill(pg.Color('lightgreen'), (self.left + self.cell_size * i,
                                                         self.top + self.cell_size * j,
                                                         self.cell_size, self.cell_size))
                elif self.true_false_cell[i][j]:
                    pg.draw.rect(self.screen, translate[str(self.cells[i][j])],
                                 (self.left + self.cell_size * i, self.top + self.cell_size * j,
                                  self.cell_size, self.cell_size))
                pg.draw.rect(screen, '#0a2fa2', (self.left + self.cell_size * i, self.top + self.cell_size * j,
                                                 self.cell_size, self.cell_size), 2)

    def get_current_cell(self) -> list:
        return self.current_cell

    def froze(self) -> None:
        self.frozen = not self.frozen

    def is_frozen(self) -> bool:
        return self.frozen

    def show_dice(self, dice: Dice) -> None:
        self.froze()
        dice.visibled()
        dice.rotating = True