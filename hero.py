import pygame as pg
from loader import Loader


class Hero(pg.sprite.Sprite, Loader):  # Родительский класс героя
    img_filename = 'hero_3.png'

    def __init__(self):
        self.image = None
        self.side = 'right'  # Изначальное положение
        super(Hero, self).__init__()

    def resize(self, width: int, height: int) -> None:  # Изменение размеров изображения
        self.image = pg.transform.scale(self.load_image(FieldHero.img_filename), (width, height))

    def get_side(self) -> str:  # Получение текущей стороны
        return self.side

    def change_side(self, side: str) -> None:  # Изменение текущей стороны
        self.side = side
        self.image = pg.transform.flip(self.image, True, False)


class FieldHero(Hero):  # Класс героя, находящегося на клетчатом поле
    def __init__(self, current_cell, indent, group: pg.sprite.AbstractGroup):
        super(FieldHero, self).__init__()
        group.add(self)
        self.resize(50, 50)  # Загружаем картинку и растягиваем под нужный размер
        # Служебные переменные
        self.lives, self.size_hero, self.moves, self.cells_passed = None, None, None, None
        self.quantity = None

        self.start(current_cell, indent)

    def start(self, current_cell: list, indent: tuple) -> None:  # Инициализация героя
        self.lives = 1  # Текущие жизни
        self.size_hero = 50  # Размер изображения героя
        if self.side != 'right':  # Установка изначально положения
            self.change_side('right')
        # Словарь-счётчик пройденных клеток
        self.quantity = {'passed': 0,
                         'task': 0,
                         'health': 0,
                         'trap': 0,
                         'teleport': 0,
                         'cell': 0}
        self.moves = 1  # герой вступает на поле
        self.move_hero(current_cell, indent)

    def get_quantity(self) -> dict:  # Получение словаря-счётчика
        return self.quantity

    def add_quantity(self, cell: str) -> None:  # Добавление в счётчик
        self.quantity[cell] += 1

    def get_lives(self) -> int:  # Получение текущих жизней
        return self.lives

    def move_hero(self, current_cell: list, indent: tuple):  # Передвижение героя по полю
        if self.moves != 0:
            self.moves -= 1
            self.quantity['passed'] += 1
            left, top = indent
            self.rect = self.image.get_rect(
                bottomright=(left + self.size_hero * (current_cell[0] + 1),
                             top + self.size_hero * (current_cell[1] + 1)))
            return 'show-dice' if self.moves == 0 else None

    def get_moves(self) -> int:  # Получение оставшихся ходов
        return self.moves

    def get_passed_cells(self) -> int:  # Получение общего числа пройденных клеток
        return self.quantity['passed']


class TaskHero(Hero):  # Родительский класс для героев в мини-играх
    step = None

    def __init__(self):
        super(TaskHero, self).__init__()
        self.resize(110, 110)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)  # Маска столкновений

    def set_step(self, step: int) -> None:  # Установить скорость героя
        self.step = step


class StarFallHero(TaskHero):  # Класс героя мини-игры "Звездопад"
    def make_move(self, event: pg.event.Event, screen_width: int) -> None:  # Передвижение
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


class RunningInForestHero(TaskHero):
    def __init__(self):
        super(RunningInForestHero, self).__init__()
        # Служебные переменные, падает ли герой или прыгает
        self.is_falling, self.is_jumping = False, False
        self.flying = 0  # Время, которое летит герой

    def make_move(self, event: pg.event.Event) -> None:  # Передвижение
        if event.key == pg.K_UP or event.key == pg.K_w:
            if not self.is_falling and not self.is_jumping and self.rect.y >= 358:
                self.is_jumping = True
                self.rect.y -= 25

    def update(self) -> None:  # Переписанная функция update в pg.sprite.Sprite
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
