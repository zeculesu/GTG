class ImageNotFoundError(FileNotFoundError):  # Исключение ненахождения картинки
    pass


class FontNotFoundError(FileNotFoundError):  # Исключение ненахождения шрифта
    pass


class SoundNotFoundError(FileNotFoundError):  # Исключение ненахождения звука/музыки
    pass


class ButtonInitializationError(Exception):
    pass