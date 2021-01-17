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
        in_alpha = 0
        fon.set_alpha(in_alpha)
        pg.display.set_icon(Loader.load_image('icon.png'))
        screen.blit(fon, (0, 0))
        pg.display.flip()
        start_music = Loader.load_sound('start.wav')
        start_music.play(10000, fade_ms=3000)
        start_music.set_volume(0.1)

        running = True
        proceeded = False
        clock = pg.time.Clock()
        fps = 20
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    start_music.fadeout(1000)
                    proceeded = True
                    running = False
            if in_alpha < 100:
                in_alpha += 2
                fon.set_alpha(in_alpha)
                screen.blit(fon, (0, 0))
                pg.display.flip()
                clock.tick(fps)
        start_music.stop()
        pg.quit()
        return proceeded


class EndScreen:
    fontname = 'Special Elite.ttf'

    def __init__(self, screen: pg.Surface, hero: Hero, field, state: str, language: str):
        self.screen = screen
        self.hero = hero
        self.field_width, self.field_height = field.get_size()
        self.field_x, self.field_y = map(int, (field.x, field.y))
        self.state = state
        self.language = language
        self.font = Loader.load_font(EndScreen.fontname, 60)

        self.translate = {'en': {'victory': ('VICTORY', 0.06, 'main'),
                                 'loss': ('LOSS', 0.06, 'main'),
                                 'passed': ('You passed %d cells', 0.2, 'first'),
                                 'task': ('Task - %d', 0.3, 'first'),
                                 'health': ('Health - %d', 0.4, 'first'),
                                 'trap': ('Trap - %d', 0.5, 'first'),
                                 'teleport': ('Teleport - %d', 0.6, 'first'),
                                 'cell': ('Ordinary cell - %d', 0.7, 'first'),
                                 'inscription': (('To start again press', 'the space bar'),
                                                 (0.85, 0.9), 'second')},
                          'ru': {'victory': ('ПОБЕДА', 0.06, 'main'),
                                 'loss': ('ВЫ ПРОИГРАЛИ', 0.06, 'main'),
                                 'passed': ('Вы прошли %d клеток', 0.2, 'first'),
                                 'task': ('Задания - %d', 0.3, 'first'),
                                 'health': ('Здоровье - %d', 0.4, 'first'),
                                 'trap': ('Капканы - %d', 0.5, 'first'),
                                 'teleport': ('Телепорты - %d', 0.6, 'first'),
                                 'cell': ('Обычные лктеки - %d', 0.7, 'first'),
                                 'inscription': (('Чтобы начать заново', 'нажмите пробел'),
                                                 (0.85, 0.9), 'second')}}

        self.blur_surf(screen)
        self.update()

    @staticmethod
    def blur_surf(screen: pg.Surface) -> None:
        path = os.path.join('data', 'temp.png')
        pg.image.save(screen, path)
        pil_img = Image.open(path)
        pil_img = pil_img.filter(ImageFilter.GaussianBlur(radius=6))
        pil_img.save(path)
        screen.blit(pg.image.load(path), screen.get_rect())
        os.remove(os.path.join('data', 'temp.png'))

    def update(self):
        cells = self.hero.get_quantity()
        font_text = Loader.load_font(EndScreen.fontname, 40)
        font_text_2 = Loader.load_font(EndScreen.fontname, 30)
        fonts = {'main': self.font,
                 'first': font_text,
                 'second': font_text_2}
        keys = list(self.translate[self.language].keys())
        keys = keys[:1] + keys[2:] if self.state == 'victory' else keys[1:]
        for i in range(len(keys)):
            data = self.translate[self.language][keys[i]]
            font = fonts[data[-1]]
            raw_string = data[0]
            inscriptions = (raw_string,) if isinstance(raw_string, str) else raw_string
            for j, inscription in enumerate(inscriptions):
                if keys[i] in cells.keys():
                    inscription = inscription % cells[keys[i]]
                text = font.render(inscription, True, pg.Color('#141b47'))
                x = self.field_x + (self.field_width // 2 - text.get_width() // 2)
                h = data[1][j] if isinstance(data[0], tuple) else data[1]
                y = self.field_y + self.field_width * h
                self.screen.blit(text, (x, y))


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
