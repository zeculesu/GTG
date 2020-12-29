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
        self.hero = hero
        in_path = os.path.join('data', 'temp.png')
        out_path = os.path.join('data', 'temp2.png')
        pg.image.save(screen, in_path)
        pil_img = Image.open(in_path)
        pil_img = pil_img.filter(ImageFilter.GaussianBlur(radius=6))
        pil_img.save(out_path)
        screen.blit(pg.image.load(out_path), screen.get_rect())
        self.screen = screen
        self.clear_temp_files()
        self.update()

    @staticmethod
    def clear_temp_files():
        env = os.listdir(os.path.join('data'))
        for filename in ('temp.png', 'temp2.png'):
            if filename in env:
                del_path = os.path.join('data', filename)
                os.remove(del_path)

    def update(self): # *args, **kwargs
        font = Loader.load_font('Special Elite.ttf', 50)
        game_over = font.render('GAME OVER', True, pg.Color('#000000'))
        passed = font.render('You passed %d cells' % self.hero.get_passed_cells(), True, pg.Color('#000000'))
        cells = self.hero.get_quantity()
        task = font.render('Task - %d' % cells['task'], True, pg.Color('#000000'))
        health = font.render('Health - %d' % cells['health'], True, pg.Color('#000000'))
        trap = font.render('Trap - %d' % cells['trap'], True, pg.Color('#000000'))
        teleport = font.render('Teleport - %d' % cells['teleport'], True, pg.Color('#000000'))
        cell = font.render('Ordinary Cell - %d' % cells['cell'], True, pg.Color('#000000'))
        message_1 = font.render('To start again press', True, pg.Color('#000000'))
        message_2 = font.render('the space bar', True, pg.Color('#000000'))
        self.screen.blit(game_over, (260, 60))
        self.screen.blit(passed, (80, 140))
        self.screen.blit(task, (80, 210))
        self.screen.blit(health, (80, 280))
        self.screen.blit(trap, (80, 350))
        self.screen.blit(teleport, (80, 420))
        self.screen.blit(cell, (80, 490))
        self.screen.blit(message_1, (125, 580))
        self.screen.blit(message_2, (205, 650))


class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)   # call Sprite initializer
        self.image = image_file
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location