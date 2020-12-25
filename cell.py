import pygame as pg
from random import randint


class Cell:
    def __init__(self, hero):
        self.hero = hero

    def number_of_special_cells(self, cell):
        self.hero.add_quantity(cell)


class Trap(Cell):
    img_name = 'trap.png'

    def __init__(self, hero):
        super().__init__(hero)

    def minus_health(self):
        self.hero.add_live(-1)
        self.number_of_special_cells('trap')


class Health(Cell):
    def __init__(self, hero):
        super().__init__(hero)

    def add_health(self):
        self.hero.add_live(1)
        self.number_of_special_cells('health')


class Task(Cell):
    pass


class Teleport(Cell):
    def __init__(self, i, j, hero, top, left):
        self.i = i
        self.j = j
        self.top = top
        self.left = left
        super().__init__(hero)

    def teleportation(self):
        i_new, j_new = randint(1, 11), randint(1, 10)
        while randint(1, 11) == self.i and randint(1, 10) == self.j:
            i_new, j_new = randint(1, 11), randint(1, 10)
        self.hero.move_hero([i_new, j_new], (self.left, self.top))
        self.number_of_special_cells('teleport')
        return [i_new, j_new]
