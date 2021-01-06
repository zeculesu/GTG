import pygame as pg
from random import randint

from hero import Hero
from savers import Background
# from main import SCREEN_SIZE
# from field import Field


class MiniGame:
    def __init__(self, hero: Hero, field, surface: pg.Surface):
        self.hero = hero
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
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    callback = 'closeEvent'
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    # if event.key == pg.K_ESCAPE:
                    #     callback = 'gameOver'
                    #     self.running = False
                    self.hero.handle_game_move(event, width)
                all_sprites.update()
                all_sprites.draw(self.screen)
                pg.display.flip()
        return callback