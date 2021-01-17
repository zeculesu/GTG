from random import choice
import pygame as pg

from loader import Loader
from hero import StarFallHero, RunningInForestHero, Hero
from savers import StaticBackground, DynamicBackground, EndScreen
from tiles import Comet, Star, ParticlesForRunningInForest, FieldMagicMaze


class MiniGame:  # Родительский класс всех мини-игр
    start_img = 'mini_game.jpg'  # Изображение заставки
    fontname = 'Special Elite.ttf'  # Основной шрифт

    def __init__(self, field, surface: pg.Surface, lives: int, sound_of_on):
        self.lives = lives  # Жизни героя
        self.hero = None
        self.field = field  # Экземпляр поля
        self.screen = surface  # Экран
        self.screen_width, self.screen_height = surface.get_size()  # Размеры экрана

        # Перевод всех возможных надписей
        self.translate = {'en': {'stars': 'Stars',
                                 'lives': 'Lives',
                                 'pause': 'Pause',
                                 'victory': ('Victory', 'You have received 1 life'),
                                 'loss': ('Loss', 'You have lost 1 life'),
                                 'score': 'Score',
                                 'games': {
                                     'StarFall': 'Starfall',
                                     'RunningInForest': 'Running in Forest',
                                     'MagicMaze': 'Magic Maze'
                                 },
                                 'inscription': 'Press Space'},
                          'ru': {'stars': 'Звёзды',
                                 'lives': 'Жизни',
                                 'pause': 'Пауза',
                                 'victory': ('Победа', 'Вы получили 1 жизнь'),
                                 'loss': ('Поражение', 'Вы потеряли 1 жизнь'),
                                 'score': 'Счёт',
                                 'games': {
                                     'StarFall': 'Звездопад',
                                     'RunningInForest': 'Бегущий в лесу',
                                     'MagicMaze': 'Лабиринт'
                                 },
                                 'inscription': 'Нажмите пробел'}}
        # Значения громкости для разных звуковых файлов
        self.music_data = {'minigame_1.wav': {'volume': 0.1},
                           'minigame_2.wav': {'volume': 0.05}}

        self.language = self.field.get_language()  # Текущий язык
        self.running = False  # Булево значение завершённости игры
        self.game_over = ''  # Значение победы или поражения в виде строки
        # Далее служебные переменные
        self.music = None
        self.victory_sound, self.loss_sound = None, None
        self.font = None
        self.sound_of_on = sound_of_on

    def start(self):  # Функция начала игры
        # Определение фоновой музыки
        filename = choice(['minigame_1.wav', 'minigame_2.wav'])
        self.music = Loader.load_sound(filename)
        self.music.play(1000)
        self.music.set_volume(self.music_data[filename]['volume'])
        # Звуки победы и поражения
        self.victory_sound = Loader.load_sound('victory.wav')
        self.victory_sound.set_volume(0.1)
        self.loss_sound = Loader.load_sound('loss.wav')
        self.loss_sound.set_volume(0.1)
        self.font = Loader.load_font(MiniGame.fontname, 60)  # Общеиспользуемый шрифт
        self.running = True  # Статус начала игры

    def end_loop(self, sound: pg.mixer.Sound) -> str:  # Цикл выхода из игры по нажатию пробела
        callback = None
        while self.running and self.game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    callback = 'closeEvent'
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        sound.stop()
                        callback = self.game_over
                        self.running = False
        return callback

    # Окончание игры и конечная заставка
    def end_game(self, font: pg.font.Font, state: str, color: str = '#ff4573') -> pg.mixer.Sound:
        sound = self.victory_sound if state == 'victory' else self.loss_sound
        if self.sound_of_on:
            sound.play()
        EndScreen.blur_surf(self.screen)
        self.game_over = state
        game_over_1 = font.render(self.translate[self.language][state][0],
                                  True, pg.Color(color))
        game_over_2 = font.render(self.translate[self.language][state][1],
                                  True, pg.Color(color))
        self.screen.blit(game_over_1, (self.screen_width // 2 - game_over_1.get_width() * 0.5,
                                       self.screen_height // 2.5))
        self.screen.blit(game_over_2, (self.screen_width // 2 - game_over_2.get_width() * 0.5,
                                       self.screen_height * 0.5))
        pg.display.flip()
        self.music.stop()
        return sound

    # Цикл начальной заставки по нажатию пробела
    def start_loop(self, game_name: str, width: int) -> str:
        sprites = pg.sprite.Group()
        bg = StaticBackground(MiniGame.start_img, [0, 0],
                              size=(self.screen_width, self.screen_height))
        sprites.add(bg)

        title_font = Loader.load_font(MiniGame.fontname, width)
        title = title_font.render(self.translate[self.language]['games'][game_name],
                                  True, pg.Color('#ebebeb'))
        title_pos = (self.screen_width // 2 - title.get_width() // 2,
                     self.screen_height // 2.25)
        inscription_font = Loader.load_font(MiniGame.fontname, int(width * 0.5))
        inscription = inscription_font.render(self.translate[self.language]['inscription'],
                                              True, pg.Color('#ebebeb'))
        inscription_pos = (self.screen_width // 2 - inscription.get_width() // 2,
                           title_pos[1] + title.get_height() // 2 + self.screen_height // 10)

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

    def sound_render(self):
        if self.sound_of_on:
            pg.mixer.unpause()
            image_sound = Loader.load_image('volume.png')
        else:
            pg.mixer.pause()
            image_sound = Loader.load_image('mute.png')
        self.screen.blit(image_sound, image_sound.get_rect(
            bottomright=(self.screen.get_size()[0], image_sound.get_size()[1])))


class MagicMaze(MiniGame):  # Класс мини-игры "Лабиринт"
    def __init__(self, field, surface: pg.Surface, lives: int, sound_of_on):
        super(MagicMaze, self).__init__(field, surface, lives, sound_of_on)
        self.hero = Hero()  # Инициализация нового героя

    def loop(self, _):  # Игровой цикл
        if self.start_loop('MagicMaze', 100) == 'closeEvent':  # Если на заставке игру закрыли
            return 'closeEvent', self.sound_of_on
        # Инициализация групп спрайтов
        all_sprites = pg.sprite.Group()
        tiles_group = pg.sprite.Group()
        hero_group = pg.sprite.Group()
        # Корректировка размеров героя
        hero_width, hero_height = 80, 80
        self.hero.resize(hero_width, hero_height)
        hero_group.add(self.hero)
        maze = FieldMagicMaze(all_sprites, tiles_group, self.hero)  # Инициализация поля лабиринта
        self.hero.rect = self.hero.image.get_rect(  # Перемещение героя в точку начала
            bottomright=(hero_width * (maze.current_cell[0] + 1),
                         hero_height * (maze.current_cell[1] + 1)))
        sound = None
        clock = pg.time.Clock()
        fps = 20
        running = True
        arrow = pg.sprite.Sprite(all_sprites)
        arrow.image = Loader.load_image('arrow.png')
        arrow.rect = arrow.image.get_rect()
        arrow_group = pg.sprite.GroupSingle(arrow)
        groups = [tiles_group, hero_group, arrow_group]
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 'closeEvent', self.sound_of_on
                if maze.move(event) == 'finish':
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x >= self.screen.get_width() - 36 and y <= 40:
                        self.sound_of_on = not self.sound_of_on
                if event.type == pg.MOUSEMOTION:
                    arrow.rect.x, arrow.rect.y = pg.mouse.get_pos()
            for group in groups:
                group.update()
                group.draw(self.screen)
            self.sound_render()
            pg.display.flip()
            clock.tick(fps)
            if not running:
                sound = self.end_game(self.font, 'victory', '#ebebeb')
        return self.end_loop(sound), self.sound_of_on  # Возвращает callback из конечного цикла


class RunningInForest(MiniGame):  # Класс мини-игры "Бегущий по лесу"
    background_img = 'forest_long.png'  # Картинка заднего фона
    background_img_reverse = 'forest_long_reverse.png'  # Отзеркаленная картинка заднего фона

    def __init__(self, field, surface: pg.Surface, lives: int, sound_of_on):
        super(RunningInForest, self).__init__(field, surface, lives, sound_of_on)
        self.hero = RunningInForestHero()  # Инициализация героя для этой мини-игры

    def loop(self, screen_size: tuple):  # Игровой цикл
        if self.start_loop('RunningInForest', 70) == 'closeEvent':
            return 'closeEvent', self.sound_of_on
        width, height = screen_size  # Размеры экрана
        all_sprites = pg.sprite.Group()  # Иницилиализация группы спрайтов
        # Инициализация двух динамических задних фонов
        bg_1 = DynamicBackground(RunningInForest.background_img,
                                 [0, 0], size=screen_size)
        bg_2 = DynamicBackground(RunningInForest.background_img_reverse,
                                 [bg_1.image.get_width(), 0], size=screen_size)
        # Корректировка размеров и позиционирование героя
        self.hero.adjust((100, 100), int(width * 0.1), int(height * 0.8))
        hero_bottom = self.hero.rect.bottom
        all_sprites.add(bg_1, bg_2, self.hero)
        fires = pg.sprite.Group()  # Группа препятствий
        tile_velocity = 10  # Скорость приближения препятствий к герою
        ParticlesForRunningInForest(tile_velocity, fires,
                                    screen_size, hero_bottom)  # Инициализация 1-го спрайта
        score = 0  # Текущий счёт
        goal = choice([15000, 20000, 25000])  # Возможные цели счёта
        state = False  # Переменная паузы
        sound = None  # Переменная звука
        velocity_tick = 0  # Счётчик увеличения скорости
        spawn_tick = 0  # Счётчик спавна препятствий
        fps = 80
        clock = pg.time.Clock()
        arrow = pg.sprite.Sprite(all_sprites)
        arrow.image = Loader.load_image('arrow.png')
        arrow.rect = arrow.image.get_rect()
        arrow_group = pg.sprite.GroupSingle(arrow)
        running = True
        while running:
            if not state:
                velocity_tick += 1
                spawn_tick += 1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 'closeEvent', self.sound_of_on
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        state = not state
                        EndScreen.blur_surf(self.screen)
                        text = 'PAUSE' if self.field.get_language() == 'en' else 'ПАУЗА'
                        self.screen.blit(self.font.render(text, True, pg.Color('#ebebeb')),
                                         (self.screen_width // 2 - self.font.size('PAUSE')[0] * 0.5,
                                          self.screen_height // 2.5))
                        pg.display.update()
                    if not state:
                        self.hero.make_move(event)
                elif event.type == pg.MOUSEMOTION:
                    arrow.rect.x, arrow.rect.y = pg.mouse.get_pos()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x >= self.screen.get_width() - 36 and y <= 40:
                        self.sound_of_on = not self.sound_of_on
            if state:
                continue
            if velocity_tick == fps * 10:
                velocity_tick = 0
                bg_1.velocity += 1
                bg_2.velocity += 1
                tile_velocity += 1
            if spawn_tick == fps * 2.5:
                spawn_tick = 0
                ParticlesForRunningInForest(tile_velocity, fires, screen_size, hero_bottom)
            all_sprites.update()
            all_sprites.draw(self.screen)
            fires.update(self.hero)
            fires.draw(self.screen)
            arrow_group.update()
            arrow_group.draw(self.screen)
            self.sound_render()
            for elem in fires:
                if elem.get_callback() == 'loss':  # Проверка на столкновение героя с препятствием
                    callback = 'loss'
                    sound = self.loss_sound
                    self.end_game(self.font, callback)
                    running = False
                    break
            score += 6
            score_text = self.font.render('%s - %d /%d' % (self.translate[self.language]['score'],
                                                           score, goal), True, pg.Color('#ebebeb'))
            self.screen.blit(score_text, (int(self.screen_width * 0.01),
                                          int(self.screen_height * 0.005)))
            if score >= goal:
                callback = 'victory'
                sound = self.end_game(self.font, callback)
                running = False
            pg.display.update()
            clock.tick(fps)
        return self.end_loop(sound), self.sound_of_on


class StarFall(MiniGame):  # Класс мини-игры "Звездопад"
    background_img = 'forest.jpg'  # Изображение заднего фона

    def __init__(self, field, surface: pg.Surface, lives: int, sound_of_on):
        super(StarFall, self).__init__(field, surface, lives, sound_of_on)
        self.hero = StarFallHero()  # Инициализация героя Звездопада

    def loop(self, screen_size: tuple):  # Игровой цикл
        if self.start_loop('StarFall', 120) == 'closeEvent':  # -/- с другими классами мини-игр
            return 'closeEvent', self.sound_of_on
        # Далее сходная расстановка переменных с другими мини-играми
        all_sprites = pg.sprite.Group()
        bg = StaticBackground(StarFall.background_img, [0, 0], size=screen_size)
        self.hero.resize(110, 110)
        width, height = screen_size
        self.hero.rect.x = width // 2 - self.hero.image.get_width() // 2
        self.hero.rect.y = int(height * 0.8)
        self.hero.set_step(10)
        all_sprites.add(bg, self.hero)
        stars = pg.sprite.Group()
        for _ in range(3):  # Первый спавн комет
            Comet(stars, screen_size)
        for _ in range(1):  # Первый спавн звёздочки
            Star(stars, screen_size)
        fps = 60
        clock = pg.time.Clock()
        tick = 0
        stars_caught = 0
        goal = choice([10, 15, 20])
        state = False
        sound = None
        arrow = pg.sprite.Sprite(all_sprites)
        arrow.image = Loader.load_image('arrow.png')
        arrow.rect = arrow.image.get_rect()
        arrow_group = pg.sprite.GroupSingle(arrow)
        while self.running and not self.game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 'closeEvent', self.sound_of_on
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        state = not state
                        EndScreen.blur_surf(self.screen)
                        text = 'PAUSE' if self.field.get_language() == 'en' else 'ПАУЗА'
                        self.screen.blit(self.font.render(text, True, pg.Color('#ebebeb')),
                                         (self.screen.get_width() // 2 - self.font.size('PAUSE')[0] * 0.5,
                                          self.screen.get_height() // 2.5))
                    if not state:
                        self.hero.make_move(event, width)
                elif event.type == pg.MOUSEMOTION:
                    arrow.rect.x, arrow.rect.y = pg.mouse.get_pos()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x >= self.screen.get_width() - 36 and y <= 40:
                        self.sound_of_on = not self.sound_of_on
            if not state:
                all_sprites.update()
                all_sprites.draw(self.screen)
                stars.update(self.hero)
                stars.draw(self.screen)
                arrow_group.update()
                arrow_group.draw(self.screen)
                for elem in stars:
                    if elem.get_callback() == '-':
                        self.lives -= 1
                        elem.kill()
                        if self.lives == 0:
                            sound = self.loss_sound
                            self.end_game(self.font, 'loss')
                            break
                    elif elem.get_callback() == '+':
                        stars_caught += 1
                        elem.kill()
                        if stars_caught == goal:
                            sound = self.victory_sound
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
                self.screen.blit(lives, (int(self.screen_width) * 0.01,
                                         int(self.screen_height * 0.0075)))
                self.screen.blit(stars_caught_text, (int(self.screen_width * 0.01),
                                                     int(self.screen_height * 0.075)))
                tick += 1
                if tick == 150:
                    tick = 0
                    for _ in range(3):
                        Comet(stars, screen_size)
                    for _ in range(1):
                        Star(stars, screen_size)
            self.sound_render()
            clock.tick(fps)
            pg.event.pump()
            pg.display.flip()
        return self.end_loop(sound), self.sound_of_on  # Возвращение callback из конечного цикла
