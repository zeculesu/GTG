from pygame import Surface
from random import randint, choice
from games import StarFall
from typing import Union

from hero import FieldHero
# from field import Field


GAMES = [StarFall]


class Cell:
    def __init__(self, hero):
        self.hero = hero
        self.active = True

    def is_active(self) -> bool:
        return self.active

    def disable(self):
        self.active = False

    def number_of_special_cells(self, cell):
        if self.is_active():
            self.hero.add_quantity(cell)


class Trap(Cell):
    def minus_health(self):
        if self.is_active():
            self.hero.add_live(-1)
            self.number_of_special_cells('trap')
            self.disable()


class Health(Cell):
    def add_health(self):
        if self.is_active():
            self.hero.add_live(1)
            self.number_of_special_cells('health')
            self.disable()


class Task(Cell):
    def start_game(self, surface: Surface, field, last_game: Union[StarFall]):
        # if last_game:
        #     last_game_idx = GAMES.index(last_game)
        #     games = GAMES[:last_game_idx] + GAMES[last_game_idx + 1:]
        # else:
        games = GAMES[:]
        game = choice(games)(field, surface, self.hero.get_live())  # initialization of a game
        game.start()
        return game


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