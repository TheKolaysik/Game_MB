import pygame
import os
import sys


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)

    else:
        image = image.convert_alpha()
    return image


class Board:
    # создание поля
    def __init__(self, width, height, gamer, window):

        self.width = width
        self.height = height
        self.gamer = gamer
        self.board = [[0] * 10 for _ in range(10)]
        self.window = window
        # значения по умолчанию
        self.mode = 'plan'
        self.boats = 20

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        colors = [pygame.Color(0, 110, 255), pygame.Color(0, 0, 255), pygame.Color(255, 0, 0), pygame.Color(0, 255, 0)]

        if self.mode:
            for y in range(self.height):
                for x in range(self.width):
                    pygame.draw.rect(screen, colors[self.board[y][x]], (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                        self.cell_size))
                    pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                     1)

    def on_click(self, cell):
        if self.mode == "plan":
            if self.count < 19:
                self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2
                if (self.board[cell[1]][cell[0]] + 1) % 2 == 1:
                    self.count -= 1
                elif (self.board[cell[1]][cell[0]] + 1) % 2 == 0:
                    self.count += 1
            else:
                if self.gamer == 1:
                    self.window.set_board1(self.board)
                elif self.gamer == 2:
                    self.window.set_board2(self.board)
                self.running = False
        else:
            if self.gamer == 1:
                if self.window.get_coords2(cell[1], cell[0]) == 1:
                    self.board[cell[1]][cell[0]] = 2
                    self.boats -= 1
                else:
                    self.board[cell[1]][cell[0]] = 3
            elif self.gamer == 2:
                if self.window.get_coords1(cell[1], cell[0]) == 1:
                    self.board[cell[1]][cell[0]] = 2
                    self.boats -= 1
                else:
                    self.board[cell[1]][cell[0]] = 3
            if self.boats == 0:
                terminate()
                self.window.finish_game(self.gamer)
            self.running = False
            self.board2.running_game()
        print(cell)

    # Получение координат
    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)  # возвращает координаты клетки в виде кортежа
        self.on_click(cell)  # как-то изменяет поле, опираясь на полученные координаты клетки

    def running_game(self):
        pygame.init()
        self.count = 0
        size = width, height = 400, 400
        if self.gamer == 1:
            pygame.display.set_caption('Игрок Первый')
        else:
            pygame.display.set_caption('Игрок Второй')
        screen = pygame.display.set_mode(size)
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.board1.get_click(event.pos)
            self.board1.render(screen)
            pygame.display.flip()
        pygame.quit()

    def strun(self, data, data1):
        self.board1 = data
        self.board2 = data1

    def set_mode(self):
        self.mode = "game"
        self.board = [[0] * 10 for _ in range(10)]
