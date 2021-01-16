import pygame as pg
from random import choice
from loader import Loader


class Dice(pg.sprite.Sprite, Loader):
    img_names = ['dice_1.png', 'dice_2.png', 'dice_3.png',
                 'dice_4.png', 'dice_5.png', 'dice_6.png']
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
        self.show()

    def is_rotating(self) -> bool:
        return self.rotating

    def show(self):
        self.visible = True
        self.rotating = True
        self.rect.x = self.field_indent[0] + self.field_size[0] // 2 - self.img_width // 2
        self.rect.y = self.field_indent[1] + self.field_size[1] // 2 - self.img_height // 2

    def hide(self):
        self.visible = False
        self.rotating = False
        Dice.drop_sound.play()
        pg.time.wait(500)
        self.rect.x = -1000
        self.rect.y = -1000

    def handle_rotating(self):
        self.hide()
        return self.images.index(self.image) + 1

    def rotate(self, tick: int) -> bool:
        if self.rotating and tick == 5:
            idx = self.images.index(self.image)
            self.image = choice(self.images[:idx] + self.images[idx + 1:])
            return True
        return False