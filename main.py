import copy
import tkinter as tk
import tkinter.ttk
import time
import ship
import case
from PIL import Image, ImageTk, ImageDraw
import InfoTable
import sInfoTbl

# img = Image.new('RGB', (200, 200), (255, 255, 255))  ## Image에 대한 속성, 픽셀, 색깔 정해주기
# drw = ImageDraw.Draw(img, 'RGBA')
# drw.ellipse([(0, 0), (200, 200)], (255, 255, 255, 255), outline=(255, 255, 0), width=3)
# img.save("detection.png")
#
# image = Image.open("detection.png")
# resize_image = image.resize((100, 100))
# resize_image.save("detection.png")

window_w = 400
window_h = 300
ship_r = 5

global running
running = -1

window = tk.Tk()
window.title("Ship Detection Program")
window.geometry("800x500")
window.resizable(0, 0)

frame_info = tk.Frame(window)
frame_canvas = tk.Frame(window)
frame_btn = tk.Frame(window)

# frame_canvas.pack(side="left", fill="both")
# frame_info.pack(side="right", fill="both")
frame_canvas.grid(row=0, column=0)
frame_info.grid(row=0, column=1)
frame_btn.grid(row=1, column=1)

canvas = tk.Canvas(frame_canvas, width=window_w, height=window_h, bg="white")
canvas.pack()

f_tbl = tk.Frame(frame_info)
f_lbl = tk.Frame(frame_info)
f_chk = tk.Frame(frame_info)

f_lbl.grid(row=0)
f_chk.grid(row=1)
f_tbl.grid(row=2)


def RdiotoFixed():
    tCase.target = init_target
    for t in tCase.target:
        print("x = {}, y = {}, delay = {}".format(t.x, t.y, t.delay))


def RdiotoRandom():
    tCase.target = tCase.set_rand_target(tCase.total_time)
    for t in tCase.target:
        print("x = {}, y = {}, delay = {}".format(t.x, t.y, t.delay))

## Check
radioValue = tk.IntVar()
rdioLbl = tk.Label(f_chk, text="Select Target Type : ")
rdioF = tk.Radiobutton(f_chk, text="Fixed", variable=radioValue, value=1, command=RdiotoFixed)
rdioF.select()
rdioR = tk.Radiobutton(f_chk, text="Random", variable=radioValue, value=2, command=RdiotoRandom)

rdioLbl.grid(row=0, column=0)
rdioF.grid(row=0, column=1)
rdioR.grid(row=0, column=2)

# Label
head_lbl = tk.Label(f_lbl, text="Ship Info.")
head_lbl.grid(row=0)


images = []

ratio = 10
start_x = (window_w - 20 * ratio) / 2
start_y = window_h / 2 + (10 * ratio) / 2

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





def path_to_string(s):
    res = ""
    i = 0
    for i in range(len(s) - 1):
        res += str(s[i][0])
        res += ", "
        res += str(s[i][1])
        res += " > "
    res += str(s[i][0])
    res += ", "
    res += str(s[i][1])

    return res


def path_to_string_nl(s):
    res = ""
    i = 0
    for i in range(len(s)):
        res += str(s[i][0])
        res += ", "
        res += str(s[i][1])
        res += '\n'
    res = res[:-1]

    return res


def read_file_formatting(patrol, target):
    data = []

    for i in range(len(patrol)):
        data.append([])
        for j in range(len(target) + 7):
            data[i].append(0)

    for i in range(len(patrol)):
        data[i][0] = patrol[i].get_x()
        data[i][1] = patrol[i].get_y()
        # 현 탐지
        data[i][2] = 0
        # 총 탐지
        data[i][3] = 0
        # 경로
        data[i][-1] = path_to_string_nl(patrol[i].get_path())
        # 탐지 범위
        data[i][-2] = patrol[i].get_detection_dist()
        # Knot
        data[i][-3] = patrol[i].get_knot()
        # target detection time
        for j in range(len(target)):
            data[i][4 + j] = 0

    return data


def init_draw_patrol(patrol, target):
    for i in range(len(patrol)):
        temp_x, temp_y = patrol[i].get_position()
        temp_x, temp_y = converse(temp_x, temp_y)

        ## draw path
        for p in patrol:
            cur_path = p.get_path()
            num = len(cur_path)-1
            for j in range(num):
                x1 = converse_x(cur_path[j][0])
                y1 = converse_y(cur_path[j][1])
                x2 = converse_x(cur_path[j+1][0])
                y2 = converse_y(cur_path[j+1][1])
                canvas.create_line(x1, y1, x2, y2, dash=(2, 2), fill="green")
        ## draw patrol
        temp_c = canvas.create_oval(temp_x - ship_r, temp_y - ship_r, temp_x + ship_r, temp_y + ship_r, fill='green')
        c_patrol.append(temp_c)
        ## draw detection range
        temp_c = canvas.create_image(temp_x - (ratio * patrol[i].detection_dist), temp_y - (ratio * patrol[i].detection_dist), image=img, anchor=tk.NW)
        c_patrol_detection.append(temp_c)

    for i in range(len(patrol)):
        c_patrol_detection_l.append([])
        for j in range(len(target)):
            c_patrol_detection_l[i].append([])



