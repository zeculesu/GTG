import pygame as pg
from loader import Loader


class Hero(pg.sprite.Sprite, Loader):
    img_filename = 'hero_3.png'

    def __init__(self):
        self.image = None
        self.side = 'right'
        super(Hero, self).__init__()

    def resize(self, width: int, height: int) -> None:
        self.image = pg.transform.scale(self.load_image(FieldHero.img_filename), (width, height))

    def get_side(self) -> str:
        return self.side

    def change_side(self, side: str) -> None:
        self.side = side
        self.image = pg.transform.flip(self.image, True, False)


class FieldHero(Hero):
    def __init__(self, current_cell, indent, group: pg.sprite.AbstractGroup):
        super(FieldHero, self).__init__()
        group.add(self)
        self.resize(50, 50)  # Загружаем картинку и растягиваем под нужный размер
        self.live, self.size_hero, self.moves, self.cells_passed = None, None, None, None
        self.quantity = None

        self.start(current_cell, indent)

    def start(self, current_cell: list, indent: tuple) -> None:
        self.live = 1
        self.size_hero = 50
        if self.side != 'right':
            self.change_side('right')
        self.quantity = {'passed': 0,
                         'task': 0,
                         'health': 0,
                         'trap': 0,
                         'teleport': 0,
                         'cell': 0}
        self.moves = 1  # герой вступает на поле
        self.cells_passed = -1
        self.move_hero(current_cell, indent)

    def get_quantity(self) -> dict:
        return self.quantity

    def add_quantity(self, cell: str) -> None:
        self.quantity[cell] += 1

    def add_live(self, live: int) -> None:
        self.live += live

    def get_live(self) -> int:
        return self.live

    def move_hero(self, current_cell: list, indent: tuple):
        if self.moves != 0:
            self.moves -= 1
            self.quantity['passed'] += 1
            left, top = indent
            self.rect = self.image.get_rect(
                bottomright=(left + self.size_hero * (current_cell[0] + 1),
                             top + self.size_hero * (current_cell[1] + 1)))
            return 'show-dice' if self.moves == 0 else None

    def get_moves(self) -> int:
        return self.moves

    def add_moves(self, moves: int) -> None:
        self.moves += moves

    def get_passed_cells(self) -> int:
        return self.quantity['passed']


class TaskHero(Hero):
    def __init__(self):
        super(TaskHero, self).__init__()
        self.resize(110, 110)
        self.rect = self.image.get_rect()
        self.falls = None
        self.mask = pg.mask.from_surface(self.image)


class StarFallHero(TaskHero):
    step = None

    def make_move(self, event: pg.event.Event, screen_width: int) -> None:
        if event.key == pg.K_LEFT or event.key == pg.K_a:
            if self.rect.x - self.step >= self.image.get_width() * 0.1:
                self.rect.x -= self.step
                if self.get_side() != 'left':
                    self.change_side('left')
        elif event.key == pg.K_RIGHT or event.key == pg.K_d:
            if self.rect.x + self.step <= screen_width - self.image.get_width():
                self.rect.x += self.step
                if self.get_side() != 'right':
                    self.change_side('right')

    def set_step(self, step: int) -> None:
        self.step = step


class RunningInForestHero(TaskHero):
    def __init__(self):
        super(RunningInForestHero, self).__init__()
        self.is_falling, self.is_jumping = False, False
        self.flying = 0

    def make_move(self, event: pg.event.Event) -> None:
        if event.key == pg.K_UP or event.key == pg.K_w:
            if not self.is_falling and not self.is_jumping and self.rect.y >= 358:
                self.is_jumping = True
                self.rect.y -= 25

    def update(self) -> None:
        if self.is_jumping:
            self.rect.y -= 10
            if self.rect.y <= 358:
                self.is_jumping = False
                self.flying += 1
        if self.flying > 0:
            self.flying += 1
            if self.flying == 15:
                self.flying = 0
                self.is_falling = True
        if self.is_falling:
            self.rect.y += 5
            if self.rect.y >= 608:
                self.is_falling = False