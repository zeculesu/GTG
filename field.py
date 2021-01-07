from random import choice
import pygame as pg
from typing import Union

from loader import Loader
from hero import FieldHero
from dice import Dice
from cell import Cell, Trap, Health, Task, Teleport


class Field(pg.sprite.Sprite, Loader):
    def __init__(self, screen: pg.Surface, group: pg.sprite.AbstractGroup):
        super(Field, self).__init__()
        self.group = group
        self.screen = screen
        self.cells = [[None] * 12 for _ in range(12)]
        self.cell_size = 50
        screen_width, screen_height = screen.get_size()
        self.left = screen_width // 2 - len(self.cells[0]) * self.cell_size // 2
        self.top = screen_height // 2 - len(self.cells) * self.cell_size // 2.25
        self.true_false_cell, self.current_cell, self.finish = None, None, None
        self.frozen, self.finished, self.moving_finish = None, None, None
        self.language = None
        self.current_game = None
        self.last_game = None
        self.task_active = False

    def start(self, hero: FieldHero, dice: Dice) -> None:
        if self.finish:
            self.cells[self.finish[0]][self.finish[1]] = None
        self.true_false_cell = [[None] * 12 for _ in range(12)]
        self.distribution_of_cells(hero)
        self.current_cell = [0, 0]
        self.language = 'en'
        self.frozen = True
        self.finished = False
        self.moving_finish = 0
        hero.start(self.current_cell, (self.left, self.top))
        dice.start()

    def distribution_of_cells(self, hero: FieldHero) -> None:
        options = {Cell: [0, 58],
                   Trap: [0, 40],
                   Health: [0, 20],
                   Task: [0, 100],
                   Teleport: [0, 60]}
        # options = {Task: [0, 144]}
        for i in range(12):
            for j in range(12):
                if i == 0 and j == 0:
                    continue
                elif i == len(self.cells[i]) - 1 and j == len(self.cells[i]) - 1:
                    self.cells[i][j] = 'finish'
                    self.finish = [i, j]
                    break
                option = choice(list(options.keys()))
                while option in self.get_sibling_cells(i, j) or options[option][0] + 1 > options[option][1]:
                    option = choice(list(options.keys()))
                options[option][0] += 1
                args = ((i, j, hero, self.top, self.left) if str(option) == "<class 'cell.Teleport'>"
                        else (hero,))
                self.cells[i][j] = option(*args)
                if options[option][1] <= options[option][0]:
                    del options[option]

    def get_sibling_cells(self, i: int, j: int) -> list:
        cells = ['self.cells[i - 1][j - 1]', 'self.cells[i - 1][j]', 'self.cells[i - 1][j + 1]',
                 'self.cells[i][j - 1]', 'self.cells[i][j + 1]',
                 'self.cells[i + 1][j - 1]', 'self.cells[i + 1][j]', 'self.cells[i + 1][j + 1]']
        square = []
        for cell in cells:
            try:
                if i == 0 or j == 0:
                    if 'i - 1' in cell or 'j - 1' in cell:
                        continue
                square.append(eval(cell))
            except IndexError:
                continue
        return square

    def at_finish(self) -> bool:
        return self.current_cell == self.finish

    def is_finished(self) -> bool:
        return self.finished

    def task_is_active(self) -> bool:
        return self.task_active

    def handle_move(self, event: pg.event.Event, hero: FieldHero, dice: Dice) -> Union[str, None]:
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
                    if hero.get_side() != 'left':
                        hero.change_side('left')
                    if self.current_cell[0] != 0:
                        move_allowed = True
                        self.be_way(i, j)
                        self.current_cell[0] -= 1
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    if hero.get_side() != 'right':
                        hero.change_side('right')
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
                            self.finished = True
                            if hero.get_side() != 'right':
                                hero.change_side('right')
                            return 'end-screen'
                    self.move_finish(hero)
                    if callback == 'show-dice' and not self.at_finish():
                        self.show_dice(dice)
                if self.at_finish():
                    self.froze()
                    self.finished = True
                    if hero.get_side() != 'right':
                        hero.change_side('right')
                    return 'end-screen'
            return None

    def move_finish(self, hero: FieldHero) -> None:
        if self.moving_finish < 3:
            if 'finish' in self.get_sibling_cells(self.current_cell[0], self.current_cell[1]):
                i, j = choice([0, 11]), choice([0, 11])
                while i == self.finish[0] and j == self.finish[1]:
                    i, j = choice([0, 11]), choice([0, 11])
                self.cells[self.finish[0]][self.finish[1]] = Cell(hero)
                self.cells[i][j] = 'finish'
                self.finish = [i, j]
                self.moving_finish += 1

    def paint(self, hero: FieldHero):
        i, j = self.current_cell
        self.true_false_cell[i][j] = True
        cell = self.cells[i][j]
        if isinstance(cell, Teleport):
            new_coords = cell.teleportation()
            if new_coords:
                i_new, j_new = new_coords
                self.current_cell = [i_new, j_new]
                hero.add_moves(1)
                hero.move_hero(self.current_cell, (self.left, self.top))
        elif isinstance(cell, Health):
            cell.add_health()
        elif isinstance(cell, Trap):
            cell.minus_health()
        elif isinstance(cell, Task):
            cell.number_of_special_cells('task')
            self.current_game = cell.start_game(self.screen, self, self.last_game)
            self.last_game = self.current_game.__class__
            self.task_active = True
        elif isinstance(cell, Cell):
            cell.number_of_special_cells('cell')

    def be_way(self, i, j) -> None:
        if str(self.cells[i][j]) != "finish" and not self.true_false_cell[i][j]:
            self.cells[i][j] = 'way'

    def get_size(self) -> tuple:
        return self.cell_size * len(self.cells[0]), self.cell_size * len(self.cells)

    def get_indent(self) -> tuple:
        return self.left, self.top

    def render(self, screen: pg.Surface, moves: int, lives: int, backGround) -> None:
        screen.fill([255, 255, 255])
        screen.blit(backGround.image, backGround.rect)
        pg.font.init()
        font = self.load_font('Special Elite.ttf', 36)
        if self.language == 'en':
            move = font.render('Moves - %d' % moves, True, pg.Color('#ebebeb'))
            live = font.render('Lives - %d' % lives, True, pg.Color('#ebebeb'))
        else:
            move = font.render('Ходы - %d' % moves, True, pg.Color('#ebebeb'))
            live = font.render('Жизни - %d' % lives, True, pg.Color('#ebebeb'))
        screen.blit(move, (self.left, 50))
        screen.blit(live, (510, 50))
        translate = {Task: 'yellow',
                     Teleport: 'purple',
                     Health: 'green',
                     Trap: 'orange',
                     Cell: '#ff4573'}
        image_translate = Loader.load_image('language.png')
        screen.blit(image_translate, image_translate.get_rect(
            bottomright=(40, 40)))
        for i in range(12):
            for j in range(12):
                # 92d4ec
                screen.fill('#ebebeb', (self.left + self.cell_size * i,
                                        self.top + self.cell_size * j,
                                        self.cell_size, self.cell_size))
                if str(self.cells[i][j]) == "finish":
                    pg.draw.rect(screen, '#fe1f18', (self.left + self.cell_size * i,
                                                     self.top + self.cell_size * j,
                                                     self.cell_size, self.cell_size))
                elif str(self.cells[i][j]) == "way":
                    screen.fill(pg.Color('#b4e9ff'), (self.left + self.cell_size * i,
                                                      self.top + self.cell_size * j,
                                                      self.cell_size, self.cell_size))
                elif self.true_false_cell[i][j]:
                    try:
                        pg.draw.rect(self.screen, translate[self.cells[i][j].__class__],
                                     (self.left + self.cell_size * i, self.top + self.cell_size * j,
                                      self.cell_size, self.cell_size))
                    except KeyError as e:
                        print('exception: %s' % e)
                        print(self.true_false_cell[i][j])
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

    def change_language(self):
        if self.language == 'en':
            self.language = 'ru'
        else:
            self.language = 'en'

    def get_language(self):
        return self.language

    def disable_task(self):
        self.task_active = False