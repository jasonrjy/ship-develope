import copy
import tkinter as tk
import tkinter.ttk
import tkinter.simpledialog
from tkinter.messagebox import askquestion, showinfo
import time
import case
from PIL import Image, ImageTk, ImageDraw
import sInfoTbl
import GUI
import type
import re
import cv2
import math

# img = Image.new('RGB', (200, 200), (255, 255, 255))  ## Image에 대한 속성, 픽셀, 색깔 정해주기
# drw = ImageDraw.Draw(img, 'RGBA')
# drw.ellipse([(0, 0), (200, 200)], (255, 255, 255, 255), outline=(255, 255, 0), width=3)
# img.save("detection.png")
#
# image = Image.open("detection.png")
# resize_image = image.resize((100, 100))
# resize_image.save("detection.png")

## -1 == 첫 시작, 0 = stop, 1 = run, 2 = end
global running, store_time, pg_value
running = -1
store_time = 0
pg_value = 0

operation_x = 20
operation_y = 10
oper_margin = 5

window = tk.Tk()
window.title("Ship Detection Program")
window.geometry("900x500")
window.resizable(0, 0)

frame_info = tk.Frame(window)
frame_bbs = tk.Frame(window, padx=10, pady=10)
frame_opt = tk.Frame(frame_bbs)
frame_btn = tk.Frame(window)
frame_pgb = tk.Frame(window)

# frame_canvas.pack(side="left", fill="both")
# frame_info.pack(side="right", fill="both")
frame_bbs.grid(row=0, column=0)
frame_info.grid(row=0, column=1)
frame_pgb.grid(row=1,column=0)
frame_btn.grid(row=1, column=1)
frame_opt.pack(anchor=tk.E)

f_tbl = tk.Frame(frame_info)
f_lbl = tk.Frame(frame_info)
f_chk = tk.Frame(frame_info)

f_lbl.grid(row=0)
f_chk.grid(row=1)
f_tbl.grid(row=2)


# def RdiotoFixed():
#     tCase.target = copy.deepcopy(init_target)
#     for t in tCase.target:
#         print("x = {}, y = {}, delay = {}".format(t.x, t.y, t.delay))
#
#
# def RdiotoRandom():
#     tCase.target = tCase.set_rand_target(tCase.total_time)
#     for t in tCase.target:
#         print("x = {}, y = {}, delay = {}".format(t.x, t.y, t.delay))
#
#
# def bbsSelectG():
#     ## Check F or R
#     targetType = tk.IntVar()
#     rdioLbl = tk.Label(f_chk, text="Select Target Type : ")
#     rdioF = tk.Radiobutton(f_chk, text="Fixed", variable=targetType, value=1, command=RdiotoFixed)
#     rdioF.select()
#     rdioR = tk.Radiobutton(f_chk, text="Random", variable=targetType, value=2, command=RdiotoRandom)
#
#     # rdioLbl.grid(row=1, column=0)
#     # rdioF.grid(row=1, column=1)
#     # rdioR.grid(row=1, column=2)
#
# def bbsSelectR():
#     rdioLbl.grid_forget()
#     rdioF.grid_forget()
#     rdioR.grid_forget()
#
# ## Check Graphic or Exe result
# bbsType = tk.IntVar()
# bbsLbl = tk.Label(f_chk, text="프로그램 유형 선택 : ")
# bbsGraphic = tk.Radiobutton(f_chk, text="그래픽", variable=bbsType, value=1, command=bbsSelectG)
# bbsGraphic.select()
# bbsGraphic.invoke()
# bbsResult = tk.Radiobutton(f_chk, text="실행 결과", variable=bbsType, value=2, command=bbsSelectR)
#
# # bbsLbl.grid(row=0, column=0)
# # bbsGraphic.grid(row=0, column=1)
# # bbsResult.grid(row=0, column=2)
#
# targetType = None
# rdioLbl = None
# rdioF = None
# rdioR = None


# Label
head_lbl = tk.Label(f_lbl, text="Ship Info.")
head_lbl.grid(row=0)


images = []


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

