# Общий алгоритм
# 1. Выводим состояние клеточек из массива вывода на экран если в массиве что то есть.
# В массиве вывода объекты, состояние которых должно быть изменено.
# Перед выводом очищаем подготовительный массив и во время вывода в него заносим клеточки
# которые активны и все их соседи. Текущий цвет их записываем в их прошлое (свойство old).
# Массив типа set, поэтому объекты в него попадают только один раз.
# 2. Вычисляем будущее состояние каждой клеточки в подготовительном массиве используя правила
# переключения. При этом новое состояние записываем в текущее состояние, а при вычислении
# используем их свойства old. Клеточки которые не были активными и не становятся - удаляются
# из массива.
# 3. Опрашиваем органы управления. При обнаружении переключения клеточки вносим изменения в массив
# вывода, повторно запускаем п. 1 и 2. Ждем окончания итерации в цикле п.3
# 4. Копируем подготовительный массив в массив вывода. Переходим к началу.

import pygame
import sys, time, queue, random
from collections import Counter
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

run = False
size_x = 155  # Количество клеточек по ширине
size_y = 95  # Количество клеточек по высоте
size_points = 7  # Размер клеточки
field = []
counter_step = 0
step = 0
counter_points = 0
change = queue.Queue()  # Очередь изменений
speed = 0  # Скорость. Задержка в секундах между кадрами
repair = set()  # Массив для подготовки
out = set()  # Массив для вывода
userEvent = pygame.USEREVENT + 1  # Пользовательское событие возникает после нажатия кнопки


class Rectangle(object):
    color_1 = [100, 100, 100]

    def __init__(self, sc, x, y):
        self.x = x  # Горизонтальная координата сетки
        self.y = y  # Вертикальная координата сетки
        self.color = 6  # Цвет клетки (6 - нет цвета, остальные цвета как в Palette)
        self.old_color = 6
        self.neighbors = set() # Соседи клеточки

        global size_points
        coords = (x * (size_points + 1) + 1, y * (size_points + 1) + 1,
                  size_points, size_points)
        self.sc = sc
        self.rect = pygame.draw.rect(sc, self.color_1, coords)

    # Переключение клеточки при щелчке. Цвет из палитры
    def change_color(self):
        self.color = 6 if self.color == palette.activ_rect.color_num else palette.activ_rect.color_num


    # Рисование клеточки
    def show_cell(self):
        global counter_points
        palette.change_color(self.old_color, self.color)  # Меняем счетчик в палитре
        self.old_color = self.color
        counter_points += 1 if self.color != 6 else -1
        pygame.draw.rect(self.sc, palette.colors[self.color], self.rect)
        count_point.update_label(str(counter_points))  # Меняем общий счетчик клеточек


    # Список состояний соседей свойства old_color
    def status_old(self):
        return list(old.old_color for old in self.neighbors)


    # Приводим состояние соседей в положение как до старта и возвращяем их список
    def cast_neighbors(self):
        for cell in self.neighbors:
            cell.old_color = cell.color
        return self.neighbors

