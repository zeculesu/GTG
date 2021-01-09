import os
from loader import Loader
import pygame as pg
from PIL import Image, ImageFilter

from hero import Hero


class StartScreen(Loader):
    @staticmethod
    def show() -> bool:
        pg.init()
        size = 700, 436
        screen = pg.display.set_mode(size)
        pg.display.set_caption('Goof the Game')
        fon = Loader.load_image('fon.png')
        pg.display.set_icon(Loader.load_image('icon.png'))
        screen.blit(fon, (0, 0))
        pg.display.flip()

        running = True
        proceeded = False
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    running = False
                    proceeded = True
        pg.quit()
        return proceeded


class EndScreen:
    def __init__(self, screen: pg.Surface, hero: Hero, state: str, language: str):
        self.hero = hero
        self.state = state
        self.language = language
        self.screen = screen
        self.blur_surf(screen)
        self.clear_temp_files()
        self.update()

    @staticmethod
    def blur_surf(screen: pg.Surface) -> None:
        in_path = os.path.join('data', 'temp.png')
        out_path = os.path.join('data', 'temp2.png')
        pg.image.save(screen, in_path)
        pil_img = Image.open(in_path)
        pil_img = pil_img.filter(ImageFilter.GaussianBlur(radius=6))
        pil_img.save(out_path)
        screen.blit(pg.image.load(out_path), screen.get_rect())

    @staticmethod
    def clear_temp_files() -> None:
        env = os.listdir(os.path.join('data'))
        for filename in ('temp.png', 'temp2.png'):
            if filename in env:
                del_path = os.path.join('data', filename)
                os.remove(del_path)

    def update(self):
        # 141b47
        font = Loader.load_font('Special Elite.ttf', 60)
        font_text = Loader.load_font('Special Elite.ttf', 40)
        font_text_2 = Loader.load_font('Special Elite.ttf', 30)
        if self.language == 'en':
            game_over = font.render(self.state.upper(), True, pg.Color('#141b47'))
            passed = font_text.render('You passed %d cells' % self.hero.get_passed_cells(), True, pg.Color('#141b47'))
            cells = self.hero.get_quantity()
            task = font_text.render('Task - %d' % cells['task'], True, pg.Color('#141b47'))
            health = font_text.render('Health - %d' % cells['health'], True, pg.Color('#141b47'))
            trap = font_text.render('Trap - %d' % cells['trap'], True, pg.Color('#141b47'))
            teleport = font_text.render('Teleport - %d' % cells['teleport'], True, pg.Color('#141b47'))
            cell = font_text.render('Ordinary Cell - %d' % cells['cell'], True, pg.Color('#141b47'))
            message_1 = font_text_2.render('To start again press', True, pg.Color('#141b47'))
            message_2 = font_text_2.render('the space bar', True, pg.Color('#141b47'))
            self.screen.blit(game_over, (self.screen.get_width() // 2 - game_over.get_width() // 2,
                                         125))
            # self.screen.blit(game_over, (230, 125))
            self.screen.blit(message_2, (275, 610))
        else:
            state_text = 'ПОБЕДА' if self.state == 'victory' else 'ВЫ ПРОИГРАЛИ'
            game_over = font.render(state_text, True, pg.Color('#141b47'))
            passed = font_text.render('Вы прошли %d клеток' % self.hero.get_passed_cells(), True, pg.Color('#141b47'))
            cells = self.hero.get_quantity()
            task = font_text.render('Задания - %d' % cells['task'], True, pg.Color('#141b47'))
            health = font_text.render('Здоровье - %d' % cells['health'], True, pg.Color('#141b47'))
            trap = font_text.render('Капканы - %d' % cells['trap'], True, pg.Color('#141b47'))
            teleport = font_text.render('Телепорты - %d' % cells['teleport'], True, pg.Color('#141b47'))
            cell = font_text.render('Обычные клетки - %d' % cells['cell'], True, pg.Color('#141b47'))
            message_1 = font_text_2.render('Чтобы начать заново', True, pg.Color('#141b47'))
            message_2 = font_text_2.render('нажмите пробел', True, pg.Color('#141b47'))
            self.screen.blit(game_over, (150, 115))
            self.screen.blit(message_2, (255, 610))
        self.screen.blit(passed, (90, 200))
        self.screen.blit(task, (90, 260))
        self.screen.blit(health, (90, 320))
        self.screen.blit(trap, (90, 380))
        self.screen.blit(teleport, (90, 440))
        self.screen.blit(cell, (90, 500))
        self.screen.blit(message_1, (225, 580))


class StaticBackground(pg.sprite.Sprite, Loader):
    def __init__(self, image_filename, position, size=None):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        img = self.load_image(image_filename)
        if size:
            img = pg.transform.smoothscale(img, size)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position


class DynamicBackground(StaticBackground):
    def __init__(self, image_filename, position, size=None):
        super(DynamicBackground, self).__init__(image_filename, position, size)
        self.velocity = 6

    def update(self):
        self.rect.x -= self.velocity
        if self.rect.x <= -self.image.get_width():
            self.rect.x = self.image.get_width()
