import os
from loader import Loader
import pygame as pg
from PIL import Image, ImageFilter


class StartScreen(Loader):
    def __init__(self):
        pg.init()
        size = 700, 436
        screen = pg.display.set_mode(size)
        pg.display.set_caption('Goof the Game')
        fon = Loader.load_image('fon.png')
        screen.blit(fon, (0, 0))
        pg.display.flip()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    pg.quit()
                    return


class EndScreen(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface, hero, group):
        # super(EndScreen, self).__init__(group)
        in_path = os.path.join('data', 'temp.png')
        out_path = os.path.join('data', 'temp2.png')
        pg.image.save(screen, in_path)
        pil_img = Image.open(in_path)
        pil_img = pil_img.filter(ImageFilter.GaussianBlur(radius=6))
        pil_img.save(out_path)
        screen.blit(pg.image.load(out_path), screen.get_rect())
        self.clear_temp_files()

    @staticmethod
    def clear_temp_files():
        env = os.listdir(os.path.join('data'))
        for filename in ('temp.png', 'temp2.png'):
            if filename in env:
                del_path = os.path.join('data', filename)
                os.remove(del_path)

    def update(self, *args, **kwargs):
        pass


class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)   # call Sprite initializer
        self.image = image_file
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location