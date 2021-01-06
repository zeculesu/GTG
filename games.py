import pygame as pg
from random import randint

from hero import TaskHero
from savers import Background
from tiles import Comet
# from main import SCREEN_SIZE
# from field import Field


class MiniGame:
    def __init__(self, field, surface: pg.Surface):
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
        for _ in range(15):
            Comet(stars, screen_size)
        fps = 60
        clock = pg.time.Clock()
        tick = 0
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    callback = 'closeEvent'
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        callback = 'gameOver'
                        self.running = False
                    self.hero.make_move(event, width)
            for group in groups:
                group.update()
                group.draw(self.screen)
            tick += 1
            if tick == 200:
                tick = 0
                for _ in range(10):
                    Comet(stars, screen_size)
            clock.tick(fps)
            pg.display.flip()
        return callback