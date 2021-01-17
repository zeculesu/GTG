import pygame as pg
from random import choice
from loader import Loader


class Dice(pg.sprite.Sprite, Loader):  # Класс костей, использующихся для получения ходов
    img_names = ['dice_1.png', 'dice_2.png', 'dice_3.png',  # Список картинок всех сторон
                 'dice_4.png', 'dice_5.png', 'dice_6.png']
    drop_sound = Loader.load_sound('dice-stop.wav')  # Подгрузка звука выпадения костей
    drop_sound.set_volume(0.2)

    def __init__(self, field_size: tuple, field_indent: tuple, group: pg.sprite.AbstractGroup):
        super(Dice, self).__init__(group)
        self.images = [pg.transform.scale(self.load_image(img), (150, 150))
                       for img in Dice.img_names]  # Корректировка изображений
        self.image = self.images[0]  # Текущая картинка
        self.rect = self.image.get_rect()  # Текущие координаты картинки
        self.img_width, self.img_height = self.image.get_size()  # Ширина и высота картинки
        self.field_size = field_size  # Размер поля
        self.field_indent = field_indent  # Отступ поля для корректного отображения картинки
        self.rotating = True  # Булево значение вращения костей
        self.show()  # Начать процесс вращения

    def is_rotating(self) -> bool:  # Возвращает, крутится ли сейчас кубик
        return self.rotating

    def show(self):  # Показывает и позиционирует кубик
        self.rotating = True
        self.rect.x = self.field_indent[0] + self.field_size[0] // 2 - self.img_width // 2
        self.rect.y = self.field_indent[1] + self.field_size[1] // 2 - self.img_height // 2

    def hide(self, sound: bool = True):  # Перестает вращать, включает звук падения, убирает кубик
        self.rotating = False
        if sound:
            Dice.drop_sound.play()
        pg.time.wait(500)
        self.rect.x = -1000
        self.rect.y = -1000

    def handle_rotating(self):  # Убирает кубик и возвращает значение текущей картинки
        self.hide()
        return self.images.index(self.image) + 1

    def rotate(self, tick: int) -> bool:  # С определённой частотой меняет сторону кубика на случайную
        if self.rotating and tick == 5:
            idx = self.images.index(self.image)
            self.image = choice(self.images[:idx] + self.images[idx + 1:])
            return True
        return False