def init_draw_target(target):
    for i in range(len(tCase.target)):
      temp_x, temp_y = tCase.target[i].get_position()
      temp_x, temp_y = converse(temp_x, temp_y)
      ## draw target
      temp_c = canvas.create_oval(temp_x - ship_r, temp_y - ship_r, temp_x + ship_r, temp_y + ship_r, fill='red')
      c_target.append(temp_c)


def update_draw_target():
    for i in range(len(tCase.target)):
        temp_x, temp_y = tCase.target[i].get_position()
        temp_x, temp_y = converse(temp_x, temp_y)
        canvas.coords(c_target[i], temp_x - ship_r, temp_y - ship_r, temp_x + ship_r, temp_y + ship_r)


def update_draw_patrol(res):
    for i in range(len(tCase.patrol)):
        temp_x, temp_y = tCase.patrol[i].get_position()
        temp_x, temp_y = converse(temp_x, temp_y)
        canvas.coords(c_patrol[i], temp_x - ship_r, temp_y - ship_r, temp_x + ship_r, temp_y + ship_r)
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
                c_patrol_detection_l[i][j] = canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, dash=(4, 2))
            else:
                canvas.delete(c_patrol_detection_l[i][j])


def run_canvas():
    for t in tCase.target:
        print("x = {}, y = {}, delay = {}".format(t.x, t.y, t.delay))

    global running
    running = 1

    for i in range(int(tCase.total_time)):
        if running == 1:
            ## update time with position and return detection res
            res = tCase.update_time()
            # get now patrol position to list
            patrol_all_p = tCase.get_all_position()
            # re-draw target
            update_draw_target()
            # re-draw patrol with detection range and detection line
            update_draw_patrol(res)
            # update x,y
            info_t.update_position(patrol_all_p)
            info_t.update_now_detection(res)
            info_t.update_res_detection(tCase)

            window.update()
            time.sleep(0.03)

def reset_info():
    global running
    running = -1
    idata = read_file_formatting(init_patrol, init_target)
    info_t = sInfoTbl.Table(f_tbl, idata, tCase)
    count = 0

    tCase.set_fixed_unit(init_patrol, init_target)

    for i in range(len(c_patrol)):
        temp_x, temp_y = init_patrol[i].get_position()
        temp_x, temp_y = converse(temp_x, temp_y)
        canvas.coords(c_patrol[i], temp_x - ship_r, temp_y - ship_r, temp_x + ship_r, temp_y + ship_r)
        canvas.coords(c_patrol_detection[i], temp_x - (ratio * 5), temp_y - (ratio * 5))
    for i in range(len(c_target)):
        temp_x, temp_y = init_target[i].get_position()
        temp_x, temp_y = converse(temp_x, temp_y)
        canvas.coords(c_patrol[i], temp_x - ship_r, temp_y - ship_r, temp_x + ship_r, temp_y + ship_r)
    for i in range(len(c_patrol_detection_l)):
        for j in range(len(c_patrol_detection_l[i])):
            canvas.delete(c_patrol_detection_l[i][j])

    init_draw_patrol(init_patrol, init_target)
    init_draw_target(init_target)


def toggleBtn():
    if(btn_run['text']=='Run'):
        btn_run['text']='Stop'
        run_canvas()

    elif(btn_run['text']=='Stop'):
        btn_run['text']='Run'
        global running
        running = 0

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

tCase = case.testCase()
tCase.total_time, count, tCase.patrol, tCase.target = case.readFile()
## init store
init_target = copy.deepcopy(tCase.target)
init_patrol = copy.deepcopy(tCase.patrol)
init_count = copy.deepcopy(count)
init_total_time = copy.deepcopy(tCase.total_time)

idata = read_file_formatting(tCase.patrol, tCase.target)
info_t = sInfoTbl.Table(f_tbl, idata, tCase)

tCase.set_fixed_unit(tCase.patrol, tCase.target)

init_draw_patrol(tCase.patrol, tCase.target)
init_draw_target(tCase.target)


btn_reset = tk.Button(frame_btn, text="Reset", overrelief="solid", width=15, command=reset_info)
btn_reset.grid(row=0, column=0, pady=10, padx=5)
btn_run = tk.Button(frame_btn, text="Run", overrelief="solid", width=15, command=toggleBtn)
btn_run.grid(row=0, column=1, pady=10, padx=5)


window.update()

########
# run_canvas()


#
window.mainloop()

