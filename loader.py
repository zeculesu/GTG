import os
import pygame as pg
from exceptions import ImageNotFoundError, FontNotFoundError


class Loader:
    @staticmethod
    def load_image(filename):
        try:
            image = pg.image.load(os.path.join('data', 'img', filename))
        except FileNotFoundError:
            raise ImageNotFoundError('Не удалось загрузить файл изображения %s' % filename)
        return image

    @staticmethod
    def load_font(fontname, size):
        try:
            font = pg.font.Font(os.path.join('data', 'font', fontname), size)
        except FileNotFoundError:
            raise FontNotFoundError('Не удалось загрузить файл шрифта %s' % fontname)
        return font