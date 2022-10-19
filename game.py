"""System module."""
import random
import os

import pygame

import cellmem
from spritesheet import StritesSheet


class MemoryGame:
    '''The main class of the game.'''
    WIDTH = 500  # ширина игрового окна
    HEIGHT = 500  # высота игрового окна
    FPS = 60  # частота кадров в секунд
    num_cell_in_row = 4  # количесво яееек в ряду/столбце
    size_cell = 124

    # инициализация PyGame
    def __init__(self):
        self.b_need_reset = False
        self.b_win = False
        self.running = False
        self.open_cells = []
        self.cells_list = []
        self.rand_data = []
        self.sprites = []
        # Создаем группу для управления спрайтами ячеек
        self.cells_group = pygame.sprite.Group()
        self.win_group = pygame.sprite.Group()
        temp_cell_size = (MemoryGame.size_cell, MemoryGame.size_cell)
        self.default_image = pygame.Surface(temp_cell_size)
        self.press_image = pygame.Surface(temp_cell_size)
        self.onhover_image = pygame.Surface(temp_cell_size)

    def load_img(self):
        '''To upload images.'''
        size_fone = 124
        # загружаем рисунки закрытых ячеек
        strites_sheet_fone = StritesSheet(os.path.join("resource", "BackGroundImg.png"))
        self.default_image = strites_sheet_fone.get_sprite(0, 0, MemoryGame.size_cell, MemoryGame.size_cell)
        self.press_image = strites_sheet_fone.get_sprite(0, size_fone, MemoryGame.size_cell, MemoryGame.size_cell)
        self.onhover_image = strites_sheet_fone.get_sprite(0, size_fone * 2, MemoryGame.size_cell, MemoryGame.size_cell)

        # создаем спрайт WinScreen и загружаем для него изображение
        win_screen = pygame.sprite.Sprite()
        win_screen.image = pygame.image.load(os.path.join("resource", "winscreen.png")).convert()
        win_screen.rect = win_screen.image.get_rect()
        win_screen.rect.centery = MemoryGame.WIDTH / 2
        win_screen.rect.centerx = MemoryGame.HEIGHT / 2
        self.win_group.add(win_screen)

        strites_sheet = StritesSheet(os.path.join("resource", "picture.png"))
        # создаем список для храннеия картинок
        self.sprites = []
        sprite_size_y = 128
        # картинка не удачная по расположению спрайтов, по этому отказались от цикла
        # задаем смещение для первого столбца
        offset_y = 2
        offset_x1 = 22
        self.sprites.append(strites_sheet.get_sprite(offset_x1, offset_y, MemoryGame.size_cell, MemoryGame.size_cell))
        self.sprites.append(
            strites_sheet.get_sprite(offset_x1, sprite_size_y + offset_y, MemoryGame.size_cell, MemoryGame.size_cell))
        self.sprites.append(strites_sheet.get_sprite(offset_x1, sprite_size_y * 2 + offset_y, MemoryGame.size_cell,
                                                     MemoryGame.size_cell))
        self.sprites.append(strites_sheet.get_sprite(offset_x1, sprite_size_y * 3 + offset_y, MemoryGame.size_cell,
                                                     MemoryGame.size_cell))
        # задаем смещение для второго столбца
        offset_x2 = 194
        self.sprites.append(strites_sheet.get_sprite(offset_x2, offset_y, MemoryGame.size_cell, MemoryGame.size_cell))
        self.sprites.append(
            strites_sheet.get_sprite(offset_x2, sprite_size_y + offset_y, MemoryGame.size_cell, MemoryGame.size_cell))
        self.sprites.append(strites_sheet.get_sprite(offset_x2, sprite_size_y * 2 + offset_y, MemoryGame.size_cell,
                                                     MemoryGame.size_cell))
        self.sprites.append(strites_sheet.get_sprite(offset_x2, sprite_size_y * 3 + offset_y, MemoryGame.size_cell,
                                                     MemoryGame.size_cell))

    def make_rand_data(self):
        '''Make random position of pictures.'''
        num_cell = MemoryGame.num_cell_in_row * MemoryGame.num_cell_in_row
        need_num_picture = int(num_cell / 2)
        # заполняем случайные данные индексами картинок
        self.rand_data = list(range(0, need_num_picture))
        self.rand_data = self.rand_data * 2
        # перемешиваем значения
        for i in range(0, num_cell):
            # генерируем новую позицию
            new_index = random.randint(0, num_cell - 1)
            #  меняем значения местами
            buffer = self.rand_data[i]
            self.rand_data[i] = self.rand_data[new_index]
            self.rand_data[new_index] = buffer

    def make_cell(self):
        '''Make sprite cell.'''
        # для вызова фунций класса Cell_mem создали отдельный список ячеек
        self.cells_list = []
        self.make_rand_data()
        self.b_win = False

        index = 0
        for i in range(MemoryGame.num_cell_in_row):
            for j in range(MemoryGame.num_cell_in_row):
                cell = cellmem.CellMem(MemoryGame.size_cell - 1, MemoryGame.size_cell - 1,
                                       i * MemoryGame.size_cell + MemoryGame.size_cell / 2 + 1,
                                       j * MemoryGame.size_cell + MemoryGame.size_cell / 2 + 1,
                                       self.rand_data[index],
                                       self.sprites[self.rand_data[index]],
                                       self.press_image,
                                       self.onhover_image,
                                       self.default_image)
                index += 1
                self.cells_group.add(cell)
                self.cells_list.append(cell)

    def check_new_open_cell(self):
        '''Сheck cells for a match.'''
        # храним открытые ячейки до сброса или до следующей проверки.
        self.open_cells = []
        # ищем открытые ячейки, которые еще в игре
        for cell in self.cells_list:
            if cell.b_in_game and cell.is_open():
                self.open_cells.append(cell)
                if len(self.open_cells) == 2:
                    break

        # если ячеек 2 , то проверяем на совпадение
        num_open_cells = len(self.open_cells)
        if num_open_cells == 2:
            if self.open_cells[0].get_id() == self.open_cells[1].get_id():
                # убираем из игры совпавшие ячейки
                self.open_cells[0].b_in_game = False
                self.open_cells[1].b_in_game = False
            else:
                # ставим флаг сброса, его проверим на следующем нажатии мышки
                self.b_need_reset = True

    # делаем отдельный сброс для кнопок, чтобы открытые кнопки были видны до следующего нажатия мышки
    def reset_open_cell(self):
        '''Reset open cell.'''
        if self.b_need_reset:
            # закрываем открытые ячейки
            for cell in self.open_cells:
                cell.reset_click()
            self.b_need_reset = False

    def check_win(self):
        '''Check win the game or not.'''
        # если нету ячеек в игре, то переходим к состоянию выигрыша
        for cell in self.cells_list:
            if cell.b_in_game:
                return False
        return True

    def show_win_screen(self, screen):
        '''To draw a winning screen, start a new game or close game.'''
        self.win_group.draw(screen)
        for event in pygame.event.get():
            # управление событиями игры, получаем события из очереди
            if event.type == pygame.QUIT:
                # выход из игры по нажатию на крестик
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # запуск новой игры по нажатию мыши
                self.make_cell()

    # цикл игры
    def process_game(self):
        '''Game loop.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # выход из игры по нажатию на крестик
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # переворот несовпавших ячеек на тыльную сторону
                self.reset_open_cell()
                # передаем событие нажатия мыши ячейкам
                for cell in self.cells_list:
                    cell.try_press()
            elif event.type == pygame.MOUSEBUTTONUP:
                # передаем событие отпускания мыши
                for cell in self.cells_list:
                    cell.try_release()

        # проверяем условие подебы
        self.b_win = self.check_win()

    def start_game(self):
        '''Start game.'''
        # Инициализация данных pygame
        pygame.init()  # инициализация модуля дисплея
        screen = pygame.display.set_mode((MemoryGame.WIDTH, MemoryGame.HEIGHT))  # инициализирует окно для отображения
        pygame.display.set_caption("MEMORY")  # установка заголовка текущего окна
        clock = pygame.time.Clock()  # создаем объект для управления времени

        self.load_img()
        self.make_cell()
        # запускаем игровой цикл
        self.running = True
        while self.running:
            clock.tick(MemoryGame.FPS)
            if self.b_win:
                self.show_win_screen(screen)
            else:
                # обновление
                self.process_game()
                self.cells_group.update()
                self.check_new_open_cell()
                # очистить фон
                screen.fill((0, 0, 0))
                # рендер
                self.cells_group.draw(screen)

            # вывод картинки на экран
            pygame.display.flip()

        # выход из игры
        pygame.quit()


# запускаем игру
MemoryGame = MemoryGame()
MemoryGame.start_game()
