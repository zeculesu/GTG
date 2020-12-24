import pygame as pg
from img_loader import ImageLoader


class Hero(pg.sprite.Sprite, ImageLoader):
    img_filename = 'itachi.jpg'

    def __init__(self, group: pg.sprite.AbstractGroup):
        self.image = self.load_image(Hero.img_filename)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.image.set_colorkey((255, 255, 255))
        super(Hero, self).__init__(group)
        self.live = 3
        self.size_hero = 50
        self.task_quantity = 0
        self.health_quantity = 0
        self.trap_quantity = 0
        self.teleport_quantity = 0
        self.motion = 0

    def move_hero(self, current_cell, indent):
        left, top = indent
        self.rect = self.image.get_rect(
            bottomright=(left + self.size_hero * (current_cell[0] + 1),
                         top + self.size_hero * (current_cell[1] + 1)))
        # self.screen.blit(self.hero, Hero.hero_rect)