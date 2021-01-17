import pygame as pg
from typing import Union
from random import randint, choice

from loader import Loader
from hero import Hero


class Tile(pg.sprite.Sprite):
    tile_images = {
        'wall': pg.transform.smoothscale(Loader.load_image('tile.png'), (80, 80)),
        'empty': pg.transform.smoothscale(Loader.load_image('pol.jpg'), (80, 80)),
        'finish': pg.transform.smoothscale(Loader.load_image('finish.png'), (80, 80))
    }

    def __init__(self, tile_type: str, pos_x: int, pos_y: int, all_sprites: pg.sprite.AbstractGroup,
                 tiles_group: pg.sprite.AbstractGroup):
        super(Tile, self).__init__(tiles_group, all_sprites)
        self.tile_type = tile_type  # тип тайла
        self.pos_x, self.pos_y = pos_x, pos_y  # координаты
        self.image = Tile.tile_images[tile_type]  # выбираем нужную картинку
        self.rect = self.image.get_rect().move(  # ставим на нужное место
            80 * self.pos_x, 80 * self.pos_y)

    def shift_tile(self, pos_x: int, pos_y: int) -> None:  # сдвиг тайлов
        self.pos_x += pos_x
        self.pos_y += pos_y
        self.rect = self.image.get_rect(
            bottomright=(80 * (self.pos_x + 1),
                         80 * (self.pos_y + 1)))


class FieldMagicMaze:  # лабиринт
    def __init__(self, all_sprites: pg.sprite.AbstractGroup,
                 tiles_group: pg.sprite.AbstractGroup, hero: Hero):
        self.images = []
        self.hero = hero
        self.lambd = [0, 0]  # сдвиг для тайлов
        self.current_map = choice(['map_1.txt', 'map_2.txt'])  # случайно выбираем карту
        self.current_cell = [4, 4] if self.current_map == 'map_1.txt' else [5, 5]  # задаём текучую клетку
        self.generate_level(Loader.load_level(self.current_map), all_sprites, tiles_group)  # генерируем уровень

    def get_current_map(self) -> str:  # возвращаем текущую карту
        return self.current_map

    def generate_level(self, level: list, all_sprites: pg.sprite.AbstractGroup,
                       tiles_group: pg.sprite.AbstractGroup) -> None:  # генерируем карту
        for x in range(len(level)):
            self.images.append([])
            for y in range(len(level[x])):
                if level[x][y] == '.':  # пустая
                    self.images[x].append(Tile('empty', x, y, all_sprites, tiles_group))  # создаём обьект тайла
                elif level[x][y] == '#':  # стена
                    self.images[x].append(Tile('wall', x, y, all_sprites, tiles_group))  # создаём обьект тайла
                elif level[x][y] == '@':  # финиш
                    self.images[x].append(Tile('finish', x, y, all_sprites, tiles_group))  # создаём обьект тайла

    def move(self, event: pg.event.Event) -> Union[str, None]:
        x, y = self.current_cell  # координаты текущей клетки
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                if self.hero.get_side() != 'left':  # меняем сторону героя
                    self.hero.change_side('left')
                if self.images[x - 1][y].tile_type != 'wall':  # если не стена двигаемся
                    self.current_cell[0] -= 1
                    self.lambd[0] += 1
            elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                if self.hero.get_side() != 'right':  # меняем сторону героя
                    self.hero.change_side('right')
                if self.images[x + 1][y].tile_type != 'wall':  # если не стена двигаемся
                    self.current_cell[0] += 1
                    self.lambd[0] -= 1
            elif ((event.key == pg.K_UP or event.key == pg.K_w)
                  and self.images[x][y - 1].tile_type != 'wall'):  # если не стена двигаемся
                self.current_cell[1] -= 1
                self.lambd[1] += 1
            elif ((event.key == pg.K_DOWN or event.key == pg.K_s)
                  and self.images[x][y + 1].tile_type != 'wall'):  # если не стена двигаемся
                self.current_cell[1] += 1
                self.lambd[1] -= 1
            self.shift_tiles(*self.lambd)  # двигаем тайлы
            x, y = self.current_cell
            if self.images[x][y].tile_type == 'finish':  # если финиш возвращаем победу
                return 'finish'
            return None

    def shift_tiles(self, pos_x: int, pos_y: int) -> None:  # сдвиг тайлов
        self.lambd = [0, 0]  # очищаем сдвиг
        for line in self.images:
            for tile in line:
                tile.shift_tile(pos_x, pos_y)  # передаём куда надо сдвинуть каждый тайл


