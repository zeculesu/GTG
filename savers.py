from img_loader import ImageLoader
import pygame as pg


class StartScreen(ImageLoader):
    def __init__(self):
        pg.init()
        size = 700, 436
        screen = pg.display.set_mode(size)
        fon = ImageLoader.load_image('fon.png')
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
        super(EndScreen, self).__init__(group)
        self.hero = hero
        self.image = self.draw_saver()

    def draw_saver(self) -> pg.Surface:
        pass

    def update(self, *args, **kwargs):
        pass