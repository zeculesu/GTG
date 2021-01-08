from random import randint, choice

import pygame as pg
from loader import Loader
from hero import TaskHero
from savers import Background, EndScreen
from tiles import Comet, Star


class MiniGame:
    def __init__(self, field, surface: pg.Surface, live):
        self.lives = live
        self.hero = TaskHero()
        self.field = field
        self.screen = surface
        self.translate = {'en': {'stars': 'Stars',
                                 'lives': 'Lives',
                                 'pause': 'Pause',
                                 'victory': ('Victory', 'You have received 1 life'),
                                 'loss': ('Loss', 'You have lost 1 life'),
                                 'score': 'Score'},
                          'ru': {'stars': 'Звёзды',
                                 'lives': 'Жизни',
                                 'pause': 'Пауза',
                                 'victory': ('Победа', 'Мы даруем Вам 1 жизнь'),
                                 'loss': ('Поражение', 'Мы забираем 1 Вашу бренную жизнь'),
                                 'счёт': 'Счёт'}}
        self.language = self.field.get_language()
        self.running = False
        self.game_over = ''

    def start(self):
        self.running = True


class RunningInForest(MiniGame):
    background_img = 'forest_long.png'
    background_img_reverse = 'forest_long_reverse.png'

    def loop(self, screen_size: tuple):
        callback = None
        width, height = screen_size
        all_sprites = pg.sprite.Group()
        bg_1 = Background(RunningInForest.background_img, [0, 0])
        bg_2 = Background(RunningInForest.background_img_reverse, [bg_1.image.get_width(), 0])
        self.hero.resize(100, 100)
        self.hero.rect.x = width * 0.1
        self.hero.rect.y = int(height * 0.8)
        all_sprites.add(bg_1, bg_2, self.hero)
        running = True
        fps = 80
        clock = pg.time.Clock()
        shrubs = pg.sprite.Group()
        groups = [all_sprites, shrubs]
        font = Loader.load_font('Special Elite.ttf', 60)
        score = 0
        goal = choice([15000, 20000, 25000])
        score_text = font.render('%s - %d/%d' % (self.translate[self.language]['score'],
                                                 score, goal), True, '#ebebeb')
        self.screen.blit(score_text, (90, 200))
        # for _ in range(3):
        #     Comet(stars, screen_size)
        state = False
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    callback = 'closeEvent'
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        state = not state
                        EndScreen.blur_surf(self.screen)
                        EndScreen.clear_temp_files()
                        text = 'PAUSE' if self.field.get_language() == 'en' else 'ПАУЗА'
                        self.screen.blit(font.render(text, True, pg.Color('#ebebeb')),
                                         (self.screen.get_width() // 2 - font.size('PAUSE')[0] * 0.5,
                                          self.screen.get_height() // 2.5))
            if state:
                continue
            for group in groups:
                group.update()
                group.draw(self.screen)
            score += 6
            score_text = font.render('%s - %d /%d' % (self.translate[self.language]['score'],
                                                     score, goal), True, '#ebebeb')
            self.screen.blit(score_text, (10, 5))
            if score == goal:
                callback = 'victory'
                running = False
            pg.display.update()
            clock.tick(fps)
        return callback


class StarFall(MiniGame):
    background_img = 'forest.jpg'

    def end_game(self, font, state: str) -> None:
        EndScreen.blur_surf(self.screen)
        EndScreen.clear_temp_files()
        self.game_over = state
        game_over_1 = font.render(self.translate[self.language][state][0],
                                  True, pg.Color('#ebebeb'))
        game_over_2 = font.render(self.translate[self.language][state][1],
                                  True, pg.Color('#ebebeb'))
        self.screen.blit(game_over_1, (self.screen.get_width() // 2 - game_over_1.get_width() * 0.5,
                                       self.screen.get_height() // 2.5))
        self.screen.blit(game_over_2, (self.screen.get_width() // 2 - game_over_2.get_width() * 0.5,
                                       self.screen.get_height() * 0.5))
        pg.display.flip()

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
        lives = font.render('%s - %d' % (self.translate[self.language]['lives'], self.lives),
                            True, pg.Color('#ebebeb'))
        goal = choice([10, 15, 20])
        stars_caught_text = font.render('%s - %d/%d' % (self.translate[self.language]['stars'],
                                                        stars_caught, goal),
                                        True, pg.Color('#ebebeb'))
        self.screen.blit(lives, (90, 200))
        self.screen.blit(stars_caught_text, (90, 200))
        state = False
        while self.running and not self.game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    callback = 'closeEvent'
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        state = not state
                        EndScreen.blur_surf(self.screen)
                        EndScreen.clear_temp_files()
                        text = 'PAUSE' if self.field.get_language() == 'en' else 'ПАУЗА'
                        self.screen.blit(font.render(text, True, pg.Color('#ebebeb')),
                                         (self.screen.get_width() // 2 - font.size('PAUSE')[0] * 0.5,
                                          self.screen.get_height() // 2.5))
                    if not state:
                        self.hero.make_move(event, width)
            if not state:
                for group in groups:
                    group.update(self.hero)
                    group.draw(self.screen)
                for elem in stars:
                    if elem.get_callback() == '-':
                        self.lives -= 1
                        elem.kill()
                        if self.lives == 0:
                            self.end_game(font, 'loss')
                            break
                    elif elem.get_callback() == '+':
                        stars_caught += 1
                        elem.kill()
                        if stars_caught == goal:
                            self.end_game(font, 'victory')
                            break
                if self.game_over:
                    continue
                lives = font.render('%s - %d' % (self.translate[self.language]['lives'], self.lives),
                                    True, pg.Color('#ebebeb'))
                stars_caught_text = font.render('%s - %d/%d' %
                                                (self.translate[self.language]['stars'],
                                                 stars_caught, goal),
                                                True, pg.Color('#ebebeb'))
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
        while self.running and self.game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    callback = 'closeEvent'
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        callback = self.game_over
                        self.running = False
        return callback
