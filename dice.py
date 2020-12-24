import pygame as pg
from img_loader import ImageLoader


class Dice(pg.sprite.Sprite, ImageLoader):
    img_names = ['one-dice.png', 'two-dice.png', 'three-dice.png',
                 'four-dice.png', 'five-dice.png', 'six-dice.png']

    def __init__(self, screen_size, group):
        super(Dice, self).__init__(group)
        self.images = [self.load_image(img) for img in Dice.img_names]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = screen_size[0] // 2, screen_size[1] // 2