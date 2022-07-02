from tkinter import *
from tkinter.messagebox import *
from time import sleep
import threading
import numpy as np
import random

#define board size
ROWS = 20
COLS = 30

#default sleep time
pace = 0.1

#Create cells as a 2D list + temporary list for each iteration
cells = np.zeros((ROWS,COLS), dtype="int16")

temp_cells = np.zeros((ROWS,COLS), dtype="int16")

#main functions
def update_cells():
    global cells

    for row in range(ROWS):
        for col in range(COLS):
            if buttons[row][col]['bg'] == 'red':
                cells[row][col] = 1
            else:
                cells[row][col] = 0

def update_buttons():
    global cells
    global buttons

    for row in range(ROWS):
        for col in range(COLS):
            if cells[row][col] == 1:
                buttons[row][col]['bg'] = 'red'
            else:
                buttons[row][col]['bg'] = '#F0F0F0'

def get_neighbours(row,col):
    global cells
    global neighbours

    neighbours = 0

    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if i >= 0 and j >= 0 and i < ROWS and j < COLS:
                neighbours += int(cells[i][j])
    neighbours -= int(cells[row][col])
    return neighbours

def next_iteration():
    global cells
    global temp_cells

    temp_cells = np.zeros((ROWS,COLS), dtype="int16")

    update_cells()

    for row in range(ROWS):
        for col in range(COLS):
            get_neighbours(row,col)
            if cells[row][col] == 1:
                if neighbours < 2:
                    temp_cells[row][col] = 0
                elif neighbours > 3:
                    temp_cells[row][col] = 0
                else:
                    temp_cells[row][col] = 1
            else:
                if neighbours == 3:
                    temp_cells[row][col] = 1

    cells = temp_cells.copy()
    update_buttons()

def speed(spd):
    global pace
    pace = pace + spd
    if pace <= 0:
        pace += 0.05

def initialize():
    global pace
    global stop
    stop = 0
    while True:
        if stop != 1:
            sleep(pace)
            root.update()
            next_iteration()
            continue
        else:
            break

def run(x):
    global stop
    stop = x

def mark_cell(row,col):
    global cells
    if buttons[row][col]['bg'] == 'red':
        buttons[row][col]['bg'] = '#F0F0F0'
        cells[row][col] = 1
    else:
        buttons[row][col]['bg'] = 'red'
        cells[row][col] = 0

    #print(f"marked cell: {x}, {y}")

def clear_buttons():
    global buttons
    for row in range(ROWS):
        for col in range(COLS):
            buttons[row][col]['bg'] = '#F0F0F0'

def random_buttons():
    global cells
    cells = [[random.randint(0,2) for col in range(COLS)] for row in range(ROWS)]
    update_buttons()

def about():
    showinfo("About Game of Life", "A tribute by @donpipon\nOriginal by John Conway\nhttps://playgameoflife.com\n\nCode available at:\nhttps://github.com/donpipon/gameoflife ")

#Main window GUI
root = Tk()
root.title("Game of Life by @donpipon")

title = Label(text="Game of Life", font=('Arial', 20))
title.pack(side="top")

menubar = Menu(root)
root.config(menu=menubar)

fileMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Quit", command=quit)

helpMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpMenu)
helpMenu.add_command(label="About", command=about)


top_menu = Frame(root)
top_menu.pack(side="top")

clear_button = Button(top_menu, text="Clear", font=('Arial',14), command=clear_buttons)
clear_button.grid(row=0,column=0)

iteration_button = Button(top_menu, text="Next iteration", font=('Arial',14), command=next_iteration)
iteration_button.grid(row=0,column=1)

start_button = Button(top_menu, text="START", font=('Arial',14), command=initialize)
start_button.grid(row=0,column=2)

faster_button = Button(top_menu, text="Faster >", font=('Arial',14), command=lambda: speed(-0.05))
faster_button.grid(row=0,column=3)

slower_button = Button(top_menu, text="< Slower", font=('Arial',14), command=lambda: speed(0.05))
slower_button.grid(row=0,column=4)

stop_button = Button(top_menu, text="STOP", font=('Arial',14), command=lambda: run(1))
stop_button.grid(row=0,column=5)

random_button = Button(top_menu, text="Random", font=('Arial',14), command=random_buttons)
random_button.grid(row=0,column=6)

frame = Frame(root)
frame.pack()
#Create 2D list of buttons

buttons = [[0 for col in range(COLS)] for row in range(ROWS)]

#create grid of buttons representing each cell
for row in range(ROWS):
    for col in range(COLS):
        buttons[row][col] = Button(frame, text="", width=2, height=1, command=lambda row=row, col=col: mark_cell(row,col))
        buttons[row][col].grid(row=row, column=col)

bottom_menu = Frame(root)
bottom_menu.pack()

speed_label = Label(bottom_menu, text="Speed: ", font=('Arial',14))
#speed_label.grid(row=0, column=0)

speed_dial = Scale(bottom_menu, length=(COLS*10), from_=1000, to=1, orient=HORIZONTAL, showvalue=0)
speed_dial.set(((speed_dial['from']-speed_dial['to'])/2)+speed_dial['to'])
#speed_dial.grid(row=0, column=1)

window = threading.Thread(target=root.mainloop(), daemon=True)
game = threading.Thread(target=initialize(), daemon=True)

if __name__ == '__main__':
    window.start()
    game.start()


