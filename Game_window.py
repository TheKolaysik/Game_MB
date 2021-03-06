import pygame
import os
import sys


# Завершение работы окна
def terminate():
    pygame.quit()
    sys.exit()


# Игровое окно
class Board:
    # создание поля
    def __init__(self, width, height, gamer, window):
        self.width = width
        self.height = height
        self.gamer = gamer
        self.board = [[0] * 10 for _ in range(10)]
        self.window = window
        self.mode = 'plan'
        self.boats = 20

    # Указание размеров
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # Отображение данных клеток
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

    # Действие при нажании кнопки мыши
    def on_click(self, cell):
        # Расстановка кораблей
        if self.mode == "plan":
            if self.count < 20:
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
        # Атака кораблей противника
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
                self.window.adder_item(self.name, data1=1)
                self.window.adder_item(self.name2, data2=1)
                self.window.res_window()
                self.finish_screen()
                terminate()
            self.running = False
            self.board2.running_game()

    # Получение координат
    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)  # возвращает координаты клетки в виде кортежа
        self.on_click(cell)  # Изменяет поле, опираясь на полученные координаты клетки

    # Обновление данных экрана
    def running_game(self):
        pygame.init()
        self.count = 0
        size = 400, 400
        pygame.display.set_caption(f'Игрок {self.name}')
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

    # Стартовое окно
    def start_screen(self):
        if self.mode == "plan":
            intro_text = ["", "",
                          "Укажите расположение своих кораблей.",
                          "Ваша цель одолеть противника,",
                          "уничтожив все его корабли.", "", "",
                          "Нажмите любую кнопку  ..."]
            intro_text[0] = f"Игрок {self.name}"
        else:
            intro_text = ["ИГРА НАЧАЛАСЬ", "", "", "", "", "", "", "Нажмите любую кнопку  ..."]
        pygame.init()
        size = 400, 400
        clock = pygame.time.Clock()
        pygame.display.set_caption(f'Игрок {self.name}')
        screen = pygame.display.set_mode(size)
        screen.fill((255, 255, 0))
        font = pygame.font.Font(None, 25)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 20
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            clock.tick(50)

    # Концовка
    def finish_screen(self):
        pygame.init()
        size = 400, 400
        clock = pygame.time.Clock()
        pygame.display.set_caption('Результат')
        intro_text = ["Победил", "Игрок", str(self.name)]
        screen = pygame.display.set_mode(size)
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 40)
        text_coord = 70
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 20
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            clock.tick(50)

    # Передача поля
    def strun(self, data, data1):
        self.board1 = data
        self.board2 = data1

    # Выбор режима поля
    def set_mode(self):
        self.mode = "game"
        self.board = [[0] * 10 for _ in range(10)]

    # Указание имени действующего игрока
    def set_name(self, name):
        self.name = name

    # Указание имени другого игрока
    def set_name2(self, name):
        self.name2 = name