def run_canvas():
    if typeChk.targetType == 2:
        tCase.target = tCase.set_rand_target(tCase.total_time)
    for t in tCase.target:
        print("x = {}, y = {}, delay = {}".format(t.x, t.y, t.delay))

    global running, store_time
    running = 1

    while store_time < int(tCase.total_time):
        store_time += tCase.time
        if running == 1:
            ## update time with position and return detection res
            res, path_changed = tCase.update_time(info_t.patrol_btn_tg, info_t.target_btn_tg)
            cvs.patrol_changed_path(path_changed)

            # get now patrol position to list
            patrol_all_p = tCase.get_all_position()
            # re-draw target
            cvs.update_draw_target(info_t.target_btn_tg)
            for i in range(len(tCase.target)):
                cvs.set_target_img(i)
            # re-draw patrol with detection range and detection line
            cvs.update_draw_patrol(res, info_t.patrol_btn_tg, info_t.target_btn_tg)
            # update x,y
            info_t.update_position(patrol_all_p)
            info_t.update_now_detection(res)
            info_t.update_res_detection(tCase)

            # print(info_t.tbl[8][1]['disabledbackground'])
            # info_t.tbl[8][1].configure(disabledbackground="#666666")
            # print(info_t.tbl[8][1]['disabledbackground'])
            window.update()
            # print(info_t.tbl[8][1]['background'])
            time.sleep(0.03)
        else:
            return i
            # print("waiting start")
            # # waiting.wait(lambda: run_ready(), timeout_seconds=120, waiting_for="something to be ready")
            # print("waiting end")

    ## stop이 아니면 > 루프가 끝났다면
    if running != 0:
        btn_run['state'] = tk.DISABLED


def run_result():
    global running, store_time
    running = 1
    tt = 300
    cnt = int(typeChk.countVal.get())

    resText.text.config(state=tk.NORMAL)
    # progress_bar.start(10)
    progress_bar.pack()
    progress_bar["value"] = 0
    progress_bar["maximum"] = cnt
    print(progress_bar["maximum"])

    case.cal_case_write_text(tt, cnt, tCase.patrol, tCase.target, resText, info_t.patrol_btn_tg,
                             info_t.target_btn_tg, progress_update, operation_x, operation_y)
    resText.text.config(state=tk.DISABLED)
    progress_bar.pack_forget()


def reset_info():
    global running, store_time
    running = -1
    store_time = 0

    btn_run['state'] = tk.NORMAL
    typeChk.rdioR['state'] = tk.NORMAL
    typeChk.rdioF['state'] = tk.NORMAL
    typeChk.bbsGraphic['state'] = tk.NORMAL
    typeChk.bbsResult['state'] = tk.NORMAL
    for i in info_t.path_entry:
        i['state'] = tk.NORMAL
    for i in range(len(tCase.patrol)):
        info_t.drange_entry[i]['state'] = tk.NORMAL
        info_t.knot_entry[i]['state'] = tk.NORMAL
        info_t.path_list[i]['state'] = tk.NORMAL
        info_t.path_entry[i]['state'] = tk.NORMAL
        info_t.patrol_btn[i]['state'] = tk.NORMAL
        info_t.target_btn[i]['state'] = tk.NORMAL
    if btn_run['text'] == 'Stop':
        btn_run['text'] = 'Run'

    tCase.patrol = copy.deepcopy(init_patrol)
    for i in range(len(tCase.total_accum_t)):
        tCase.total_accum_t[i] = 0
    for i in range(len(tCase.accum_time)):
        for j in range(len(tCase.accum_time[i])):
            tCase.accum_time[i][j] = 0

    if typeChk.targetType.get() == 2:
        typeChk.RdiotoRandom()
    else:
        tCase.target = copy.deepcopy(init_target)
    idata = read_file_formatting(tCase.patrol, tCase.target)
    tCase.accum_t = 0
    info_t.reset()
    count = 0

    tCase.set_fixed_unit(tCase.patrol, tCase.target)

    for i in range(len(cvs.c_patrol)):
        temp_x, temp_y = tCase.patrol[i].get_position()
        temp_x, temp_y = cvs.converse(temp_x, temp_y)
        # print("c_patorl {} = {}".format(i, canvas.coords(c_patrol[i])))

        cvs.canvas.coords(cvs.c_patrol[i], temp_x - cvs.patrol_r, temp_y - cvs.patrol_r)
        # print("c_patorl {} = {}".format(i, canvas.coords(c_patrol[i])))
        ## init size c_patrol_detection
        cvs.set_detection_range_img(tCase.patrol)
        cvs.canvas.coords(cvs.c_patrol_detection[i], temp_x - (cvs.ratio * 5), temp_y - (cvs.ratio * 5))
        cvs.set_patrol_img(i)
    for i in range(len(cvs.c_target)):
        temp_x, temp_y = tCase.target[i].get_position()
        temp_x, temp_y = cvs.converse(temp_x, temp_y)
        cvs.canvas.coords(cvs.c_target[i], temp_x - cvs.target_r, temp_y - cvs.target_r)
    for i in range(len(cvs.c_patrol_detection_l)):
        for j in range(len(cvs.c_patrol_detection_l[i])):
            cvs.canvas.delete(cvs.c_patrol_detection_l[i][j])

    ## update for path
    cvs.update_init_draw_patrol()
    info_t.refresh_all_path()

    for i in range(len(tCase.patrol)):
        info_t.data_t[8][i].set(tCase.patrol[i].detection_dist)
        info_t.data_t[7][i].set(tCase.patrol[i].knot)

    ## reset patrol tg
    btn_tg = info_t.patrol_btn_tg
    for i in range(len(btn_tg)):
        btn_tg[i] = False
        heading_patrol_toggle(i)

    ## reset target tgg
    btn_tg = info_t.target_btn_tg
    for i in range(len(btn_tg)):
        btn_tg[i] = False
        property_target_toggle(i)


