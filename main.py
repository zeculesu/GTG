import pygame as pg

from field import Field
from hero import Hero
from dice import Dice
from savers import StartScreen, EndScreen


def main():
    StartScreen()
    pg.init()
    size = 760, 760
    screen = pg.display.set_mode(size)
    pg.display.set_caption('Goof the Game')
    all_sprites = pg.sprite.Group()
    field = Field(screen, all_sprites)
    hero = Hero((0, 0), field.get_indent(), all_sprites)
    dice = Dice(field.get_size(), field.get_indent(), all_sprites)
    field.start(screen, hero, dice)
    running = True
    clock = pg.time.Clock()
    fps = 60
    screen.fill((50, 41, 88))
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if hero.get_moves() == 0:
                        field.show_dice(dice)
                        moves = dice.handle_rotating()
                        if moves:
                            hero.add_moves(moves)
                    elif field.is_finished():
                        field.start(screen, hero, dice)
                else:
                    callback = field.handle_move(event, hero, dice)
                    if callback == 'end-screen':
                        EndScreen(hero, all_sprites)
                    clock.tick(fps)
            field.render(screen, hero.get_moves(), hero.get_live())
        if dice.is_rotating():
            dice.rotate()
        all_sprites.update()
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(10)
    pg.quit()


if __name__ == '__main__':
    main()