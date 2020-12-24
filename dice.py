import pygame as pg
from random import choice
from img_loader import ImageLoader


class Dice(pg.sprite.Sprite, ImageLoader):
    img_names = ['dice_1.png', 'dice_2.png', 'dice_3.png',
                 'dice_4.png', 'dice_5.png', 'dice_6.png']

    def __init__(self, field_size, field_indent, group):
        super(Dice, self).__init__(group)
        self.images = [pg.transform.scale(self.load_image(img), (150, 150)) for img in Dice.img_names]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        img_width, img_height = self.image.get_size()
        self.rect.x = field_indent[0] + field_size[0] // 2 - img_width // 2
        self.rect.y = field_indent[1] + field_size[1] // 2 - img_height // 2
        self.rotating = True

    def is_rotating(self) -> bool:
        return self.rotating

    def handle_rotating(self):
        self.rotating = not self.rotating
        return self.images.index(self.image) + 1 if not self.is_rotating() else None

    def rotate(self):
        if self.is_rotating():
            prev_image = self.image
            while self.image == prev_image:
                self.image = choice(self.images)