class Button():
    # Класс кнопка. Выполняет функцию заданную при нажатии. Помнит все свои кнопки. После нажатия
    # кнопки подсвечивает ее, устанавливает событие, которое запускает функцию погашения подсветки
    all_buttons = []

    def __init__(self, sc, x, y, width, height, text='', func=None):
        self.color = (255, 255, 255)  # рамки и текста
        self.color2 = (0, 0, 0)  # Фон кнопки
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.sc = sc
        self.func = func
        self.disabled = False
        pygame.draw.rect(self.sc, self.color, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        self.rect = pygame.draw.rect(self.sc, self.color2, (self.x, self.y, self.width, self.height), 0)
        Button.all_buttons.append(self)
        self.text_write(1)

    def text_write(self, press=0):
        color = self.color if press else self.color2
        if self.text != '':
            font = pygame.font.SysFont('arial', 14)
            text = font.render(self.text, 1, color)
            self.sc.blit(text,
                         (self.x + (self.width / 2 - text.get_width() / 2),
                          self.y + (self.height / 2 - text.get_height() / 2)))

    def button_press(self, press=0):
        if press:
            pygame.draw.rect(self.sc, self.color, self.rect)
            self.text_write(0)
            pygame.time.set_timer(userEvent, 100)
        else:
            for but in Button.all_buttons:
                pygame.draw.rect(but.sc, but.color2, but.rect)
                but.text_write(1)
            pygame.time.set_timer(userEvent, 0)

    def cange_text(self, text):
        self.text = text
        self.button_press(1)
        self.text_write()

    def dis(self, dis=True):
        # Переключение кнопки (активнв / не активна)
        if dis:
            self.disabled = True
            self.color = (100, 100, 100)
            self.text_write()
        else:
            self.disabled = False
            self.color = (255, 255, 255)
            self.text_write()

    def isPress(pos):
        # Проверка, нажата ли одна из кнопок, выполнение заданной функции если нажата
        for but in Button.all_buttons:
            if but.rect.collidepoint(pos):
                if not but.disabled:
                    but.button_press(1)
                    but.func()
                    return True
        return False


class Label():
    # Класс для вывода и изменения текстав красным цветом
    def __init__(self, sc, x, y, text=''):
        self.text = text
        self.sc = sc
        self.x = x
        self.y = y
        self.font_size = 33
        self.color = (255, 0, 0)
        self.f1 = pygame.font.SysFont('arial', self.font_size)
        self.write_label()

    def write_label(self):
        self.surface = self.f1.render(self.text, True, self.color)
        self.sc.blit(self.surface, (self.x, self.y))

    def clear_label(self):
        self.surface.fill((0, 0, 0))
        sc.blit(self.surface, (self.x, self.y))

    def update_label(self, text=''):
        self.text = text
        self.clear_label()
        if text:
            self.write_label()


class Palette():
    # Палитра для выбора активного цвета и отображения количества клеточек каждого цвета

    def __init__(self, sc, x, y):
        # Цвета: 0 - черный, 1 - белый, 2 - желтый, 3 - красный, 4 - зеленый, 5 - синий
        self.colors = ((0, 0, 0), (255, 255, 255), (255, 255, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (100, 100, 100))
        self.x = x # Координаты палитры по горизонтали
        self.y = y # Координаты палитры по вертикали
        self.width = 45 # Ширина клеточки с рамкой
        self.height = 30 # Высота клеточки с рамкой
        self.gap = 4 # Расстояние между клеточками
        self.cells = [] # Объекты клеток
        r = pygame.draw.rect(sc, (255, 255, 255), (self.x, self.y, self.width*2+self.gap, self.height), 1)
        self.activ_rect = self.Cell(self, sc, r, 3) # Объект с rect и цветом
        self.activ_rect.draw_cell()

        for i in range(6):
            y = self.y + (self.height + self.gap) * ((i+2)//2)
            x = self.x + (self.width + self.gap) * (i%2)
            r = pygame.draw.rect(sc, (255, 255, 255), (x, y, self.width, self.height), 1) # Объект Rect клетки цвета
            new_cell = self.Cell(self, sc, r, i)
            self.cells.append(new_cell) # Объект с rect и цветом
            new_cell.draw_cell()
            new_cell.write_cell()

    def change_color(self, color_old, color_new):
        # Учет счетчиков цветов клеточек в палитре. Получает старый и новый цвета
        if color_old < 6:
            cell = self.cells[color_old]
            cell.color_counter_plus(-1)
        if color_new < 6:
            cell = self.cells[color_new]
            cell.color_counter_plus(1)

    def isPress(self, pos):
        # Проверка, нажата ли одна из клеток палитры
        for cell in self.cells:
            if cell.rect.collidepoint(pos):
                self.activ_rect.color = cell.color
                self.activ_rect.color_num = cell.color_num
                self.activ_rect.draw_cell()

    class Cell():
        # Класс хранит цветовые ячейки и объекты Rect

        def __init__(self, self_up, sc, rect, color_num):
            self.rect = rect
            self.color = self_up.colors[color_num]
            self.color_num = color_num
            self.sc = sc
            self.count = 0 # Количество клеточек этого цвета
            self.self_up = self_up # Объект выше (этот класс вложенный)
            self.font = pygame.font.SysFont('arial', 18)


        def draw_cell(self):
            # Принимает объект rect, закрашивает внутреннюю часть с отступом
            pygame.draw.rect(self.sc, self.color, (self.rect.left + 2, self.rect.top + 2,
                                                   self.rect.width - 4, self.rect.height - 4))

        def write_cell(self):
            # Вписывает количество клеточек такого цвета
            color = (0, 0, 0) if self.color in ((255, 255, 255), (255, 255, 0), (0, 255, 0)) else (255, 255, 255)
            text = self.font.render(str(self.count), 1, color)
            self.sc.blit(text,
                         (self.rect.x + (self.rect.width / 2 - text.get_width() / 2),
                          self.rect.y + (self.rect.height / 2 - text.get_height() / 2)))

        def color_counter_plus(self, param):
            # Увеличиваем или уменьшаем счетчик цвета, ячейку перерисовываем
            # Принимает 1 или -1
            self.count += param
            self.draw_cell()
            self.write_cell()


#            Функции

# Кнопка Пауза
def click_pause():
    global run
    if run:
        run = False
        step_btn.dis(False)
        start_stop_btn.cange_text('Старт')
    else:
        run = True
        step_btn.dis(True)
        start_stop_btn.cange_text('Стоп')
        prestart()


# Кнопка 1 шаг
def step_fun():
    global step, counter_step
    step = 1
    click_pause()
    counter_step += 1
    count.update_label(str(counter_step))


# Кнопка Очистка
def click_clear():
    global counter_points
    for y in range(size_y):
        for x in range(size_x):
            if field[y][x].color < 6 or field[y][x].old_color < 6:
                field[y][x].color = 6
                field[y][x].show_cell()
    counter_points = 0
    count_point.update_label(str(counter_points))
    count_reset_fun()

# Кнопка Открыть
def open_file():
    root = Tk()
    root.withdraw()
    name_file = askopenfilename(filetypes=[("Life файл", "*.life")])
    root.destroy()
    if name_file:
        with open(name_file, encoding='utf-8') as f:
            new = f.read().split('\n')
            color = []
            if new[0] == '-3-':
                color = new[2]
                del new[2]
                del new[0]
            new = new[0].split(' ')
            del new[-1]
            if not len(color):
                color = '3' * (len(new) // 2)
            color = list(color)
            click_clear()
            for i in range(len(color)):
                field[int(new[i*2 + 1])][int(new[i*2])].color = int(color[i])
                field[int(new[i * 2 + 1])][int(new[i * 2])].show_cell()


# Кнопка Сохранить.
# Сохраняет координаты x, y через пробелы только активных клеточек
# Второй строкой цвета этих клеточек через пробелы
# В первой строке -3- Для этой версии программы

def save_file():
    root = Tk()
    root.withdraw()
    name_file = asksaveasfilename(filetypes=[("Life файл", "*.life")])
    root.destroy()
    if name_file:
        if name_file[len(name_file) - 5:] != '.life':
            name_file += '.life.'
        st = ''
        color = ''
        for y in range(size_y):
            for x in range(size_x):
                if field[y][x].color < 6:
                    st += str(field[y][x].x) + ' ' + str(field[y][x].y) + ' '
                    color += str(field[y][x].color)
        st = '-3-\n' + st + '\n' + color
        with open(name_file, "w") as f:
            f.write(st)


# Кнопка сброс счетчика шагов
def count_reset_fun():
    global counter_step
    counter_step = 0
    count.update_label(str(counter_step))


# Кнопка Рассановка/удаление позиционных точек
def position_fun():
    pos = ((size_x // 4, size_y // 4), (size_x // 4 * 3, size_y // 4), (size_x // 2, size_y // 2),
           (size_x // 4, size_y // 4 * 3), (size_x // 4 * 3, size_y // 4 * 3))
    for i in pos:
        field[i[1]][i[0]].change_color()


# Кнопка уменьшения скорости
def speed_minus():
    global speed
    if speed > 0:
        speed -= 1
        print(speed)
        speed_view.update_label(str(speed / 10)[:3])


# Кнопка увеличения скорости
def speed_plus():
    global speed
    if speed < 100:
        speed += 1
        speed_view.update_label(str(speed / 10)[:3])


# Кнопка Выход
def the_end():
    sys.exit()


# Перед запуском Проходит по всему полю и готовит массив repair
# записывая в него активные клетки и их соседей
def prestart():
    repair.clear()
    out.clear()
    for y in range(size_y):
        for x in range(size_x):
            if field[y][x].color < 6:
                repair.update(field[y][x].cast_neighbors())  # Добавляем соседей для проверки
                field[y][x].old_color = field[y][x].color
                repair.add(field[y][x])  # Добавляем клеточку для проверки
    switching()


# Вывод изменений из массива на поле и занесение клеточек в которых могут быть изменения
# в массив для проверки
def out_and_rerair():
    global counter_step, step
    auto_stop = True
    for cell in out:
        if cell.old_color != cell.color:
            cell.show_cell()
            repair.update(cell.neighbors)  # Добавляем соседей для проверки
            repair.add(cell)  # Добавляем клеточку для проверки
            auto_stop = False
    out.clear()
    if auto_stop or step:
        if run:
            click_pause()
            step = 0
    else:
        counter_step += 1
        count.update_label(str(counter_step))


# Обработка массива repair. Переключение ячеек в соответствии с правилами
# Удаление клеточек которые не переключаются
def switching():
    del_cell = set()  # Кандидаты на удаление
    global out
    for cell in repair:
        neighbors = Counter(cell.status_old())
        del neighbors[6]  # Удаляем количество пустых клеток вокруг исследуемой
        count_neighbors = sum(neighbors.values())  # Клеточек вокруг заполнено

        if count_neighbors == 3 and cell.old_color == 6:
            # Появление новой клеточки
            if max(neighbors.values()) == 1:
                # Клеточки все разных цветов, родитель случайный из них
                cell.color = random.choice(tuple(neighbors.keys()))
            else:
                # 2 или 3 клеточки одинаковые, родитель по большинству
                cell.color = max(neighbors, key=neighbors.get)
        else:
            if cell.color < 6 and (count_neighbors < 2 or count_neighbors > 3):
                # Удаление клеточки
                cell.color = 6
        if cell.old_color == cell.color:
            # Состояние клеточки не меняется, не обрабатываем ее
            del_cell.add(cell)
    repair.difference_update(del_cell)  # Удаляем из обработки клеточки не изменившиеся
    out = repair.copy()
    repair.clear()


# Инициализация
sc = pygame.display.set_mode()
clock = pygame.time.Clock()
pygame.font.init()
infoObject = pygame.display.Info()  # Информационный объект
# Разрешение экрана
w = infoObject.current_w
h = infoObject.current_h

# Для разрешения 1366х768
# При размере клетки 7 они занимают:
# по горизонтали при количестве 155: 1241 (125 остается на кнопки справа)
# по  вертикали при количестве 95: 762 (оставляем 6)
# Исходя из этого корректируем размер клеточки для данного разрешения
size_points = min((w - 125 - size_x - 1) // size_x, (w - 6 - size_y - 1) // size_y)

# Подготовка поля и массива его объектов
for y in range(size_y):
    string = []
    for x in range(size_x):
        string.append(Rectangle(sc, x, y))
    field.append(string)

# Запись в свойства каждой клеточки ее соседей
for y in range(size_y):
    for x in range(size_x):
        field[y][x].neighbors.add(field[y][x - 1])
        field[y][x].neighbors.add(field[y - 1][x - 1])
        field[y][x].neighbors.add(field[y - 1][x])
        field[y][x].neighbors.add(field[y - 1][(x + 1) % size_x])
        field[y][x].neighbors.add(field[y][(x + 1) % size_x])
        field[y][x].neighbors.add(field[(y + 1) % size_y][(x + 1) % size_x])
        field[y][x].neighbors.add(field[(y + 1) % size_y][x])
        field[y][x].neighbors.add(field[(y + 1) % size_y][x - 1])

# Кнопки и метки
start_stop_btn = Button(sc, w - 110, 40, 45, 25, 'Старт', click_pause)
step_btn = Button(sc, w - 55, 40, 25, 25, '+1', step_fun)
clear_btn = Button(sc, w - 110, 80, 70, 25, 'Очистить', click_clear)
open_file_btn = Button(sc, w - 110, 120, 70, 25, 'Открыть', open_file)
save_file_btn = Button(sc, w - 110, 160, 70, 25, 'Сохранить', save_file)
count = Label(sc, w - 110, 200, '0')
count_reset = Button(sc, w - 110, 240, 70, 25, 'Сброс', count_reset_fun)
position_btn = Button(sc, w - 110, 280, 70, 25, 'Позиции', position_fun)

speed_minus_btn = Button(sc, w - 110, 320, 20, 25, '<', speed_minus)
speed_view = Label(sc, w - 85, 314, '0')
speed_plus_btn = Button(sc, w - 40, 320, 20, 25, '>', speed_plus)

palette = Palette(sc, w - 112, 400)
count_point = Label(sc, w - 110, 540, '0')

exit_btn = Button(sc, w - 110, 732, 70, 25, 'Выход', the_end)


# обновляем окно
pygame.display.update()

while 1:
    start_time = time.time()
    if run:
        out_and_rerair()
        switching()

    do = True
    while do:
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
                    if x < size_x and y < size_y:
                        field[y][x].change_color()
                        field[y][x].show_cell()


                    # По клеткам не щелкали, проверяем не по кнопкам ли
                    elif not Button.isPress(event.pos):
                        # Не по кнопкам, проверяем палитру
                        palette.isPress(event.pos)


            elif event.type == userEvent:
                Button.button_press(0)

        do = start_time + speed / 10 > time.time()

        pygame.display.update()
