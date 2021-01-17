import os
import pygame as pg
from exceptions import ImageNotFoundError, FontNotFoundError, SoundNotFoundError


class Loader:
    pg.mixer.init()

    @staticmethod
    def load_image(filename: str) -> pg.Surface:
        try:
            image = pg.image.load(os.path.join('data', 'img', filename))
        except FileNotFoundError:
            raise ImageNotFoundError('Не удалось загрузить файл изображения %s' % filename)
        return image

    @staticmethod
    def load_font(fontname: str, size: int) -> pg.font.Font:
        try:
            font = pg.font.Font(os.path.join('data', 'font', fontname), size)
        except FileNotFoundError:
            raise FontNotFoundError('Не удалось загрузить файл шрифта %s' % fontname)
        return font

    @staticmethod
    def load_sound(filename: str) -> pg.mixer.Sound:
        try:
            sound = pg.mixer.Sound(os.path.join('data', 'music', filename))
        except FileNotFoundError:
            raise SoundNotFoundError('Не удалось загрузить звуковой файл %s' % filename)
        return sound

    @staticmethod
    def load_level(filename: str) -> list:
        filename = "data/map/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        return list(level_map)