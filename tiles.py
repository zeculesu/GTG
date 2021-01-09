import pygame as pg
from random import randint, choice

from loader import Loader


class ParticlesForRunninfInForest(pg.sprite.Sprite):
    schrub = pg.transform.smoothscale(Loader.load_image('schrub.png'), (130, 210))

    def __init__(self, group: pg.sprite.AbstractGroup, screen_size: tuple):
        super(ParticlesForRunninfInForest, self).__init__()
        screen_width, screen_height = screen_size
        self.image = ParticlesForRunninfInForest.schrub
        self.rect = self.image.get_rect()
        self.rect.y = int(screen_width * 0.8) - self.image.get_height() // 2
        self.rect.x = randint(screen_width * 1.5, screen_width * 2)
        self.velocity = 10
        self.mask = pg.mask.from_surface(self.image)
        group.add(self)

    def update(self):
        self.rect.x -= self.velocity


class ParticlesForStarFall(pg.sprite.Sprite):
    def __init__(self, rect, screen_size: tuple, image):
        super(ParticlesForStarFall, self).__init__()
        self.image = image
        self.rect = rect
        self.aktiv = True
        screen_width, screen_height = screen_size
        self.velocity = randint(2, 5)
        # while pg.sprite.spritecollideany(self, group):
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
            else:
                self.callback = '+'
        else:
            self.callback = None
            self.rect.y += self.velocity
            if self.rect.y < 0:
                self.remove()

    def get_callback(self):
        return self.callback


class Comet(Loader, ParticlesForStarFall):
    image = pg.transform.smoothscale(Loader.load_image('comet.png'), (200, 200))
    image_2 = pg.transform.smoothscale(Loader.load_image('comet.png'), (100, 100))
    image_3 = pg.transform.smoothscale(Loader.load_image('comet_2.png'), (200, 200))
    image_4 = pg.transform.smoothscale(Loader.load_image('comet_2.png'), (100, 100))

    def __init__(self, group: pg.sprite.AbstractGroup, screen_size: tuple):
        image = choice([Comet.image, Comet.image_2, Comet.image_3, Comet.image_4])
        super().__init__(self.image.get_rect(), screen_size, image)
        group.add(self)


class Star(Loader, ParticlesForStarFall):
    image = pg.transform.smoothscale(Loader.load_image('star.png'), (100, 100))
    image_2 = pg.transform.smoothscale(Loader.load_image('star.png'), (70, 70))

    def __init__(self, group: pg.sprite.AbstractGroup, screen_size: tuple):
        image = choice([Star.image, Star.image_2])
        super().__init__(self.image.get_rect(), screen_size, image)
        group.add(self)