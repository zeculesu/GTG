from random import choice
import pygame as pg
from typing import Union

from loader import Loader
from hero import FieldHero
from dice import Dice
from cell import Cell, Trap, Health, Task, Teleport


class Field:  # Основное клетчатое поле
    fontname = 'Special Elite.ttf'  # Общий шрифт для всех надписей, связанных с полем

    def __init__(self, screen: pg.Surface):
        self.screen = screen  # Основной экран
        self.cells = [[None] * 12 for _ in range(12)]  # Пустое поле
        self.cell_size = 50  # Размер клетки

        self.width = self.cell_size * len(self.cells[0])  # Ширина поля в пикселях
        self.height = self.cell_size * len(self.cells)  # Высота поля в пикселях

        self.screen_width, self.screen_height = screen.get_size()  # Ширина и высота экрана
        self.x = int(self.screen_width // 2 - len(self.cells[0]) * self.cell_size // 2)
        self.y = int(self.screen_height // 2 - len(self.cells) * self.cell_size // 2.25)

        # Служебные переменные
        self.true_false_cell, self.current_cell, self.finish = None, None, None
        self.frozen, self.finished, self.moving_finish = None, None, None
        self.current_game, self.last_game = None, None
        self.task_active = None
        self.sound_active = True

        self.language = 'en'  # Начальный язык
        self.translate = {'en': {'moves': 'Moves',  # Словарь перевода надписей
                                 'lives': 'Lives'},
                          'ru': {'moves': 'Ходы',
                                 'lives': 'Жизни'}}

    def start(self, hero: FieldHero, dice: Dice) -> None:  # Функция начала игры
        if self.finish:  # Если финиш есть в служебной переменной - убрать его
            self.cells[self.finish[0]][self.finish[1]] = None
        self.true_false_cell = [[None] * 12 for _ in range(12)]
        self.distribution_of_cells(hero)  # Вызов функции распределения клеток
        self.current_cell = [0, 0]  # Координаты текущей клетки
        self.frozen = True  # Булево значение замороженности поля
        self.finished = False  # Булево значение завершённости игры
        self.moving_finish = 0  # Количество перемещения финиша
        hero.start(self.current_cell, (self.x, self.y))  # Вызов функции начала игры у героя
        dice.show()  # Вызов функции запуска костей

    def distribution_of_cells(self, hero: FieldHero) -> None:  # Функция распределения клеток
        # Предельные допустимые значения клеток
        options = {Cell: [0, 58],
                   Trap: [0, 40],
                   Health: [0, 20],
                   Task: [0, 100],
                   Teleport: [0, 60]}
        for i in range(12):
            for j in range(12):
                if i == 0 and j == 0:
                    continue
                # Определение финиша
                elif i == len(self.cells[i]) - 1 and j == len(self.cells[i]) - 1:
                    self.cells[i][j] = 'finish'
                    self.finish = [i, j]
                    break
                # Распределение клеток без соседства с похожими
                option = choice(list(options.keys()))
                while option in self.get_sibling_cells(i, j) or options[option][0] + 1 > options[option][1]:
                    option = choice(list(options.keys()))
                options[option][0] += 1
                # Уточнение аргументов для инициализации разных классов
                args = ((i, j, hero, self.y, self.x) if str(option) == "<class 'cell.Teleport'>"
                        else (hero,))
                self.cells[i][j] = option(*args)
                if options[option][1] <= options[option][0]:
                    del options[option]

    # Функция получения соседей клетки (квадрат 3x3)
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

    # Функция логистики передвижения по полю
    def handle_move(self, event: pg.event.Event, hero: FieldHero, dice: Dice) -> Union[str, None]:
        if not self.frozen:
            i, j = self.current_cell
            move_allowed = False
            if hero.get_moves() > 0:  # Если есть ходы, то ...
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
                if move_allowed:  # Если герой двигается не в стенку
                    callback = hero.move_hero(self.current_cell, (self.x, self.y))
                    if hero.get_moves() == 0:  # Если ходов не осталось - герой остановился
                        self.activate_cell(hero)  # Активация текущей клетки
                        if hero.get_lives() == 0:  # Если герой теряет последнюю жизнь
                            self.freeze()  # Заморозка поля
                            self.finished = True  # Статус завершения игры
                            return 'loss'
                    self.move_finish(hero)  # Иначе проверяем, нужно ли двигать финиш
                    # Если функция говорит нам о том, что всё в порядке - запускаем кости
                    if callback == 'show-dice' and not self.at_finish():
                        self.show_dice(dice)
                if self.at_finish():  # Если герой оказался на финише
                    self.freeze()
                    self.finished = True
                    return 'victory'
            return None

    # Функция отрисовки поля
    def render(self, screen: pg.Surface, moves: int, lives: int, background) -> None:
        if self.sound_active:
            pg.mixer.unpause()
        else:
            pg.mixer.pause()
        screen.fill([255, 255, 255])  # Заполнение экрана чёрным экраном
        screen.blit(background.image, background.rect)  # Отрисовка заднего фона
        font = Loader.load_font(Field.fontname, 36)  # Инициализация шрифта
        move = font.render('%s - %d' % (self.translate[self.language]['moves'], moves),
                           True, pg.Color('#ebebeb'))  # Надпись ходов
        live = font.render('%s - %d' % (self.translate[self.language]['lives'], lives),
                           True, pg.Color('#ebebeb'))  # Надпись жизней
        screen.blit(move, (self.x,
                           self.y - int(move.get_height() * 1.5)))
        screen.blit(live, ((self.x + self.width) - live.get_width(),
                           self.y - int(live.get_height() * 1.5)))
        for i in range(12):
            for j in range(12):
                cell = self.cells[i][j]
                true_false_cell = self.true_false_cell[i][j]
                screen.fill('#ebebeb', (self.x + self.cell_size * i,
                                        self.y + self.cell_size * j,
                                        self.cell_size, self.cell_size))
                if cell == "finish":
                    pg.draw.rect(screen, '#fe1f18', pg.Rect(self.x + self.cell_size * i,
                                                            self.y + self.cell_size * j,
                                                            self.cell_size, self.cell_size))
                elif cell == "way":
                    screen.fill(pg.Color('#b4e9ff'), (self.x + self.cell_size * i,
                                                      self.y + self.cell_size * j,
                                                      self.cell_size, self.cell_size))
                elif true_false_cell:  # Если это клетка, на которой остановился герой
                    pg.draw.rect(self.screen, cell.get_color(),
                                 pg.Rect(self.x + self.cell_size * i,
                                         self.y + self.cell_size * j,
                                         self.cell_size, self.cell_size))
                pg.draw.rect(screen, '#0a2fa2', pg.Rect(self.x + self.cell_size * i,
                                                        self.y + self.cell_size * j,
                                                        self.cell_size, self.cell_size), 2)

    def at_finish(self) -> bool:  # Проверяет, стоит ли герой на финише
        return self.current_cell == self.finish

    def is_finished(self) -> bool:  # Возвращает состояние завершённости игры
        return self.finished

    def task_is_active(self) -> bool:  # Возвращает, активна ли сейчас мини-игра
        return self.task_active

    def activate_cell(self, hero: FieldHero) -> None:  # Активирует клетку
        i, j = self.current_cell
        self.true_false_cell[i][j] = True
        cell = self.cells[i][j]
        if isinstance(cell, Teleport):
            new_coords = cell.teleportation()
            if new_coords:
                i_new, j_new = new_coords
                self.current_cell = [i_new, j_new]
                hero.moves += 1
                hero.move_hero(self.current_cell, (self.x, self.y))
        elif any(map(lambda x: isinstance(cell, x), [Health, Trap])):
            cell.activate()
        elif isinstance(cell, Task):
            cell.number_of_special_cells(cell.__class__.__name__.lower())
            self.current_game = cell.start_game(self.screen, self, self.last_game)
            self.last_game = self.current_game.__class__
            self.task_active = True
        elif isinstance(cell, Cell):
            cell.number_of_special_cells(cell.__class__.__name__.lower())

    def be_way(self, i: int, j: int) -> None:  # Красит пройденные клетки
        if self.cells[i][j] != "finish" and not self.true_false_cell[i][j]:
            self.cells[i][j] = 'way'

    def move_finish(self, hero: FieldHero) -> None:  # Передвинуть финиш при необходимости
        if self.moving_finish < 2:
            if 'finish' in self.get_sibling_cells(self.current_cell[0], self.current_cell[1]):
                i, j = choice([0, 11]), choice([0, 11])
                while i == self.finish[0] and j == self.finish[1]:
                    i, j = choice([0, 11]), choice([0, 11])
                self.cells[self.finish[0]][self.finish[1]] = Cell(hero)
                self.cells[i][j] = 'finish'
                self.finish = [i, j]
                self.moving_finish += 1

    def disable_task(self) -> None:  # Отключить мини-игру
        self.task_active = False

    def freeze(self) -> None:  # Заморозить/разморозить поле
        self.frozen = not self.frozen

    def is_frozen(self) -> bool:  # Возвращает булево значение, заморожено ли поле
        return self.frozen

    def show_dice(self, dice: Dice) -> None:  # Служебная функция костей для поля
        self.freeze()
        dice.show()

    def get_size(self) -> tuple:  # Возвращает размеры поля в пикселях
        return self.width, self.height

    def get_indent(self) -> tuple:  # Возвращает координаты поля
        return self.x, self.y

    def get_current_cell(self) -> list:  # Возвращает координаты текущей клетки
        return self.current_cell

    def change_language(self) -> None:  # Меняет текущий язык
        self.language = 'ru' if self.language == 'en' else 'en'

    def get_language(self) -> str:  # Возвращает текущий язык
        return self.language

    def handle_sound(self):
        self.sound_active = not self.sound_active

    def sound_is_active(self) -> bool:
        return self.sound_active
