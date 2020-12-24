import pygame as pg


class Hero(pg.sprite.Sprite):
    hero = pg.image.load('data/itachi.jpg')
    hero = pg.transform.scale(hero, (60, 60))
    hero.set_colorkey((255, 255, 255))

    def __init__(self, screen, group: pg.sprite.AbstractGroup):
        self.screen = screen
        super(Hero, self).__init__(group)
        self.live = 3
        self.size_hero = 60
        self.task_quantity = 0
        self.health_quantity = 0
        self.trap_quantity = 0
        self.teleport_quantity = 0
        self.motion = 0

    def move_hero(self, current_cell):
        Hero.hero_rect = Hero.hero.get_rect(
            bottomright=(self.size_hero * (current_cell[0] + 1), self.size_hero * (current_cell[1] + 1)))
        self.screen.blit(Hero.hero, Hero.hero_rect)
