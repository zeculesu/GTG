from pygame import Surface
from random import randint, choice
from games import StarFall, RunningInForest, MagicMaze
from typing import Union

from hero import FieldHero


GAMES = [StarFall, RunningInForest, MagicMaze]


class Cell:  # Наследуемый класс обычной клетки на поле
    color = '#ff4573'

    def __init__(self, hero: FieldHero):
        self.hero = hero  # Герой, стоящий на поле
        self.is_active = True  # Булево значение активности клетки - клетка активируется только 1 раз

    def disable(self):  # Отключает клетку
        self.is_active = False

    def number_of_special_cells(self, cell):  # Добавляет в подсчёт конкретную клетку
        if self.is_active:
            self.hero.add_quantity(cell)

    def get_color(self) -> str:  # Возвращает цвет клетки
        return self.color


class Trap(Cell):  # Клетка Капкан
    color = 'orange'

    def activate(self):
        if self.is_active:
            self.hero.lives -= 1
            self.number_of_special_cells(self.__class__.__name__.lower())
            self.disable()


class Health(Cell):  # Клетка Здоровье
    color = 'green'

    def activate(self):
        if self.is_active:
            self.hero.lives += 1
            self.number_of_special_cells(self.__class__.__name__.lower())
            self.disable()


class Task(Cell):  # Клетка Задание
    color = 'yellow'

    def start_game(self, surface: Surface, field, last_game: Union[StarFall.__class__,
                                                                   RunningInForest.__class__,
                                                                   MagicMaze.__class__]):
        if last_game:  # Проверка, чтобы при случайном выборе игры не попадалась предыдущая игра
            last_game_idx = GAMES.index(last_game)
            games = GAMES[:last_game_idx] + GAMES[last_game_idx + 1:]
        else:
            games = GAMES[:]
        game = choice(games)(field, surface, self.hero.get_lives(), field.sound_of_on)  # Инициализация игры
        game.start()
        return game


class Teleport(Cell):  # Клетка Телепорт
    color = 'purple'

    def __init__(self, i: int, j: int, hero: FieldHero, top: int, left: int):
        self.i = i  # Координата текущей клетки по высоте
        self.j = j  # Координата текущей клетки по ширине
        self.top = top  # Координата левого верхнего края поля по y
        self.left = left  # Координата левого верхнего края поля по x
        super(Teleport, self).__init__(hero)

    def teleportation(self):
        if self.is_active:
            i_new, j_new = randint(1, 11), randint(1, 10)  # Выбор случайной клетки на поле
            while randint(1, 11) == self.i and randint(1, 10) == self.j:
                i_new, j_new = randint(1, 11), randint(1, 10)
            self.hero.move_hero([i_new, j_new], (self.left, self.top))  # Передвижение героя
            self.number_of_special_cells(self.__class__.__name__.lower())
            self.disable()
            return [i_new, j_new]  # Возвращение координат новой клетки