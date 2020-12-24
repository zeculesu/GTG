import pygame as pg
from img_loader import ImageLoader


class Hero(pg.sprite.Sprite, ImageLoader):
    img_filename = 'itachi.jpg'

    def __init__(self, current_cell, indent, group: pg.sprite.AbstractGroup):
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
        self.moves = 1
        self.move_hero(current_cell, indent)

    def move_hero(self, current_cell, indent):
        if self.moves != 0:
            self.moves -= 1
            left, top = indent
            self.rect = self.image.get_rect(
                bottomright=(left + self.size_hero * (current_cell[0] + 1),
                             top + self.size_hero * (current_cell[1] + 1)))
            print('left: %d moves' % self.moves)

    def get_moves(self):
        return self.moves

    def add_moves(self, moves):
        self.moves += moves
        print('got %d moves!' % self.moves)