def toggleBtn():
    global running

    if(btn_run['text']=='Run'):
        typeChk.rdioF['state'] = tk.DISABLED
        typeChk.rdioR['state'] = tk.DISABLED
        typeChk.bbsGraphic['state'] = tk.DISABLED
        typeChk.bbsResult['state'] = tk.DISABLED
        for i in info_t.path_entry:
            i['state'] = tk.DISABLED
        for i in range(len(tCase.patrol)):
            info_t.drange_entry[i]['state'] = tk.DISABLED
            info_t.knot_entry[i]['state'] = tk.DISABLED
            info_t.path_list[i]['state'] = tk.DISABLED
            info_t.path_entry[i]['state'] = tk.DISABLED
            info_t.patrol_btn[i]['state'] = tk.DISABLED
            info_t.target_btn[i]['state'] = tk.DISABLED

        btn_run['text'] = 'Stop'
        running = 1

        ## get setting val
        tCase.set_info_data(info_t)
        cvs.set_detection_range_img(tCase.patrol)
        if typeChk.bbsType.get() == 1:
            run_canvas()
        else:
            run_result()

    elif(btn_run['text']=='Stop'):
        btn_run['text']='Run'
        running = 0


def run_ready():
    global running
    if running == 1:
        return True
    return False

def delete_path(event, idx):
    global running
    if running == -1:
        origin = info_t.path_list[idx]

        ## selection = list_box에서 선택된 것들의 리스트 // 단일선택만 되니 [0]만 존재
        selection = origin.curselection()
        # sel_val = origin.get(selection)
        # sel_val = re.split(', ', sel_val)
        # print(sel_val)
        # print(selection[0])
        if selection:
            if tCase.patrol[idx].delete_path(selection[0]):
                print(selection[0])
                if selection[0] in [0, origin.size()-1]:
                    origin.delete(origin.size()-1)
                    origin.delete(0)
                    origin.insert("end", origin.get(0))
                else:
                    origin.delete(selection)
                cvs.update_init_draw_patrol()


def insert_path(event, idx):
    global running
    if running == -1:
        origin = info_t.path_entry[idx].get()
        input_index = info_t.path_list[idx].size() - 1
        if origin.find(": ") != -1:
            temp = re.split(': ', origin)
            input_index = int(temp[0])
            origin = temp[1]
        input = re.split(', ', origin)
        if len(input) == 2:
            if str.isdigit(input[0]) and str.isdigit(input[1]):
                tCase.patrol[idx].add_path_index(input_index, int(input[0]), int(input[1]))
                info_t.path_list[idx].insert(input_index, origin)
                info_t.path_entry[idx].delete(0, 'end')
        cvs.update_init_draw_patrol()


