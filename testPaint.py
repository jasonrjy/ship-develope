from tkinter import *
import time
import ship
import case
from PIL import Image, ImageTk, ImageDraw

window = Tk()
window.title("Ship Detection Program")
window.resizable(0, 0)
canvas = Canvas(window, width=600, height=600, bg="white")
canvas.pack()

images = []

start_x = 100
start_y = 250

# img = Image.new('RGB', (200, 200), (255, 255, 255))  ## Image에 대한 속성, 픽셀, 색깔 정해주기
# drw = ImageDraw.Draw(img, 'RGBA')
# drw.ellipse([(0, 0), (200, 200)], (255, 255, 255, 255), outline=(255, 255, 0), width=50)
# img.save("detection.png")

def converse_x(x):
    return start_x + (x*20)


def converse_y(y):
    return start_y - (y*20)


def converse(x, y):
    return start_x + (x * 20), start_y - (y*20)


def create_detection_range(x, y):
    img = ImageTk.PhotoImage(Image.open('detection.png'))
    return canvas.create_image(200, 200, image=img, anchor=NW)

tCase = case.testCase()
tCase.total_time, count, tCase.patrol, tCase.target = case.readFile()

c_patrol = []
c_patrol_detection = []
c_target = []

# temp_c = create_detection_range(200, 200)
# c_patrol_detection.append(temp_c)
img = ImageTk.PhotoImage(Image.open('detection.png'))
canvas.create_image(200, 200, image=img, anchor=NW)

window.update()

window.mainloop()

