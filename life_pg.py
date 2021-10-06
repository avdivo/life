import pygame
import sys
from tkinter.filedialog import *
import queue


run = False
size_x = 155  # Количество клеточек по ширине
size_y = 85  # Количество клеточек по высоте
size_points = 7  # Размер клеточки
field = []
counter_step = 0
step = 0
counter_points = 0
change = queue.Queue()  # Очередь изменений
speed = 20  # Скорость. Минимальная 1

class Rectangle(object):
# Клеточки

    color_1 = [100, 100, 100]
    color_2 = [255, 0, 0]


    def __init__(self, sc, x, y):
        self.x = x  # Горизонтальная координата сетки
        self.y = y  # Вертикальная координата сетки
        self.activ = False  # Закрашен ли квадрат (клетка активна)

        global size_points
        coords = (x * (size_points + 1) + 1, y * (size_points + 1) + 1,
            size_points, size_points)
        self.sc = sc
        self.rect = pygame.draw.rect(sc, self.color_1, coords)

# Переключение клеточки
    def change_color(self):
        global counter_points
        self.activ = not self.activ
        color = self.color_2 if self.activ else self.color_1
        pygame.draw.rect(self.sc, color, self.rect)
        counter_points += 1 if self.activ else -1
        # count_point['text'] = counter_points


class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text


    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('arial', 14)
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text,
                     (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

sc = pygame.display.set_mode()
clock = pygame.time.Clock()
pygame.font.init()
infoObject = pygame.display.Info()  # Информационный объект
# Разрешение экрана
w = infoObject.current_w
h = infoObject.current_h

# Подготовка поля и массива его объектов
for y in range(size_y):
    string = []
    for x in range(size_x):
        string.append(Rectangle(sc, x, y))
    field.append(string)

b = button([0, 0, 1], 1250, 50, 60, 30, 'Click')
b.draw(sc, [255, 255, 255])
# обновляем окно
pygame.display.update()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Если щелчек на клетке получаем ее координаты.
                # Если на сетке или вне поля, то координаты будут больше
                x = event.pos[0] // (size_points + 1) if event.pos[0] % (size_points + 1) else 1000
                y = event.pos[1] // (size_points + 1) if event.pos[1] % (size_points + 1) else 1000
                print(event.pos[0], event.pos[1])
                if x < size_x and y < size_y:
                    field[y][x].change_color()

    pygame.display.update()
    clock.tick(10)

