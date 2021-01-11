import pygame as pg
from random import choice
from loader import Loader
import time


class Dice(pg.sprite.Sprite, Loader):
    img_names = ['dice_1.png', 'dice_2.png', 'dice_3.png',
                 'dice_4.png', 'dice_5.png', 'dice_6.png']
    pg.mixer.init()
    # roll_sound = Loader.load_sound('dice-roll.wav')
    drop_sound = Loader.load_sound('dice-stop.wav')
    drop_sound.set_volume(0.20)

    def __init__(self, field_size, field_indent, group):
        super(Dice, self).__init__(group)
        self.images = [pg.transform.scale(self.load_image(img), (150, 150)) for img in Dice.img_names]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.img_width, self.img_height = self.image.get_size()
        self.field_size = field_size
        self.field_indent = field_indent
        self.visible, self.rotating = False, True
        self.start()

    def start(self):
        self.visible = False
        self.visibled()
        self.rotating = True

    def is_rotating(self) -> bool:
        return self.rotating

    def visibled(self, sound=True):
        self.visible = not self.visible

        if self.visible:
            self.rect.x = self.field_indent[0] + self.field_size[0] // 2 - self.img_width // 2
            self.rect.y = self.field_indent[1] + self.field_size[1] // 2 - self.img_height // 2
        else:
            if sound:
                Dice.drop_sound.play()
            time.sleep(0.5)
            self.rect.x = -1000
            self.rect.y = -1000

    def handle_rotating(self):
        self.rotating = not self.rotating
        return self.images.index(self.image) + 1 if not self.is_rotating() else None

    def rotate(self, tick: int) -> bool:
        if self.is_rotating() and tick == 5:
            prev_image = self.image
            while self.image == prev_image:
                self.image = choice(self.images)
            return True
        return False