class ParticlesForRunningInForest(pg.sprite.Sprite):
    schrub = pg.transform.smoothscale(Loader.load_image('fire.png'), (130, 210))  # загружаем картинку
    fire_sound = Loader.load_sound('fire.wav')  # подгружаем музычку для огонька
    fire_sound.set_volume(0.05)

    def __init__(self, velocity: int, group: pg.sprite.AbstractGroup, screen_size: tuple):
        super(ParticlesForRunningInForest, self).__init__()
        self.screen_width, self.screen_height = screen_size
        self.image = ParticlesForRunningInForest.schrub
        self.rect = self.image.get_rect()
        self.rect.y = int(self.screen_width * 0.8) - self.image.get_height() // 2  # задаём координату y
        other_sprites = group.sprites()
        length = velocity * 50  # расстояние между огоньками
        x = None
        while not x or any(map(lambda spr: abs(spr.rect.x - x) < length,
                               other_sprites)):  # расставляем, чтобы были далеко друг от друга
            x = randint(self.screen_width * 1.25, self.screen_width * 1.5)
        self.rect.x = x
        self.velocity = velocity  # задаём скорость
        self.mask = pg.mask.from_surface(self.image)  # создаём маску
        self.callback = None
        group.add(self)

    def get_callback(self):  # возращаем коллбек
        return self.callback

    def update(self, hero):
        self.rect.x -= self.velocity
        if pg.sprite.collide_mask(self, hero):  # если огонёк коснулся героя, то возвращаем проигрыш
            ParticlesForRunningInForest.fire_sound.play()  # врубаем музычку сгорания героя
            self.callback = 'loss'
        if self.rect.x < -self.image.get_width():  # если уходит из поля видимости убиваем спрайт
            self.kill()


class ParticlesForStarFall(pg.sprite.Sprite):  # родительский класс для объектов игры
    stars_sound = Loader.load_sound('stars.wav')  # музычка для звёзд
    comet_sound = Loader.load_sound('comet_2.wav')  # музычка для комет
    comet_sound.set_volume(0.05)
    stars_sound.set_volume(0.05)

    def __init__(self, rect, screen_size: tuple, image):
        super(ParticlesForStarFall, self).__init__()
        self.image = image
        self.rect = rect
        screen_width, screen_height = screen_size  # передаём размеры экрана
        self.velocity = randint(2, 5)  # ставим случайную скорость
        self.rect.y = -randint(self.image.get_height(),
                               self.image.get_height() * 4)
        self.rect.x = randint(0, screen_width - self.image.get_width() // 2)
        self.mask = pg.mask.from_surface(self.image)
        self.callback = None

    def update(self, hero):
        if pg.sprite.collide_mask(self, hero):
            if isinstance(self, Comet):  # если коснулся кометы, забираем жизнь
                self.callback = '-'
                ParticlesForStarFall.comet_sound.play()  # музычка касания
            else:
                self.callback = '+'  # если коснулся звёзды, увеличиваем кол-во собранных звёзд
                ParticlesForStarFall.stars_sound.play()  # мызчка касания
        else:
            self.rect.y += self.velocity  # иначе объект продолжает падать
            if self.rect.y < 0:  # если скрылся из поля видимости, удаляем
                self.remove()

    def get_callback(self) -> bool:  # возвращаем коллбэк
        return self.callback


class Comet(Loader, ParticlesForStarFall):  # класс комет
    image = pg.transform.smoothscale(Loader.load_image('comet.png'), (200, 200))  # подгружаем картинки разных размеров
    image_2 = pg.transform.smoothscale(Loader.load_image('comet.png'), (100, 100))
    image_3 = pg.transform.smoothscale(Loader.load_image('comet_2.png'), (200, 200))
    image_4 = pg.transform.smoothscale(Loader.load_image('comet_2.png'), (100, 100))

    def __init__(self, group: pg.sprite.AbstractGroup, screen_size: tuple):
        image = choice([Comet.image, Comet.image_2, Comet.image_3, Comet.image_4])  # случайно выбираем картинку
        super(Comet, self).__init__(self.image.get_rect(), screen_size, image)
        group.add(self)


class Star(Loader, ParticlesForStarFall):  # класс звёзд
    image = pg.transform.smoothscale(Loader.load_image('star.png'), (100, 100))  # подгружаем картинки
    image_2 = pg.transform.smoothscale(Loader.load_image('star.png'), (70, 70))

    def __init__(self, group: pg.sprite.AbstractGroup, screen_size: tuple):
        image = choice([Star.image, Star.image_2])  # случайно выбираем одну из картинок
        super(Star, self).__init__(self.image.get_rect(), screen_size, image)
        group.add(self)
