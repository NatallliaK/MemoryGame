"""Import pygame module."""
import pygame


# определяем наш собственный класс Cell_mem, наследуя его от базового класса Sprite
class CellMem(pygame.sprite.Sprite):
    """Render the state of cell, process input mouse."""

    def __init__(self, size_x: int,
                 size_y: int,
                 location_x: int,
                 location_y: int,
                 image_id: int,
                 open_image: pygame.Surface,  # управление изображениями и экраном
                 press_image: pygame.Surface,
                 onhover_image: pygame.Surface,
                 default_image: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)  # запускает инициализатор встроенных классов Sprite
        self.image = pygame.Surface((size_x, size_y))  # графическое представление спрайта
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()  # положение и размер спрайта
        self.rect.centerx = location_x
        self.rect.centery = location_y
        self.__b_onhover = False
        self.__b_press = False
        self.__b_click = False
        self.__id = image_id
        self.b_in_game = True
        self.open_image = open_image
        self.press_image = press_image
        self.onhover_image = onhover_image
        self.default_image = default_image

    # вернуть id ячейки
    def get_id(self):
        """Return get id."""
        return self.__id

    # проверяем открыта ли ячейка, возвращаем по ячейке произведен клик
    def is_open(self):
        """Check open a cell state."""
        return self.__b_click

    # Устанавливаем значения состояния наведения на ячейку
    def __onhover(self):
        """Set state onhover for a cell."""
        self.__b_onhover = True

    # Сбрасываем состояние "наведения" и "нажатия" на ячейку
    def __unhover(self):
        """Resert state onhover and press for a cell."""
        self.__b_onhover = False
        self.__b_press = False

    # Устанавливаем состояния нажатия на ячейку
    def __press(self):
        """Set state press for a cell."""
        self.__b_press = True

    # Сбрасываем состояния нажатия на ячейку
    def __release(self):
        """Reset state "press" for a cell."""
        self.__b_press = False

    # Устанавливаем состояние клика на ячейку
    def __click(self):
        """Set state "click" for a cell."""
        self.__b_click = True
        self.__b_onhover = False
        self.__b_press = False

    # Проверяем находится ли мышка над ячейкой
    def update_onhover(self):
        """Check the mouse hover on the cell."""
        mouse_position = pygame.mouse.get_pos()
        # проверить, находится ли точка внутри прямоугольника
        if self.rect.collidepoint(mouse_position[0], mouse_position[1]):
            self.__onhover()
        else:
            self.__unhover()

    # Обновляет картинку в ячейке взависимости от состояния
    def update_image(self):
        """We show a picture corresponding to the state of the cell: hovered, pressed, click."""
        if self.__b_click:
            self.image.blit(self.open_image, (0, 0), self.open_image.get_rect())
            return

        if self.__b_onhover:
            if self.__b_press:
                # нарисовать картинку (передаем картинку, положение, размер)
                self.image.blit(self.press_image, (0, 0), self.press_image.get_rect())
            else:
                self.image.blit(self.onhover_image, (0, 0), self.onhover_image.get_rect())
        else:
            self.image.blit(self.default_image, (0, 0), self.default_image.get_rect())

    # Переопределение родительской функиции update()
    def update(self):
        """Override pygame.sprite.update."""
        self.update_onhover()
        self.update_image()

    # Пытаемся нажать на ячейку. Если мышка находится над ячейкой
    # нажатие проходит успешно
    def try_press(self):
        """Try press on a cell."""
        if self.__b_onhover:
            self.__press()

    # Пытаемся отпустить ячейку. Если мышка находится над ячейкой
    # дейстие проходит успешно. Если состояние "press", то происходит "click"
    def try_release(self):
        """ Try release a cell."""
        if self.__b_onhover:
            if self.__b_press:
                self.__click()
            self.__release()

    # Сбрасываем состояние "click"
    def reset_click(self):
        """Reset click state."""
        if self.b_in_game:
            self.__b_click = False
