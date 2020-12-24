import os
import pygame as pg
from exceptions import ImageNotFoundError


class ImageLoader:
    @staticmethod
    def load_image(filename):
        try:
            image = pg.image.load(os.path.join('data', filename))
        except FileNotFoundError:
            raise ImageNotFoundError('Не удалось загрузить файл изображения %s' % filename)
        return image