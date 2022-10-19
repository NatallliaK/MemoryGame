"""Import pygame module."""
import pygame


# Класс для работы с картинками
class StritesSheet:
    """Class for work with picture."""

    # конструтор, на вход подаем адрес картинки
    def __init__(self, filename: str):
        self.__sprite_sheet = pygame.image.load(filename).convert()

    # Получаем область картинки с заданными размерами и координатами
    def get_sprite(self, x: int, y: int, w: int, h: int):
        """X,Y - coordinates, W,H - size. Return pygame.Surface."""
        sprite = pygame.Surface((w, h))
        sprite.blit(self.__sprite_sheet, (0, 0), (x, y, w, h))
        return sprite
