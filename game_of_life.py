from tkinter import *
from time import sleep

#define board size
ROWS = COLS = 25

#Create cells as a 2D list
cells = []
for row in range(ROWS):
    columns = []
    cells.append(columns)
    for col in range(COLS):
        columns.append(0)

#Create temporary list for each iteration
temp_cells = []
for row in range(ROWS):
    temp_columns = []
    temp_cells.append(temp_columns)
    for col in range(COLS):
        temp_columns.append(0)



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
            if i >= 0 and j >= 0 and i < ROWS and j < ROWS:
                neighbours += int(cells[i][j])
    neighbours -= int(cells[row][col])
    return neighbours

def next_iteration():
    global cells
    global temp_cells

    temp_cells.clear()
    for row in range(ROWS):
        temp_columns = []
        temp_cells.append(temp_columns)
        for col in range(COLS):
            temp_columns.append(0)

    update_cells()

    #neighbours_list = []
    for row in range(ROWS):
        for col in range(COLS):
            get_neighbours(row,col)
            #neighbours_list.append(neighbours)
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
    #print(cells)
    #print(neighbours_list)
    #print(temp_cells)
    cells = temp_cells.copy()
    update_buttons()

def initialize():
    global stop
    stop = 0
    while True:
        if stop != 1:
            sleep(0.2)
            root.update()
            next_iteration()
            continue
        else:
            break

def stop():
    global  stop
    stop = 1

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

root = Tk()
root.title("Game of Life")

title = Label(text="Game of Life", font=('Arial', 20))
title.pack(side="top")

top_menu = Frame(root)
top_menu.pack(side="top")

clear_button = Button(top_menu, text="clear", font=('Arial',14), command=clear_buttons)
clear_button.grid(row=0,column=0)

iteration_button = Button(top_menu, text="next iteration", font=('Arial',14), command=next_iteration)
iteration_button.grid(row=0,column=1)

start_button = Button(top_menu, text="start!", font=('Arial',14), command=initialize)
start_button.grid(row=0,column=2)

stop_button = Button(top_menu, text="stop", font=('Arial',14), command=stop)
stop_button.grid(row=0,column=3)

frame = Frame(root)
frame.pack()
#Create 2D list of buttons
buttons = []
for row in range(ROWS):
    columns = []
    buttons.append(columns)
    for col in range(COLS):
        columns.append(0)
#create grid of buttons representing each cell
for row in range(ROWS):
    for col in range(COLS):
        buttons[row][col] = Button(frame, text="", width=2, height=1, command=lambda row=row, col=col: mark_cell(row,col))
        buttons[row][col].grid(row=row, column=col)

root.mainloop()


