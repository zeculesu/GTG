import pygame as pg
import os
from PIL import Image, ImageFilter
from random import randint
from loader import Loader
from hero import TaskHero
from savers import Background
from tiles import Comet, Star


# from main import SCREEN_SIZE
# from field import Field


class MiniGame:
    def __init__(self, field, surface: pg.Surface, live):
        self.lives = live
        self.hero = TaskHero()
        self.field = field
        self.screen = surface
        self.running = False

    def start(self):
        self.running = True


class StarFall(MiniGame):
    background_img = 'forest.jpg'

    def handle_move(self):
        pass

    def loop(self, screen_size: tuple):
        callback = None
        all_sprites = pg.sprite.Group()
        bg = Background(StarFall.background_img, [0, 0], size=(760, 760))
        self.hero.resize(110, 110)
        width, height = screen_size
        self.hero.rect.x = width // 2 - self.hero.image.get_width() // 2
        self.hero.rect.y = int(height * 0.8)
        self.hero.set_step(10)
        all_sprites.add(bg, self.hero)
        stars = pg.sprite.Group()
        groups = [all_sprites, stars]
        for _ in range(3):
            Comet(stars, screen_size)
        for _ in range(1):
            Star(stars, screen_size)
        fps = 60
        clock = pg.time.Clock()
        tick = 0
        stars_caught = 0
        font = Loader.load_font('Special Elite.ttf', 60)
        lives = font.render('Lives - %d' % self.lives, True, pg.Color('#ebebeb'))
        stars_caught_text = font.render('Stars - %d' % stars_caught, True, pg.Color('#ebebeb'))
        self.screen.blit(lives, (90, 200))
        self.screen.blit(stars_caught_text, (90, 200))
        state = False
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    callback = 'closeEvent'
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        state = not state
                        in_path = os.path.join('data', 'temp.png')
                        out_path = os.path.join('data', 'temp2.png')
                        pg.image.save(self.screen, in_path)
                        pil_img = Image.open(in_path)
                        pil_img = pil_img.filter(ImageFilter.GaussianBlur(radius=6))
                        pil_img.save(out_path)
                        self.screen.blit(pg.image.load(out_path), self.screen.get_rect())
                        self.screen.blit(font.render('PAUSE', True, pg.Color('#ebebeb')),
                                         (self.screen.get_width() // 2 - font.size('PAUSE')[0] * 0.5,
                                          self.screen.get_height() // 2.5))
                    if not state:
                        if event.key == pg.K_ESCAPE:
                            callback = 'gameOver'
                            self.running = False
                        else:
                            self.hero.make_move(event, width)
            if not state:
                for group in groups:
                    group.update(self.hero)
                    group.draw(self.screen)
                for elem in stars:
                    if elem.get_callback() == '-':
                        self.lives -= 1
                        elem.kill()
                    elif elem.get_callback() == '+':
                        stars_caught += 1
                        elem.kill()
                lives = font.render('Lives - %d' % self.lives, True, pg.Color('#ebebeb'))
                stars_caught_text = font.render('Stars - %d' % stars_caught, True, pg.Color('#ebebeb'))
                self.screen.blit(lives, (10, 5))
                self.screen.blit(stars_caught_text, (10, 55))
                tick += 1
                if tick == 150:
                    tick = 0
                    for _ in range(3):
                        Comet(stars, screen_size)
                    for _ in range(1):
                        Star(stars, screen_size)
            clock.tick(fps)
            pg.event.pump()
            pg.display.flip()
        return callback
