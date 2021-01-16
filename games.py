from random import choice

import pygame as pg
from loader import Loader
from hero import StarFallHero, RunningInForestHero, Hero
from savers import StaticBackground, DynamicBackground, EndScreen
from tiles import Comet, Star, ParticlesForRunningInForest, FieldMagicMaze


class MiniGame:
    start_img = 'mini_game.jpg'
    fontname = 'Special Elite.ttf'

    def __init__(self, field, surface: pg.Surface, live):
        self.lives = live
        self.hero = None
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
                                 'victory': ('Победа', 'Вы получили 1 жизнь'),
                                 'loss': ('Поражение', 'Вы потеряли 1 жизнь'),
                                 'score': 'Счёт'}}
        self.language = self.field.get_language()
        self.running = False
        self.game_over = ''
        self.music = None
        self.font = None

    def start(self):
        self.music = Loader.load_sound('main.wav')
        self.music.play(1000, fade_ms=3000)
        self.music.set_volume(0.025)
        self.font = Loader.load_font(MiniGame.fontname, 60)
        self.running = True

    def end_loop(self) -> str:
        callback = None
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

    def end_game(self, font: pg.font.Font, state: str, color: str = '#ff4573') -> None:
        EndScreen.blur_surf(self.screen)
        self.game_over = state
        game_over_1 = font.render(self.translate[self.language][state][0],
                                  True, pg.Color(color))
        game_over_2 = font.render(self.translate[self.language][state][1],
                                  True, pg.Color(color))
        self.screen.blit(game_over_1, (self.screen.get_width() // 2 - game_over_1.get_width() * 0.5,
                                       self.screen.get_height() // 2.5))
        self.screen.blit(game_over_2, (self.screen.get_width() // 2 - game_over_2.get_width() * 0.5,
                                       self.screen.get_height() * 0.5))
        pg.display.flip()
        self.music.stop()

    def start_loop(self, title: str, width: int) -> str:
        sprites = pg.sprite.Group()
        bg = StaticBackground(MiniGame.start_img, [0, 0], size=(760, 760))
        sprites.add(bg)

        screen_width, screen_height = self.screen.get_size()
        title_font = Loader.load_font(MiniGame.fontname, width)
        title = title_font.render(title, True, pg.Color('#ebebeb'))
        title_pos = (screen_width // 2 - title.get_width() // 2,
                     screen_height // 2.25)
        inscription_font = Loader.load_font(MiniGame.fontname, int(width * 0.5))
        inscription = inscription_font.render('Press Space', True, pg.Color('#ebebeb'))
        inscription_pos = (screen_width // 2 - inscription.get_width() // 2,
                           title_pos[1] + title.get_height() // 2 + screen_height // 10)

        centering_indent = (inscription_pos[1] + inscription.get_height() - title_pos[1]) // 4
        title_pos = (title_pos[0], title_pos[1] - centering_indent)
        inscription_pos = (inscription_pos[0], inscription_pos[1] - centering_indent)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 'closeEvent'
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        return 'proceeded'
            sprites.update()
            sprites.draw(self.screen)
            self.screen.blit(title, title_pos)
            self.screen.blit(inscription, inscription_pos)
            pg.display.flip()


class MagicMaze(MiniGame):
    def __init__(self, field, surface: pg.Surface, lives: int):
        super(MagicMaze, self).__init__(field, surface, lives)
        self.hero = Hero()

    def loop(self, _):
        if self.start_loop('MagicMaze', 100) == 'closeEvent':
            return 'closeEvent'
        all_sprites = pg.sprite.Group()
        tiles_group = pg.sprite.Group()
        hero_group = pg.sprite.Group()
        hero_width, hero_height = 80, 80
        self.hero.resize(hero_width, hero_height)
        self.hero.rect = self.hero.image.get_rect(
            bottomright=(hero_width * 5,
                         hero_height * 5))
        hero_group.add(self.hero)
        maze = FieldMagicMaze(all_sprites, tiles_group, self.hero)
        groups = [tiles_group, hero_group]
        clock = pg.time.Clock()
        fps = 10
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 'closeEvent'
                if maze.move(event) == 'finish':
                    running = False
            for group in groups:
                group.update()
                group.draw(self.screen)
            pg.display.flip()
            clock.tick(fps)
            if not running:
                self.end_game(self.font, 'victory', '#ebebeb')
        return self.end_loop()


class RunningInForest(MiniGame):
    background_img = 'forest_long.png'
    background_img_reverse = 'forest_long_reverse.png'

    def __init__(self, field, surface: pg.Surface, lives: int):
        super(RunningInForest, self).__init__(field, surface, lives)
        self.hero = RunningInForestHero()

    def loop(self, screen_size: tuple):
        if self.start_loop('RunningInForest', 70) == 'closeEvent':
            return 'closeEvent'
        width, height = screen_size
        all_sprites = pg.sprite.Group()
        bg_1 = DynamicBackground(RunningInForest.background_img, [0, 0])
        bg_2 = DynamicBackground(RunningInForest.background_img_reverse, [bg_1.image.get_width(), 0])
        self.hero.resize(100, 100)
        self.hero.rect.x = int(width * 0.1)
        self.hero.rect.y = int(height * 0.8)
        all_sprites.add(bg_1, bg_2, self.hero)
        running = True
        fps = 80
        clock = pg.time.Clock()
        fires = pg.sprite.Group()
        tile_velocity = 10
        ParticlesForRunningInForest(tile_velocity, fires, screen_size)
        score = 0
        goal = choice([15000, 20000, 25000])
        score_text = self.font.render('%s - %d/%d' % (self.translate[self.language]['score'],
                                                      score, goal), True, pg.Color('#ebebeb'))
        self.screen.blit(score_text, (90, 200))
        state = False
        velocity_tick = 0
        spawn_tick = 0
        while running:
            if not state:
                velocity_tick += 1
                spawn_tick += 1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 'closeEvent'
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        state = not state
                        EndScreen.blur_surf(self.screen)
                        text = 'PAUSE' if self.field.get_language() == 'en' else 'ПАУЗА'
                        self.screen.blit(font.render(text, True, pg.Color('#ebebeb')),
                                         (self.screen.get_width() // 2 - font.size('PAUSE')[0] * 0.5,
                                          self.screen.get_height() // 2.5))
                        pg.display.update()
                    if not state:
                        self.hero.make_move(event)
            if state:
                continue
            if velocity_tick == fps * 10:
                velocity_tick = 0
                bg_1.velocity += 1
                bg_2.velocity += 1
                tile_velocity += 1
            if spawn_tick == fps * 2.5:
                spawn_tick = 0
                ParticlesForRunningInForest(tile_velocity, fires, screen_size)
            all_sprites.update()
            all_sprites.draw(self.screen)
            fires.update(self.hero)
            fires.draw(self.screen)
            for elem in fires:
                if elem.get_callback() == 'loss':
                    callback = 'loss'
                    self.end_game(self.font, callback)
                    running = False
                    break
            score += 6
            score_text = self.font.render('%s - %d /%d' % (self.translate[self.language]['score'],
                                                           score, goal), True, pg.Color('#ebebeb'))
            self.screen.blit(score_text, (10, 5))
            if score >= goal:
                callback = 'victory'
                self.end_game(self.font, callback)
                running = False
            pg.display.update()
            clock.tick(fps)
        callback = self.end_loop()
        return callback


class StarFall(MiniGame):
    background_img = 'forest.jpg'

    def __init__(self, field, surface: pg.Surface, lives: int):
        super(StarFall, self).__init__(field, surface, lives)
        self.hero = StarFallHero()

    def loop(self, screen_size: tuple):
        if self.start_loop('StarFall', 120) == 'closeEvent':
            return 'closeEvent'
        all_sprites = pg.sprite.Group()
        bg = StaticBackground(StarFall.background_img, [0, 0], size=(760, 760))
        self.hero.resize(110, 110)
        width, height = screen_size
        self.hero.rect.x = width // 2 - self.hero.image.get_width() // 2
        self.hero.rect.y = int(height * 0.8)
        self.hero.set_step(10)
        all_sprites.add(bg, self.hero)
        stars = pg.sprite.Group()
        for _ in range(3):
            Comet(stars, screen_size)
        for _ in range(1):
            Star(stars, screen_size)
        fps = 60
        clock = pg.time.Clock()
        tick = 0
        stars_caught = 0
        lives = font.render('%s - %d' % (self.translate[self.language]['lives'], self.lives),
                            True, pg.Color('#ebebeb'))
        goal = choice([10, 15, 20])
        stars_caught_text = self.font.render('%s - %d/%d' % (self.translate[self.language]['stars'],
                                                             stars_caught, goal),
                                             True, pg.Color('#ebebeb'))
        self.screen.blit(lives, (90, 200))
        self.screen.blit(stars_caught_text, (90, 200))
        state = False
        while self.running and not self.game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 'closeEvent'
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        state = not state
                        EndScreen.blur_surf(self.screen)
                        EndScreen.clear_temp_files()
                        text = 'PAUSE' if self.field.get_language() == 'en' else 'ПАУЗА'
                        self.screen.blit(self.font.render(text, True, pg.Color('#ebebeb')),
                                         (self.screen.get_width() // 2 - self.font.size('PAUSE')[0] * 0.5,
                                          self.screen.get_height() // 2.5))
                    if not state:
                        self.hero.make_move(event, width)
            if not state:
                all_sprites.update()
                all_sprites.draw(self.screen)
                stars.update(self.hero)
                stars.draw(self.screen)
                for elem in stars:
                    if elem.get_callback() == '-':
                        self.lives -= 1
                        elem.kill()
                        if self.lives == 0:
                            self.end_game(self.font, 'loss')
                            break
                    elif elem.get_callback() == '+':
                        stars_caught += 1
                        elem.kill()
                        if stars_caught == goal:
                            self.end_game(self.font, 'victory')
                            break
                if self.game_over:
                    continue
                lives = self.font.render('%s - %d' % (self.translate[self.language]['lives'], self.lives),
                                         True, pg.Color('#ebebeb'))
                stars_caught_text = self.font.render('%s - %d/%d' %
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
        callback = self.end_loop()
        return callback
