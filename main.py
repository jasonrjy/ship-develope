from tkinter import *
import time
import ship
import case
from PIL import Image, ImageTk, ImageDraw

# img = Image.new('RGB', (200, 200), (255, 255, 255))  ## Image에 대한 속성, 픽셀, 색깔 정해주기
# drw = ImageDraw.Draw(img, 'RGBA')
# drw.ellipse([(0, 0), (200, 200)], (255, 255, 255, 255), outline=(255, 255, 0), width=3)
# img.save("detection.png")
#
# image = Image.open("detection.png")
# resize_image = image.resize((100, 100))
# resize_image.save("detection.png")

w = 400
h = 300
r = 5

window = Tk()
window.title("Ship Detection Program")
window.resizable(0, 0)
canvas = Canvas(window, width= w, height= h, bg="white")
canvas.pack()

images = []

ratio = 10
start_x = (w - 20 * ratio)/2
start_y = h / 2 + (10 * ratio)/2

tCase = case.testCase()
tCase.total_time, count, tCase.patrol, tCase.target = case.readFile()
tCase.set_fixed_unit(tCase.patrol, tCase.target)

c_patrol = []
c_patrol_detection = []
c_patrol_detection_l = []
c_target = []
img = ImageTk.PhotoImage(Image.open('detection.png'))


def converse_x(x):
    return start_x + (x*10)


def converse_y(y):
    return start_y - (y*10)


def converse(x, y):
    return start_x + (x * 10), start_y - (y * 10)


def init_draw_patrol(patrol):
    for i in range(len(tCase.patrol)):
        temp_x, temp_y = tCase.patrol[i].get_position()
        temp_x, temp_y = converse(temp_x, temp_y)
        ## draw patrol
        temp_c = canvas.create_oval(temp_x - r, temp_y - r, temp_x + r, temp_y + r, fill='green')
        c_patrol.append(temp_c)
        ## draw detection range
        temp_c = canvas.create_image(temp_x - (ratio * tCase.patrol[i].detection_dist), temp_y - (ratio * tCase.patrol[i].detection_dist), image=img, anchor=NW)
        c_patrol_detection.append(temp_c)

    for i in range(len(tCase.patrol)):
        c_patrol_detection_l.append([])
        for j in range(len(tCase.target)):
            c_patrol_detection_l[i].append([])



def init_draw_target(target):
    for i in range(len(tCase.target)):
      temp_x, temp_y = tCase.target[i].get_position()
      temp_x, temp_y = converse(temp_x, temp_y)
      ## draw target
      temp_c = canvas.create_oval(temp_x - r, temp_y - r, temp_x + r, temp_y + r, fill='red')
      c_target.append(temp_c)


def update_draw_target():
    for i in range(len(tCase.target)):
        temp_x, temp_y = tCase.target[i].get_position()
        temp_x, temp_y = converse(temp_x, temp_y)
        canvas.coords(c_target[i], temp_x - r, temp_y - r, temp_x + r, temp_y + r)


def update_draw_patrol(res):
    for i in range(len(tCase.patrol)):
        temp_x, temp_y = tCase.patrol[i].get_position()
        temp_x, temp_y = converse(temp_x, temp_y)
        canvas.coords(c_patrol[i], temp_x - r, temp_y - r, temp_x + r, temp_y + r)
        canvas.coords(c_patrol_detection[i], temp_x-(ratio * 5), temp_y - (ratio * 5))

    ### draw detection line
    for i in range(len(tCase.patrol)):
        for j in range(len(tCase.target)):
            if res[i][j] != -1:
                print("i : {}, j : {} >> {} ".format(i, j, res[i][j]))
                x1, y1 = tCase.patrol[i].get_position()
                x1, y1 = converse(x1, y1)
                x2, y2 = tCase.target[j].get_position()
                x2, y2 = converse(x2, y2)

                canvas.delete(c_patrol_detection_l[i][j])
                c_patrol_detection_l[i][j] = canvas.create_line(x1, y1, x2, y2, arrow=LAST, dash=(4, 2))
            else:
                canvas.delete(c_patrol_detection_l[i][j])


def run_canvas():
    for i in range(int(tCase.total_time)):
        ## update time with position and return detection res
        res = tCase.update_time()
        # re-draw target
        update_draw_target()
        # re-draw patrol with detection range and detection line
        update_draw_patrol(res)
        window.update()
        time.sleep(0.03)

#
# def create_oval(x1, y1, x2, y2, **kwargs):
#     if 'alpha' in kwargs:
#         alpha = int(kwargs.pop('alpha') * 255)
#         fill = kwargs.pop('fill')
#         fill = window.winfo_rgb(fill) + (alpha,)
#         image = save_img(x1,y1,x2,y2,fill)
#         images.append(ImageTk.PhotoImage(image))
#         canvas.create_image(x1, y1, image=images[-1], anchor='nw')
#
#     oval = canvas.create_oval(x1, y1, x2, y2, **kwargs)
#     return oval
#
# def save_img(x1, y1, x2, y2, fill):
#     image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)  ## Image에 대한 속성, 픽셀, 색깔 정해주기
#     drw = ImageDraw.Draw(image)  ## image 값으로 드로우하기
#     drw.ellipse([(x1, y1), (x2, y2)], fill, outline="yellow")
#     # drw.ellipse([(x1, y1), (x2, y2)], fill, outline=None)
#     return image
#
#
# def t_create_oval(x1, y1, x2, y2, **kwargs):
#     if "alpha" in kwargs:
#         if "fill" in kwargs:
#             # Get and process the input data
#             fill = window.winfo_rgb(kwargs.pop("fill"))\
#                    + (int(kwargs.pop("alpha") * 255),)
#             outline = kwargs.pop("outline") if "outline" in kwargs else None
#             # We need to find a rectangle the polygon is inscribed in
#             # (max(args[::2]), max(args[1::2])) are x and y of the bottom right point of this rectangle
#             # and they also are the width and height of it respectively (the image will be inserted into
#             # (0, 0) coords for simplicity)
#             image = Image.new("RGBA", (x2 - x1, y2 - y1), fill)
#             ImageDraw.Draw(image).ellipse([(x1, y1), (x2, y2)], fill=fill, outline=outline)
#             images.append(ImageTk.PhotoImage(image))  # prevent the Image from being garbage-collected
#             return canvas.create_image(0, 0, image=images[-1], anchor="nw")  # insert the Image to the 0, 0 coords
#         raise ValueError("fill color must be specified!")
#     return canvas.create_oval(x1, y1, x2, y2, **kwargs)

######## init setting section

init_draw_patrol(tCase.patrol)
init_draw_target(tCase.target)
window.update()

########
run_canvas()


#
window.mainloop()

