import pygame as pg


class Cell(pg.sprite.Sprite):
    pass


class Trap(Cell):
    img_name = 'trap.png'
    pass


class Health(Cell):
    pass


class Task(Cell):
    pass


class Teleport(Cell):
    pass