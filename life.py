from tkinter import *
from tkinter.filedialog import *

run = False
size = 45
field = []
counter_step = 0


class MyButton(Button):
    """ Create Button with some default values. """

    def __init__(self, *args):
        kwargs = dict(command=self.click, relief=GROOVE, activebackground='#FF0000', bd=1,
                      background='SystemButtonFace')  # Allow defaults to be overridden.
        super().__init__(*args, **kwargs)

    def click(self):
        if self['background'] == 'SystemButtonFace':
            self['background'] = '#FF0000'
        else:
            self['background'] = 'SystemButtonFace'

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
    else:
        run = True
        pause['text'] = 'Стоп'


def click_clear():
    for y in range(size):
        for x in range(size):
            field_shadow[y][x] = 0
    out()
    count_reset_fun()


def open_file():
    name_file = askopenfilename()
    if name_file[len(name_file) - 5:] == '.life':
        with open(name_file, encoding='utf-8') as f:
            new = f.read().split(' ')
            del new[0]
            if len(new[0]) != size:
                return
            for i in range(size):
                field_shadow[i] = list(map(int, list(new[i])))
            out()
            count_reset_fun()


def save_file():
    name_file = asksaveasfilename() + '.life'
    if name_file != '.life':
        st = ''
        for y in field:
            st += ' ' + ''.join(map(lambda x: str(int(x['background'] != 'SystemButtonFace')), y))
        with open(name_file, "w") as f:
            f.write(st)


def out():
    global counter_step
    auto_stop = True
    for y in range(size):
        for x in range(size):
            if field_shadow[y][x]:
                field[y][x]['background'] = '#FF0000'
                auto_stop = False
            else:
                field[y][x]['background'] = 'SystemButtonFace'
    if auto_stop:
        if run:
            click_pause()

    counter_step += 1
    count['text'] = counter_step


def count_reset_fun():
    global counter_step
    counter_step = 0
    count['text'] = counter_step


root = Tk()
root.title("Жизнь")

window_x = size * 12 + 120
window_y = size * 12 + 20

w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2  # середина экрана
h = h // 2
w = w - window_x // 2  # смещение от середины
h = h - window_y // 2
root.geometry('{}x{}+{}+{}'.format(window_x, window_y, w, h))

pause = Button(root, text='Старт', command=click_pause)
clear = Button(root, text='Очистить', command=click_clear)
open_f = Button(root, text='Открыть', command=open_file)
save_f = Button(root, text='Сохранить', command=save_file)
count = Label(text="0", fg='#FF0000', font="Arial 20")
count_reset = Button(root, text='Сброс', command=count_reset_fun)

pause.place(x=window_x - 90, y=50)
clear.place(x=window_x - 90, y=100)
open_f.place(x=window_x - 90, y=150)
save_f.place(x=window_x - 90, y=200)
count.place(x=window_x - 90, y=250)
count_reset.place(x=window_x - 90, y=300)

for y in range(size):
    string = []
    for x in range(size):
        b = MyButton(root)
        string.append(b)
        b.place(x=10 + x * 12, y=10 + y * 12, width=12, height=12)
    field.append(string)
field_shadow = [[0 for x in range(size)] for y in range(size)]

while True:
    if run:
        for y in range(size):
            for x in range(size):
                neighbors = field[y][x - 1]['background'] == '#FF0000'
                neighbors += field[y - 1][x - 1]['background'] == '#FF0000'
                neighbors += field[y - 1][x]['background'] == '#FF0000'
                neighbors += field[y - 1][(x + 1) % size]['background'] == '#FF0000'
                neighbors += field[y][(x + 1) % size]['background'] == '#FF0000'
                neighbors += field[(y + 1) % size][(x + 1) % size]['background'] == '#FF0000'
                neighbors += field[(y + 1) % size][x]['background'] == '#FF0000'
                neighbors += field[(y + 1) % size][x - 1]['background'] == '#FF0000'

                life = False
                if neighbors == 2 and field[y][x]['background'] == '#FF0000':
                    life = True
                if neighbors == 3:
                    life = True
                field_shadow[y][x] = life

        out()

    root.update()
