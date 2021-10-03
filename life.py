from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox as mb

run = False
size_x = 80
size_y = 40
field = []
counter_step = 0
step = 0
counter_points = 0

class MyButton(Button):
    """ Create Button with some default values. """

    def __init__(self, *args):
        kwargs = dict(command=self.click, relief=GROOVE, activebackground='#FF0000', bd=1,
                      background='SystemButtonFace')  # Allow defaults to be overridden.
        super().__init__(*args, **kwargs)

    def click(self):
        global counter_points
        if self['background'] == 'SystemButtonFace':
            self['background'] = '#FF0000'
            counter_points += 1
        else:
            self['background'] = 'SystemButtonFace'
            counter_points -= 1
        count_point['text'] = counter_points


    def auto(self):
        if self['background'] == 'SystemButtonFace':
            self['background'] = '#FF0000'
        else:
            self['background'] = 'SystemButtonFace'


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


def step_fun():
    global step
    step = 1
    click_pause()


def click_clear():
    for y in range(size_y):
        for x in range(size_x):
            field_shadow[y][x] = 0
    out()
    count_reset_fun()


def open_file():
    name_file = askopenfilename(filetypes=[("Life файл", "*.life")])
    if name_file:
        with open(name_file, encoding='utf-8') as f:
            new = f.read().split(' ')
            del new[0]
            if len(new[0]) != size_x or len(new) != size_y:
                mb.showerror("Ошибка", "Не соответствует размер окна")
                return
            for i in range(size_y):
                field_shadow[i] = list(map(int, list(new[i])))
            out()
            count_reset_fun()


def save_file():
    name_file = asksaveasfilename(filetypes=[("Life файл", "*.life")])
    if name_file:
        if name_file[len(name_file) - 5:] != '.life':
            name_file += ' ({}x{}).life.'.format(size_x, size_y)
        st = ''
        for y in field:
            st += ' ' + ''.join(map(lambda x: str(int(x['background'] != 'SystemButtonFace')), y))
        with open(name_file, "w") as f:
            f.write(st)


def out():
    global counter_step, step, counter_points
    auto_stop = True
    counter_points = 0
    for y in range(size_y):
        for x in range(size_x):
            if field_shadow[y][x]:
                field[y][x]['background'] = '#FF0000'
                counter_points += 1
                auto_stop = False
            else:
                field[y][x]['background'] = 'SystemButtonFace'
    if auto_stop or step:
        if run:
            click_pause()
            step = 0

    counter_step += 1
    count['text'] = counter_step
    count_point['text'] = counter_points

def count_reset_fun():
    global counter_step
    counter_step = 0
    count['text'] = counter_step


root = Tk()
root.title("Жизнь")

window_x = size_x * 12 + 120
window_y = size_y * 12 + 20

w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2  # середина экрана
h = h // 2
w = w - window_x // 2  # смещение от середины
h = h - window_y // 2
root.geometry('{}x{}+{}+{}'.format(window_x, window_y, w, h))

pause = Button(root, text='Старт', command=click_pause)
step_btn = Button(root, text='+1', command=step_fun)
clear = Button(root, text='Очистить', command=click_clear)
open_f = Button(root, text='Открыть', command=open_file)
save_f = Button(root, text='Сохранить', command=save_file)
count = Label(text="0", fg='#FF0000', font="Arial 20")
count_reset = Button(root, text='Сброс', command=count_reset_fun)
count_point = Label(text="0", fg='#FF0000', font="Arial 20")

pause.place(x=window_x - 90, y=40)
step_btn.place(x=window_x - 40, y=40)
clear.place(x=window_x - 90, y=80)
open_f.place(x=window_x - 90, y=120)
save_f.place(x=window_x - 90, y=160)
count.place(x=window_x - 90, y=200)
count_reset.place(x=window_x - 90, y=240)
count_point.place(x=window_x - 90, y=0)

for y in range(size_y):
    string = []
    for x in range(size_x):
        b = MyButton(root)
        string.append(b)
        b.place(x=10 + x * 12, y=10 + y * 12, width=12, height=12)
    field.append(string)
field_shadow = [[0 for x in range(size_x)] for y in range(size_y)]

while True:
    if run:
        for y in range(size_y):
            for x in range(size_x):
                neighbors = field[y][x - 1]['background'] == '#FF0000'
                neighbors += field[y - 1][x - 1]['background'] == '#FF0000'
                neighbors += field[y - 1][x]['background'] == '#FF0000'
                neighbors += field[y - 1][(x + 1) % size_x]['background'] == '#FF0000'
                neighbors += field[y][(x + 1) % size_x]['background'] == '#FF0000'
                neighbors += field[(y + 1) % size_y][(x + 1) % size_x]['background'] == '#FF0000'
                neighbors += field[(y + 1) % size_y][x]['background'] == '#FF0000'
                neighbors += field[(y + 1) % size_y][x - 1]['background'] == '#FF0000'

                life = False
                if neighbors == 2 and field[y][x]['background'] == '#FF0000':
                    life = True
                if neighbors == 3:
                    life = True
                field_shadow[y][x] = life

        out()

    root.update()
