import pygame as pg
from random import randint


class Cell:
    def __init__(self, hero):
        self.hero = hero
        self.active = True

    def is_active(self) -> bool:
        return self.active

    def disable(self):
        self.active = False

    def number_of_special_cells(self, cell):
        self.hero.add_quantity(cell)


class Trap(Cell):
    def __init__(self, hero):
        super(Trap, self).__init__(hero)

    def minus_health(self):
        if self.is_active():
            self.hero.add_live(-1)
            self.number_of_special_cells('trap')
            self.disable()


class Health(Cell):
    def __init__(self, hero):
        super(Health, self).__init__(hero)

    def add_health(self):
        if self.is_active():
            self.hero.add_live(1)
            self.number_of_special_cells('health')
            self.disable()


class Task(Cell):
    pass


class Teleport(Cell):
    def __init__(self, i, j, hero, top, left):
        self.i = i
        self.j = j
        self.top = top
        self.left = left
        super(Teleport, self).__init__(hero)

    def teleportation(self):
        if self.is_active():
            i_new, j_new = randint(1, 11), randint(1, 10)
            while randint(1, 11) == self.i and randint(1, 10) == self.j:
                i_new, j_new = randint(1, 11), randint(1, 10)
            self.hero.move_hero([i_new, j_new], (self.left, self.top))
            self.number_of_special_cells('teleport')
            self.disable()
            return [i_new, j_new]