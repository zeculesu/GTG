import pygame as pg
from loader import Loader


class Hero(pg.sprite.Sprite, Loader):
    img_filename = 'hero_3.png'

    def __init__(self, current_cell, indent, group: pg.sprite.AbstractGroup):
        self.image = self.load_image(Hero.img_filename)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.image.set_colorkey((255, 255, 255))
        self.side = None
        super(Hero, self).__init__(group)
        self.live, self.size_hero, self.moves, self.cells_passed = None, None, None, None
        self.quantity = {'task': None,
                         'health': None,
                         'trap': None,
                         'teleport': None,
                         'cell': None}
        self.start(current_cell, indent)

    def get_side(self):
        return self.side

    def start(self, current_cell, indent):
        self.live = 1
        self.size_hero = 50
        self.side = 'right'
        self.quantity = {'task': 0,
                         'health': 0,
                         'trap': 0,
                         'teleport': 0,
                         'cell': 0}
        self.moves = 1  # герой вступает на поле
        self.cells_passed = -1
        self.move_hero(current_cell, indent)

    def get_quantity(self):
        return self.quantity

    def add_quantity(self, cell):
        self.quantity[cell] += 1

    def add_live(self, live: int) -> None:
        self.live += live

    def get_live(self) -> int:
        return self.live

    def change_side(self, side):
        self.side = side
        self.image = pg.transform.flip(self.image, True, False)

    def move_hero(self, current_cell, indent):
        if self.moves != 0:
            self.moves -= 1
            self.cells_passed += 1
            left, top = indent
            self.rect = self.image.get_rect(
                bottomright=(left + self.size_hero * (current_cell[0] + 1),
                             top + self.size_hero * (current_cell[1] + 1)))
            return 'show-dice' if self.moves == 0 else None

    def get_moves(self) -> int:
        return self.moves

    def add_moves(self, moves) -> None:
        self.moves += moves

    def get_passed_cells(self) -> int:
        return self.cells_passed