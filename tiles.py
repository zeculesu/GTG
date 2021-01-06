import pygame as pg
from random import randint

from loader import Loader


class Comet(pg.sprite.Sprite, Loader):
    image = pg.transform.smoothscale(Loader.load_image('comet.png'), (400, 400))

    def __init__(self, group: pg.sprite.AbstractGroup, screen_size: tuple):
        super(Comet, self).__init__()
        self.rect = self.image.get_rect()
        screen_width, screen_height = screen_size
        # while pg.sprite.spritecollideany(self, group):
        self.rect.y = -randint(self.image.get_height(),
                               self.image.get_height() * 4)
        self.rect.x = randint(0, screen_width - self.image.get_width() // 2)
        group.add(self)
        self.velocity = randint(1, 5)

    def update(self):
        self.rect.y += self.velocity
        if self.rect.y < 0:
            self.remove()