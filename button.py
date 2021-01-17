import pygame as pg
from typing import Union

from loader import Loader
from exceptions import ButtonInitializationError


class Button(pg.sprite.Sprite):  # Класс кнопки
    def __init__(self, screen: pg.Surface, image: str,
                 edge: str, group: pg.sprite.AbstractGroup,
                 is_active: bool = False):
        super(Button, self).__init__(group)
        if not isinstance(image, str):
            raise ButtonInitializationError('Изображение должно быть одно')
        self.image = Loader.load_image(image)
        img_width, img_height = self.image.get_size()
        screen_width, screen_height = screen.get_size()
        position_translate = {'top_left': 'bottomright=(img_width, img_height)',
                              'top_right': 'bottomleft=(screen_width - img_width, img_height)'}
        self.rect = eval('self.image.get_rect(%s)' % position_translate[edge])

        self.active = is_active

    def is_activated(self) -> bool:
        return self.active

    def activate(self):
        self.active = not self.is_activated

    def handle_event(self, event: pg.event.Event):  # Активировать при нажатии
        x, y = event.pos
        if ((self.rect.x <= x <= self.rect.x + self.image.get_width() and
             self.rect.y <= y <= self.rect.y + self.image.get_height())):
            self.activate()
            return True
        return False


class MultiButton(Button):  # Класс кнопки с изменяющимися картинками
    def __init__(self, screen: pg.Surface, images: Union[tuple, list],
                 edge: str, group: pg.sprite.AbstractGroup,
                 is_active: bool = False):
        if not any(map(lambda x: isinstance(images, x), [tuple, list])):
            raise ButtonInitializationError('Неверный формат массива изображений')
        super(MultiButton, self).__init__(screen, images[0], edge, group)
        self.images = [self.image] + [Loader.load_image(img) for img in images[1:]]
        if is_active:
            self.swap()

    def activate(self):
        self.active = not self.is_activated
        self.swap()

    def swap(self) -> None:  # Поменять картинку на следующую в списке
        self.image = self.images[(self.images.index(self.image) + 1) % len(self.images)]
