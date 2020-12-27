from loader import Loader
import pygame as pg


class StartScreen(Loader):
    def __init__(self):
        pg.init()
        size = 700, 436
        screen = pg.display.set_mode(size)
        fon = Loader.load_image('fon.png')
        screen.blit(fon, (0, 0))
        pg.display.flip()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    pg.quit()
                    return


class EndScreen(pg.sprite.Sprite):
    def __init__(self, hero, group):
        # super(EndScreen, self).__init__(group)
        # self.hero = hero
        # self.image = self.draw_saver()
        if hero.get_live() == 0:
            print('you died, you are loh')
        else:
            print('you won (no, you are still loh), congratulations')
        print('cell passed: %d' % hero.get_passed_cells())

    def draw_saver(self) -> pg.Surface:
        pass

    def update(self, *args, **kwargs):
        pass