def edit_path(event, idx):
    global running
    if running == -1:
        origin = info_t.path_list[idx]
        selection = origin.curselection()

        res = tk.simpledialog.askstring("Patrol Path", "경로를 입력해주십시오.")
        if is_path_format(res):
            if selection[0] in [0, origin.size()-1]:
                origin.delete(0)
                origin.insert(0, res)
                origin.delete(origin.size()-1)
                origin.insert(origin.size(), res)

                tCase.patrol[idx].update_path(0, res)
                tCase.patrol[idx].update_path(origin.size()-1, res)
            else:
                origin.delete(selection[0])
                origin.insert(selection[0], res)
                tCase.patrol[idx].update_path(selection[0], res)

            showinfo('경로를 수정합니다', res)
            cvs.update_init_draw_patrol()
        else:
            show_canceled()

def show_canceled():
    showinfo('Canceled', 'You canceled')

def is_path_format(path_str):
    input = re.split(', ', path_str)
    if len(input) == 2:
        if str.isdigit(input[0]) and str.isdigit(input[1]):
            return True
    return False


def set_heading_func():
    for i in range(len(info_t.patrol_btn)):
        info_t.patrol_btn[i].config(command=lambda idx=i: heading_patrol_toggle(idx))


def set_property_func():
    for i in range(len(info_t.target_btn)):
        info_t.target_btn[i].config(command=lambda idx=i: property_target_toggle(idx))


def heading_patrol_toggle(idx):
    ## false
    if info_t.patrol_btn_tg[idx]:
        info_t.patrol_btn[idx]['background'] = "#808080"
        info_t.patrol_btn[idx]['fg'] = "#a0a0a0"
        for i in range(len(cvs.c_patrol_path[idx])):
            cvs.canvas.itemconfigure(cvs.c_patrol_path[idx][i], state=tk.HIDDEN)
        cvs.canvas.itemconfigure(cvs.c_patrol[idx], state=tk.HIDDEN)
        cvs.canvas.itemconfigure(cvs.c_patrol_detection[idx], state=tk.HIDDEN)
        info_t.patrol_off(idx)
    else:
        info_t.patrol_btn[idx]['background'] = "white"
        info_t.patrol_btn[idx]['fg'] = "blue"
        for i in range(len(cvs.c_patrol_path[idx])):
            cvs.canvas.itemconfigure(cvs.c_patrol_path[idx][i], state=tk.NORMAL)
        cvs.canvas.itemconfigure(cvs.c_patrol[idx], state=tk.NORMAL)
        cvs.canvas.itemconfigure(cvs.c_patrol_detection[idx], state=tk.NORMAL)
        info_t.patrol_on(idx)

    info_t.patrol_btn_tg[idx] = not info_t.patrol_btn_tg[idx]

def property_target_toggle(idx):
    ## false
    if info_t.target_btn_tg[idx]:
        info_t.target_btn[idx]['background'] = "#808080"
        info_t.target_btn[idx]['fg'] = "#a0a0a0"
        info_t.target_off(idx)
        cvs.canvas.itemconfigure(cvs.c_target[idx], state=tk.HIDDEN)
    else:
        info_t.target_btn[idx]['background'] = "white"
        info_t.target_btn[idx]['fg'] = "blue"
        info_t.target_on(idx)
        cvs.canvas.itemconfigure(cvs.c_target[idx], state=tk.NORMAL)

    info_t.target_btn_tg[idx] = not info_t.target_btn_tg[idx]


def update_detection_range_img(event, ent, idx):
    im_temp = Image.open('detection.png')
    tCase.patrol[idx].detection_dist = int(ent.get())
    n_pixel = cvs.ratio * tCase.patrol[idx].detection_dist * 2

    im_temp = im_temp.resize((n_pixel, n_pixel), Image.ANTIALIAS)
    cvs.detection_img[idx] = ImageTk.PhotoImage(im_temp)
    cvs.canvas.itemconfigure(cvs.c_patrol_detection[idx], image=cvs.detection_img[idx])

    temp_x, temp_y = tCase.patrol[idx].get_position()
    temp_x, temp_y = cvs.converse(temp_x, temp_y)
    cvs.canvas.coords(cvs.c_patrol_detection[idx], temp_x - (cvs.ratio * cvs.tCase.patrol[idx].detection_dist),
                       temp_y - (cvs.ratio * cvs.tCase.patrol[idx].detection_dist))

