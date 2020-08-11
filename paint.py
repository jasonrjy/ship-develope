from tkinter import *
import time
import ship
import main

window = Tk()
window.title("Ship Detection Program")
window.resizable(0, 0)
canvas = Canvas(window, width=640, height=640, bg="white")
canvas.pack()

canvas_start_x = 50
canvas_start_y = 50
canvas_x = 300
canvas_y = 300


def converse_x(x):
    return 50 + x


def converse_y(y):
    return 350 - y


def update_paint(patrol, target):
    patrol_c = []
    target_c = []
    for i in range(len(patrol)):
        temp_x, temp_y = patrol[i].get_position()
        patrol_c.append(canvas.create_oval(temp_x - 5, temp_y - 5, temp_x + 5, temp_y + 5, fill='green'))
    for i in range(len(target)):
        temp_x, temp_y = target[i].get_position()
        target_c.append(canvas.create_oval(temp_x - 5, temp_y - 5, temp_x + 5, temp_y + 5, fill='red'))

    window.update()



#
# ship_1 = canvas.create_oval(45, 355, 55, 345, fill='green')
#
# for i in range(100):
#     canvas.move(ship_1, 3, 0)
#     window.update()
#     time.sleep(0.01)
#
window.mainloop()

