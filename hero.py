import pygame as pg
from img_loader import ImageLoader


class Hero(pg.sprite.Sprite, ImageLoader):
    img_filename = 'itachi.jpg'

    def __init__(self, current_cell, indent, group: pg.sprite.AbstractGroup):
        self.image = self.load_image(Hero.img_filename)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.image.set_colorkey((255, 255, 255))
        super(Hero, self).__init__(group)
        self.live, self.size_hero, self.moves, self.cells_passed = None, None, None, None
        self.task_quantity, self.health_quantity = None, None
        self.trap_quantity, self.teleport_quantity = None, None
        self.start(current_cell, indent)

    def start(self, current_cell, indent):
        self.live = 3
        self.size_hero = 50
        self.task_quantity = 0
        self.health_quantity = 0
        self.trap_quantity = 0
        self.teleport_quantity = 0
        self.moves = 1  # герой вступает на поле
        self.cells_passed = -1
        self.move_hero(current_cell, indent)

    def get_quantity(self):
        return self.task_quantity, self.health_quantity, self.task_quantity, self.trap_quantity

    def add_quantity(self, cell):
        eval(f"self.{cell}_quantity += 1")

    def add_live(self, live: int) -> None:
        self.live += live

    def get_live(self) -> int:
        return self.live

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