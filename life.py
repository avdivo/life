from tkinter import *
from tkinter.filedialog import *
import queue
import time

start_time1 = time.time()
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
    def __init__(self, canvas, x, y):
        self.x = x  # Горизонтальная координата сетки
        self.y = y  # Вертикальная координата сетки
        self.activ = False  # Закрашен ли квадрат (клетка активна)
        color = '#d9d9d9'
        global size_points
        coords = (x * (size_points + 1) + 1, y * (size_points + 1) + 1,
            x * (size_points + 1) + size_points, y * (size_points + 1) + size_points)
        self.canvas = canvas
        self.outline = color
        self.fill = color
        self.canvas_id = self.canvas.create_rectangle(
            coords, outline=self.outline, fill=self.fill)
        self.canvas.tag_bind(self.canvas_id, '<ButtonPress-1>', self.onRectClick)

# Щелчек по клеточке
    def onRectClick(self, event):
        self.change_color()

# Переключение клеточки
    def change_color(self):
        global counter_points
        self.activ = not self.activ
        color = 'red' if self.activ else '#d9d9d9'
        self.canvas.itemconfigure(self.canvas_id, fill=color, outline=color)
        counter_points += 1 if self.activ else -1
        count_point['text'] = counter_points

# Кнопка Пауза
def click_pause():
    global run
    if run:
        run = False
        pause['text'] = 'Старт'
        step_btn['state'] = NORMAL
    else:
        run = True
        pause['text'] = 'Стоп'
        step_btn['state'] = DISABLED

# Кнопка 1 шаг
def step_fun():
    global step
    step = 1
    click_pause()

# Кнопка Очистка
def click_clear():
    for y in range(size_y):
        for x in range(size_x):
            if field[y][x].activ:
                change.put(field[y][x])
    out()
    count_reset_fun()

# Кнопка Открыть
def open_file():
    name_file = askopenfilename(filetypes=[("Life файл", "*.life")])
    if name_file:
        with open(name_file, encoding='utf-8') as f:
            new = f.read().split(' ')
            del new[-1]
            click_clear()
            for i in range(0, len(new), 2):
                change.put(field[int(new[i+1])][int(new[i])])
        out()
        count_reset_fun()

# Кнопка Сохранить.
# Сохраняет координаты x, y через пробелы активных клеточек
def save_file():
    name_file = asksaveasfilename(filetypes=[("Life файл", "*.life")])
    if name_file:
        if name_file[len(name_file) - 5:] != '.life':
            name_file += '.life.'
        st = ''
        for y in range(size_y):
            for x in range(size_x):
                if field[y][x].activ:
                    st += str(field[y][x].x) + ' ' + str(field[y][x].y) + ' '
        with open(name_file, "w") as f:
            f.write(st)

# Кнопка Вывод из массива на поле
def out():
    start_time = time.time()
    global counter_step, step
    auto_stop = True
    while not change.empty():
        change.get().change_color()
        auto_stop = False
    if auto_stop or step:
        if run:
            click_pause()
            step = 0
    else:
        counter_step += 1
        count['text'] = counter_step
    print("--- %s seconds для OUT---" % (time.time() - start_time))


# Кнопка Кнопка сброс счетчика шагов
def count_reset_fun():
    global counter_step
    counter_step = 0
    count['text'] = counter_step

# Кнопка Рассановка/удаление позиционных точек
def position_fun():
    pos = ((size_x//4, size_y//4), (size_x//4*3, size_y//4), (size_x//2, size_y//2),
           (size_x//4, size_y//4*3), (size_x//4*3, size_y//4*3))
    for i in pos:
        field[i[1]][i[0]].change_color()


def onScale(s):
    global speed
    speed = s


# Интерфейс
root = Tk()
root.state('zoomed')
root.title("Жизнь")

# Размер экране
w = root.winfo_screenwidth()
h = root.winfo_screenheight()

# Для разрешения 1366х768
# При размере клетки 7 они занимают:
# по горизонтали при количестве 155: 1241 (125 остается на кнопки справа)
# по  вертикали при количестве 85: 681 (оставляем 87)
# Исходя из этого корректируем размер клеточки для данного разрешения
size_points = min((w-125-size_x-1)//size_x, (w-87-size_y-1)//size_y)

canv = Canvas(root)  # , width=500, height=681

# Кнопки
pause = Button(root, text='Старт', command=click_pause)
step_btn = Button(root, text='+1', command=step_fun)
clear = Button(root, text='Очистить', command=click_clear)
open_f = Button(root, text='Открыть', command=open_file)
save_f = Button(root, text='Сохранить', command=save_file)
count = Label(text="0", fg='#FF0000', font="Arial 20")
count_reset = Button(root, text='Сброс', command=count_reset_fun)
count_point = Label(text="0", fg='#FF0000', font="Arial 20")
position_btn = Button(root, text='Позиции', command=position_fun)
scale = Scale(root, from_=20, to=1, length=80, command=onScale)

pause.place(x=w-110, y=40)
step_btn.place(x=w-60, y=40)
clear.place(x=w-110, y=80)
open_f.place(x=w-110, y=120)
save_f.place(x=w-110, y=160)
count.place(x=w-110, y=200)
count_reset.place(x=w-110, y=240)
count_point.place(x=w-110, y=0)
position_btn.place(x=w-110, y=280)
scale.place(x=w-110, y=320)
scale.set(speed)

# Подготовка поля и массива его объектов
for y in range(size_y):
    string = []
    for x in range(size_x):
        string.append(Rectangle(canv, x, y))
    field.append(string)
canv.pack(side="left", fill="both", expand=True)


# Основной цикл
def main():


    # f = (time.time() - start_time1)
    # if f > 0.1:
    #     print("--- %s seconds TKINTER---" % (time.time() - start_time1))
    start_time = time.time()
    if run:
        for y in range(size_y):
            for x in range(size_x):
                neighbors = field[y][x - 1].activ
                neighbors += field[y - 1][x - 1].activ
                neighbors += field[y - 1][x].activ
                neighbors += field[y - 1][(x + 1) % size_x].activ
                neighbors += field[y][(x + 1) % size_x].activ
                neighbors += field[(y + 1) % size_y][(x + 1) % size_x].activ
                neighbors += field[(y + 1) % size_y][x].activ
                neighbors += field[(y + 1) % size_y][x - 1].activ

                life = False
                if neighbors == 2 and field[y][x].activ:
                    life = True
                if neighbors == 3:
                    life = True
                if field[y][x].activ != life:
                    # Клеточку необходимо переключить
                    change.put(field[y][x])  # Помещаем объект в очередь на переключение
        print("--- %s seconds ПОДГОТОВКА---" % (time.time() - start_time))
        out()
        canv.after(10, main)  # 2000-100*int(speed)
        # start_time1 = time.time()
        # canv.update_idletasks()
        # canv.update()
        # root.update_idletasks()
        # root.update()

# while True:
main()
print(' Я ТУТ ')
root.mainloop()