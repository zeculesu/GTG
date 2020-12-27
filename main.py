import pygame as pg
from pygame.locals import *
from field import Field
from hero import Hero
from dice import Dice
from loader import Loader
from savers import StartScreen, EndScreen


class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = image_file
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


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
    field.start(hero, dice)
    running = True
    clock = pg.time.Clock()
    fps = 60
    img = Loader.load_image('end_screen.png')
    img = pg.transform.scale(img, (760, 760))
    backGround = Background(img, [0, 0])
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
                        field.start(hero, dice)
                else:
                    callback = field.handle_move(event, hero, dice)
                    if callback == 'end-screen':
                        EndScreen(hero, all_sprites)
                    clock.tick(fps)
            field.render(screen, hero.get_moves(), hero.get_live(), backGround)
        if dice.is_rotating():
            dice.rotate()
        all_sprites.update()
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(10)
    pg.quit()


if __name__ == '__main__':
    main()