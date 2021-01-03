import pygame as pg
from field import Field
from hero import Hero
from dice import Dice
from loader import Loader
from savers import StartScreen, EndScreen, Background


def main():
    start_screen = StartScreen()
    proceeded = start_screen.show()
    if not proceeded:
        return
    pg.init()
    size = 760, 760
    screen = pg.display.set_mode(size)
    pg.display.set_caption('Goof the Game')
    all_sprites = pg.sprite.Group()
    field = Field(screen, all_sprites)
    hero = Hero((0, 0), field.get_indent(), all_sprites)
    dice = Dice(field.get_size(), field.get_indent(), all_sprites)
    field.start(hero, dice)
    running = True
    clock = pg.time.Clock()
    img = Loader.load_image('end_screen.png')
    img = pg.transform.scale(img, (760, 760))
    bg = Background(img, [0, 0])
    screen.fill((50, 41, 88))
    pg.display.set_icon(Loader.load_image('icon.png'))
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
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
                    if callback == 'end-screen':
                        field.render(screen, hero.get_moves(), hero.get_live(), bg)
                        all_sprites.update()
                        all_sprites.draw(screen)
                        EndScreen(screen, hero, all_sprites)
        if not field.is_finished():
            field.render(screen, hero.get_moves(), hero.get_live(), bg)
            all_sprites.update()
            all_sprites.draw(screen)
        if dice.is_rotating():
            dice.rotate()
            fps = 10
        else:
            fps = 60
        pg.display.flip()
        clock.tick(fps)
    pg.quit()


if __name__ == '__main__':
    main()