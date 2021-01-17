import pygame as pg

from loader import Loader
from field import Field
from hero import FieldHero
from dice import Dice
from savers import StartScreen, EndScreen, StaticBackground

SCREEN_SIZE = 1280, 720  # Константа разрешения экрана


# Функция конца игры
def finish(screen: pg.Surface, field: Field, hero: FieldHero,
           all_sprites: pg.sprite.AbstractGroup, bg: StaticBackground,
           state: str, sound: pg.mixer.Sound) -> None:
    sound.play()
    field.render(screen, hero.get_moves(), hero.get_lives(), bg)
    if not field.is_frozen():
        field.freeze()
    field.finished = True
    all_sprites.update()
    all_sprites.draw(screen)
    EndScreen(screen, hero, field, state, field.get_language())


# Основная функция
def main():
    proceeded = StartScreen.show()  # Нажал ли любую кнопку игрок?
    if not proceeded:
        return
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption('Goof the Game')
    # Спрайты, класс и группы спрайтов
    all_sprites = pg.sprite.Group()
    field = Field(screen)
    hero = FieldHero((0, 0), field.get_indent(), all_sprites)
    dice = Dice(field.get_size(), field.get_indent(), all_sprites)
    field.start(hero, dice)
    running = True
    clock = pg.time.Clock()
    bg = StaticBackground('end_screen.png', [0, 0], size=SCREEN_SIZE)
    screen.fill((50, 41, 88))
    pg.display.set_icon(Loader.load_image('icon.png'))
    # Курсор
    arrow = pg.sprite.Sprite(all_sprites)
    arrow.image = Loader.load_image('arrow.png')
    arrow.rect = arrow.image.get_rect()
    # Звуки
    click_sound = Loader.load_sound('COOL CLICK.wav')
    click_sound.set_volume(0.25)
    victory_sound = Loader.load_sound('victory.wav')
    victory_sound.set_volume(0.1)
    loss_sound = Loader.load_sound('loss.wav')
    loss_sound.set_volume(0.1)
    current_sound = None
    # Музыка
    music = Loader.load_sound('main.wav')
    music_volume = 0.025
    music.set_volume(music_volume)
    music.play(1000, fade_ms=1000)
    pg.mouse.set_visible(False)
    all_sprites.add(arrow)
    fps = 60
    dice_tick = 0
    while running:
        if field.task_is_active():  # Переход в игровой цикл мини-игры
            music.set_volume(0)
            callback = field.current_game.loop(SCREEN_SIZE)
            if callback == 'closeEvent':
                running = False
            elif callback == 'victory':
                music.set_volume(music_volume)
                hero.lives -= 1
                field.disable_task()
            elif callback == 'loss':
                hero.lives += 1
                field.disable_task()
                if hero.get_lives() == 0:
                    music.set_volume(0)
                    dice.hide(sound=False)
                    current_sound = loss_sound
                    finish(screen, field, hero, all_sprites, bg, callback, current_sound)
        else:  # Цикл на поле
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    click_sound.play()
                    x, y = event.pos
                    if x <= 40 and y <= 40:  # Получение нажатия на кнопку перевода
                        field.change_language()
                if event.type == pg.MOUSEMOTION:
                    arrow.rect.x, arrow.rect.y = pg.mouse.get_pos()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if hero.get_moves() == 0 and not field.is_finished():
                            field.freeze()
                            moves = dice.handle_rotating()
                            hero.moves += moves
                        elif field.is_finished():
                            current_sound.fadeout(500)
                            music.set_volume(music_volume)
                            field.start(hero, dice)
                    else:
                        callback = field.handle_move(event, hero, dice)
                        if callback == 'victory':
                            music.set_volume(0)
                            current_sound = victory_sound
                            finish(screen, field, hero, all_sprites, bg, callback, victory_sound)
                        elif callback == 'loss':
                            music.set_volume(0)
                            current_sound = loss_sound
                            finish(screen, field, hero, all_sprites, bg, callback, loss_sound)
            if dice.is_rotating():
                dice_tick += 1
                rotation = dice.rotate(dice_tick)
                if rotation:
                    dice_tick = 0
            if not field.is_finished():
                field.render(screen, hero.get_moves(), hero.get_lives(), bg)
                all_sprites.update()
                all_sprites.draw(screen)
            pg.display.flip()
            clock.tick(fps)
    pg.quit()


if __name__ == '__main__':
    main()