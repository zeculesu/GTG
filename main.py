import pygame as pg
from loader import Loader
from field import Field
from hero import FieldHero
from dice import Dice
from savers import StartScreen, EndScreen, StaticBackground

SCREEN_SIZE = 760, 760


def finish(screen: pg.Surface, field: Field, hero: FieldHero,
           all_sprites: pg.sprite.AbstractGroup, bg: StaticBackground,
           state: str) -> None:
    field.render(screen, hero.get_moves(), hero.get_live(), bg)
    if not field.is_frozen():
        field.froze()
    field.finished = True
    all_sprites.update()
    all_sprites.draw(screen)
    EndScreen(screen, hero, state, field.get_language())


def main():
    proceeded = StartScreen.show()
    if not proceeded:
        return
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption('Goof the Game')
    all_sprites = pg.sprite.Group()
    field = Field(screen, all_sprites)
    hero = FieldHero((0, 0), field.get_indent(), all_sprites)
    dice = Dice(field.get_size(), field.get_indent(), all_sprites)
    field.start(hero, dice)
    running = True
    clock = pg.time.Clock()
    bg = StaticBackground('end_screen.png', [0, 0], size=SCREEN_SIZE)
    screen.fill((50, 41, 88))
    pg.display.set_icon(Loader.load_image('icon.png'))
    arrow = pg.sprite.Sprite(all_sprites)
    arrow.image = Loader.load_image('arrow.png')
    arrow.rect = arrow.image.get_rect()
    click_sound = Loader.load_sound('COOL CLICK.wav')
    click_sound.set_volume(0.25)
    pg.mouse.set_visible(False)
    all_sprites.add(arrow)
    fps = 60
    dice_tick = 0
    while running:
        if field.task_is_active():
            callback = field.current_game.loop(SCREEN_SIZE)
            if callback == 'closeEvent':
                running = False
            elif callback == 'victory':
                hero.add_live(1)
                field.disable_task()
            elif callback == 'loss':
                hero.add_live(-1)
                field.disable_task()
                if hero.get_live() == 0:
                    dice.visibled(sound=False)
                    finish(screen, field, hero, all_sprites, bg, callback)
        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    click_sound.play()
                    x, y = event.pos
                    if x <= 40 and y <= 40:
                        field.change_language()
                if event.type == pg.MOUSEMOTION:
                    arrow.rect.x, arrow.rect.y = pg.mouse.get_pos()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if hero.get_moves() == 0 and not field.is_finished():
                            field.show_dice(dice)
                            moves = dice.handle_rotating()
                            if moves:
                                hero.add_moves(moves)
                        elif field.is_finished():
                            field.start(hero, dice)
                    else:
                        callback = field.handle_move(event, hero, dice)
                        if callback == 'victory' or callback == 'loss':
                            finish(screen, field, hero, all_sprites, bg, callback)
            if not field.is_finished():
                field.render(screen, hero.get_moves(), hero.get_live(), bg)
                all_sprites.update()
                all_sprites.draw(screen)
            if dice.is_rotating():
                dice_tick += 1
                rotation = dice.rotate(dice_tick)
                if rotation:
                    dice_tick = 0
            pg.display.flip()
            clock.tick(fps)
    pg.quit()


if __name__ == '__main__':
    main()