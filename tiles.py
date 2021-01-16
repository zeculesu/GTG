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
        super().__init__(tiles_group, all_sprites)
        self.tile_type = tile_type
        self.pos_x, self.pos_y = pos_x, pos_y
        self.image = Tile.tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            80 * self.pos_x, 80 * self.pos_y)

    def shift_tile(self, pos_x: int, pos_y: int) -> None:
        self.pos_x += pos_x
        self.pos_y += pos_y
        self.rect = self.image.get_rect(
            bottomright=(80 * (self.pos_x + 1),
                         80 * (self.pos_y + 1)))


class FieldMagicMaze:
    def __init__(self, all_sprites: pg.sprite.AbstractGroup,
                 tiles_group: pg.sprite.AbstractGroup, hero: Hero):
        self.images = []
        self.current_cell, self.lambd = [4, 4], [0, 0]
        self.hero = hero
        self.generate_level(Loader.load_level('map_1.txt'), all_sprites, tiles_group)

    def generate_level(self, level: str, all_sprites: pg.sprite.AbstractGroup,
                       tiles_group: pg.sprite.AbstractGroup) -> None:
        for x in range(len(level)):
            self.images.append([])
            for y in range(len(level[x])):
                if level[x][y] == '.':
                    self.images[x].append(Tile('empty', x, y, all_sprites, tiles_group))
                elif level[x][y] == '#':
                    self.images[x].append(Tile('wall', x, y, all_sprites, tiles_group))
                elif level[x][y] == '@':
                    self.images[x].append(Tile('finish', x, y, all_sprites, tiles_group))

    def move(self, event: pg.event.Event) -> Union[str, None]:
        x, y = self.current_cell[0], self.current_cell[1]
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                if self.hero.get_side() != 'left':
                    self.hero.change_side('left')
                if self.images[x - 1][y].tile_type != 'wall':
                    self.current_cell[0] -= 1
                    self.lambd[0] += 1
            elif event.key == pg.K_RIGHT:
                if self.hero.get_side() != 'right':
                    self.hero.change_side('right')
                if self.images[x + 1][y].tile_type != 'wall':
                    self.current_cell[0] += 1
                    self.lambd[0] -= 1
            elif event.key == pg.K_UP and self.images[x][y - 1].tile_type != 'wall':
                self.current_cell[1] -= 1
                self.lambd[1] += 1
            elif event.key == pg.K_DOWN and self.images[x][y + 1].tile_type != 'wall':
                self.current_cell[1] += 1
                self.lambd[1] -= 1
            self.shift_tiles(*self.lambd)
            if self.images[x][y].tile_type == 'finish':
                return 'finish'
            return None

    def shift_tiles(self, pos_x: int, pos_y: int) -> None:
        self.lambd = [0, 0]
        for line in self.images:
            for tile in line:
                tile.shift_tile(pos_x, pos_y)


class ParticlesForRunningInForest(pg.sprite.Sprite):
    schrub = pg.transform.smoothscale(Loader.load_image('fire.png'), (130, 210))
    fire_sound = Loader.load_sound('fire.wav')
    fire_sound.set_volume(0.05)

    def __init__(self, velocity: int, group: pg.sprite.AbstractGroup, screen_size: tuple):
        super(ParticlesForRunningInForest, self).__init__()
        self.screen_width, self.screen_height = screen_size
        self.image = ParticlesForRunningInForest.schrub
        self.rect = self.image.get_rect()
        self.rect.y = int(self.screen_width * 0.8) - self.image.get_height() // 2
        other_sprites = group.sprites()
        length = velocity * 50
        x = None
        while not x or any(map(lambda spr: abs(spr.rect.x - x) < length, other_sprites)):
            x = randint(self.screen_width * 1.25, self.screen_width * 4)
        self.rect.x = x
        self.velocity = velocity
        self.mask = pg.mask.from_surface(self.image)
        self.callback = None
        group.add(self)

    def get_callback(self):
        return self.callback

    def update(self, hero):
        self.rect.x -= self.velocity
        if pg.sprite.collide_mask(self, hero):
            ParticlesForRunningInForest.fire_sound.play()
            self.callback = 'loss'
        if self.rect.x < -self.image.get_width():
            self.kill()


class ParticlesForStarFall(pg.sprite.Sprite):
    stars_sound = Loader.load_sound('stars.wav')
    comet_sound = Loader.load_sound('comet_2.wav')
    comet_sound.set_volume(0.05)
    stars_sound.set_volume(0.05)

    def __init__(self, rect, screen_size: tuple, image):
        super(ParticlesForStarFall, self).__init__()
        self.image = image
        self.rect = rect
        self.aktiv = True
        screen_width, screen_height = screen_size
        self.velocity = randint(2, 5)
        self.rect.y = -randint(self.image.get_height(),
                               self.image.get_height() * 4)
        self.rect.x = randint(0, screen_width - self.image.get_width() // 2)
        self.mask = pg.mask.from_surface(self.image)
        self.callback = None

    def update(self, hero):
        if pg.sprite.collide_mask(self, hero) and self.aktiv:
            self.aktiv = not self.aktiv
            if isinstance(self, Comet):
                self.callback = '-'
                ParticlesForStarFall.comet_sound.play()
            else:
                self.callback = '+'
                ParticlesForStarFall.stars_sound.play()
        else:
            self.callback = None
            self.rect.y += self.velocity
            if self.rect.y < 0:
                self.remove()

    def get_callback(self) -> bool:
        return self.callback


class Comet(Loader, ParticlesForStarFall):
    image = pg.transform.smoothscale(Loader.load_image('comet.png'), (200, 200))
    image_2 = pg.transform.smoothscale(Loader.load_image('comet.png'), (100, 100))
    image_3 = pg.transform.smoothscale(Loader.load_image('comet_2.png'), (200, 200))
    image_4 = pg.transform.smoothscale(Loader.load_image('comet_2.png'), (100, 100))

    def __init__(self, group: pg.sprite.AbstractGroup, screen_size: tuple):
        image = choice([Comet.image, Comet.image_2, Comet.image_3, Comet.image_4])
        super(Comet, self).__init__(self.image.get_rect(), screen_size, image)
        group.add(self)


class Star(Loader, ParticlesForStarFall):
    image = pg.transform.smoothscale(Loader.load_image('star.png'), (100, 100))
    image_2 = pg.transform.smoothscale(Loader.load_image('star.png'), (70, 70))

    def __init__(self, group: pg.sprite.AbstractGroup, screen_size: tuple):
        image = choice([Star.image, Star.image_2])
        super(Star, self).__init__(self.image.get_rect(), screen_size, image)
        group.add(self)