def progress_update(value):
    progress_bar["value"] = value
    window.update()

def callback_opt(*args):
    tCase.set_time(option_var.get())
    print(option_var.get())

def draw_init_patrol_cv():
    imgtk_list = []
    for i in range(len(tCase.patrol)):
        src = cv2.imread("Image/patrol_img.png", cv2.IMREAD_UNCHANGED)

        t_x1, t_y1 = tCase.patrol[i].get_path_index(0)
        t_x1, t_y1 = cvs.converse(t_x1, t_y1)
        t_x2, t_y2 = tCase.patrol[i].get_path_index(1)
        t_x2, t_y2 = cvs.converse(t_x2, t_y2)
        height, width, no_channels = src.shape
        angle = 360 - (math.atan2(t_x2 - t_x1, t_y2 - t_y2) * (180.0 / math.pi))
        matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
        dst = cv2.warpAffine(src, matrix, (width, height))

        img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        imgtk_list.append(imgtk)
        # img_pil = ImageTk.PhotoImage(Image.open('image/patrol_img.png'))

    for i in range(len(tCase.patrol)):
        temp_x, temp_y = tCase.patrol[i].get_position()
        temp_x, temp_y = cvs.converse(temp_x, temp_y)
        temp_c = cvs.canvas.create_image(temp_x - 7.5, temp_y - 7.5, image=imgtk_list[i], anchor=tk.NW)
        cvs.c_patrol.append(temp_c)


######## init setting section



tCase = case.testCase(operation_x, operation_y)
tCase.set_operation_margin(oper_margin)
tCase.total_time, count, tCase.patrol, tCase.target = case.readFile()
## init store
init_target = copy.deepcopy(tCase.target)
init_patrol = copy.deepcopy(tCase.patrol)
init_count = copy.deepcopy(count)
init_total_time = copy.deepcopy(tCase.total_time)

idata = read_file_formatting(tCase.patrol, tCase.target)
info_t = sInfoTbl.Table(f_tbl, idata, tCase)

tCase.set_fixed_unit(tCase.patrol, tCase.target)

option_list = [1, 0.75, 0.5]
option_var = tk.DoubleVar(window)
option_var.trace("w", callback_opt)
option_var.set(option_list[0])

opt_lbl = tk.Label(frame_opt, text="배속 : ")

opt = tk.OptionMenu(frame_opt, option_var, *option_list)
opt.config(width=5)
opt.pack(side="right")
opt_lbl.pack(side="right")

cvs = GUI.Canvas(frame_bbs, 550, 400, tCase, operation_x, operation_y)
cvs.init_draw_patrol(tCase.patrol, tCase.target)
cvs.init_draw_target(tCase.target)
cvs.set_operation(0, 0, 20, 10)

resText = GUI.ResultText(frame_bbs, 75, 25)

progress_bar = tk.ttk.Progressbar(frame_pgb, maximum=100, length=300, mode="determinate")
progress_bar.pack()
progress_bar.pack_forget()



bbs = [cvs, resText]
typeChk = type.typeCheck(f_chk, tCase, init_target, info_t, bbs)


btn_reset = tk.Button(frame_btn, text="Reset", overrelief="solid", width=15, command=reset_info)
btn_reset.grid(row=0, column=0, pady=10, padx=5)
btn_run = tk.Button(frame_btn, text="Run", overrelief="solid", width=15, command=toggleBtn)
btn_run.grid(row=0, column=1, pady=10, padx=5)

for i in range(len(info_t.path_list)):
    info_t.path_list[i].bind("<Delete>", lambda event, idx=i: delete_path(event, idx))
    info_t.path_list[i].bind('<Double-Button-1>', lambda  event, idx=i: edit_path(event, idx))
for i in range(len(info_t.path_entry)):
    info_t.path_entry[i].bind("<Return>", lambda event, idx=i: insert_path(event, idx))
for i in range(len(info_t.drange_entry)):
    info_t.drange_entry[i].bind("<Return>", lambda event, ent=info_t.drange_entry[i], idx=i: update_detection_range_img(event, ent, idx))

# print(cvs.set_detection_range_img(tCase.patrol))
set_heading_func()
set_property_func()


window.update()



#
window.mainloop()

