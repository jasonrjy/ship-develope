import copy
import tkinter as tk
import time
import case
from PIL import Image, ImageTk, ImageDraw
import sInfoTbl
import GUI
import type
import re

# img = Image.new('RGB', (200, 200), (255, 255, 255))  ## Image에 대한 속성, 픽셀, 색깔 정해주기
# drw = ImageDraw.Draw(img, 'RGBA')
# drw.ellipse([(0, 0), (200, 200)], (255, 255, 255, 255), outline=(255, 255, 0), width=3)
# img.save("detection.png")
#
# image = Image.open("detection.png")
# resize_image = image.resize((100, 100))
# resize_image.save("detection.png")

## -1 == 첫 시작, 0 = stop, 1 = run, 2 = end
global running, store_time
running = -1
store_time = 0


window = tk.Tk()
window.title("Ship Detection Program")
window.geometry("900x500")
window.resizable(0, 0)

frame_info = tk.Frame(window)
frame_bbs = tk.Frame(window, padx=10, pady=10)
frame_btn = tk.Frame(window)

# frame_canvas.pack(side="left", fill="both")
# frame_info.pack(side="right", fill="both")
frame_bbs.grid(row=0, column=0)
frame_info.grid(row=0, column=1)
frame_btn.grid(row=1, column=1)

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
    for t in tCase.target:
        print("x = {}, y = {}, delay = {}".format(t.x, t.y, t.delay))

    global running, store_time
    running = 1

    for i in range(store_time, int(tCase.total_time)):
        store_time = i
        if running == 1:
            ## update time with position and return detection res
            res = tCase.update_time()
            # get now patrol position to list
            patrol_all_p = tCase.get_all_position()
            # re-draw target
            cvs.update_draw_target()
            # re-draw patrol with detection range and detection line
            cvs.update_draw_patrol(res)
            # update x,y
            info_t.update_position(patrol_all_p)
            info_t.update_now_detection(res)
            info_t.update_res_detection(tCase)

            window.update()
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
    case.cal_case_write_text(tt, cnt, tCase.patrol, tCase.target, resText)

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

        cvs.canvas.coords(cvs.c_patrol[i], temp_x - cvs.ship_r, temp_y - cvs.ship_r, temp_x + cvs.ship_r, temp_y + cvs.ship_r)
        # print("c_patorl {} = {}".format(i, canvas.coords(c_patrol[i])))
        cvs.canvas.coords(cvs.c_patrol_detection[i], temp_x - (cvs.ratio * 5), temp_y - (cvs.ratio * 5))
    for i in range(len(cvs.c_target)):
        temp_x, temp_y = tCase.target[i].get_position()
        temp_x, temp_y = cvs.converse(temp_x, temp_y)
        cvs.canvas.coords(cvs.c_target[i], temp_x - cvs.ship_r, temp_y - cvs.ship_r, temp_x + cvs.ship_r, temp_y + cvs.ship_r)
    for i in range(len(cvs.c_patrol_detection_l)):
        for j in range(len(cvs.c_patrol_detection_l[i])):
            cvs.canvas.delete(cvs.c_patrol_detection_l[i][j])

    ## update for path
    cvs.update_init_draw_patrol()
    info_t.refresh_all_path()

    for i in range(len(tCase.patrol)):
        info_t.data_t[8][i].set(tCase.patrol[i].detection_dist)
        info_t.data_t[7][i].set(tCase.patrol[i].knot)



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

        selection = origin.curselection()
        # sel_val = origin.get(selection)
        # sel_val = re.split(', ', sel_val)
        # print(sel_val)
        # print(selection[0])
        if selection:
            if tCase.patrol[idx].delete_path(selection[0]):
                origin.delete(selection)
                cvs.update_init_draw_patrol()


def insert_path(event, idx):
    global running
    if running == -1:
        origin = info_t.path_entry[idx].get()

        input = re.split(', ', origin)
        if len(input) == 2:
            if str.isdigit(input[0]) and str.isdigit(input[1]):
                tCase.patrol[idx].add_path(int(input[0]), int(input[1]))
                info_t.path_list[idx].insert(info_t.path_list[idx].size() - 1, origin)
                info_t.path_entry[idx].delete(0, 'end')
        cvs.update_init_draw_patrol()


def set_heading_func():
    for i in range(len(info_t.patrol_btn)):
        print("!")
        info_t.patrol_btn[i].config(command=lambda idx=i: headingToggle(idx))
        print(info_t.patrol_btn[i]['command'])


def headingToggle(idx):
    print(idx)
    if info_t.patrol_btn_tg[idx]:
        info_t.patrol_btn[idx]['background'] = "black"
        info_t.patrol_btn[idx]['fg'] = "green"
        for i in range(len(cvs.c_patrol_path[idx])):
            cvs.canvas.itemconfigure(cvs.c_patrol_path[idx][i], state=tk.HIDDEN)
        cvs.canvas.itemconfigure(cvs.c_patrol[idx], state=tk.HIDDEN)
        cvs.canvas.itemconfigure(cvs.c_patrol_detection[idx], state=tk.HIDDEN)
    else:
        info_t.patrol_btn[idx]['background'] = "white"
        info_t.patrol_btn[idx]['fg'] = "black"
        for i in range(len(cvs.c_patrol_path[idx])):
            cvs.canvas.itemconfigure(cvs.c_patrol_path[idx][i], state=tk.NORMAL)
        cvs.canvas.itemconfigure(cvs.c_patrol[idx], state=tk.NORMAL)
        cvs.canvas.itemconfigure(cvs.c_patrol_detection[idx], state=tk.NORMAL)

    info_t.patrol_btn_tg[idx] = not info_t.patrol_btn_tg[idx]



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
for i in range(len(info_t.path_list)):
    info_t.path_list[i].bind("<Delete>", lambda event, idx=i: delete_path(event, idx))
for i in range(len(info_t.path_entry)):
    info_t.path_entry[i].bind("<Return>", lambda event, idx=i: insert_path(event, idx))
set_heading_func()

tCase.set_fixed_unit(tCase.patrol, tCase.target)

cvs = GUI.Canvas(frame_bbs, 550, 400, tCase)
cvs.init_draw_patrol(tCase.patrol, tCase.target)
cvs.init_draw_target(tCase.target)

resText = GUI.ResultText(frame_bbs, 75, 25)

bbs = [cvs, resText]
typeChk = type.typeCheck(f_chk, tCase, init_target, info_t, bbs)


btn_reset = tk.Button(frame_btn, text="Reset", overrelief="solid", width=15, command=reset_info)
btn_reset.grid(row=0, column=0, pady=10, padx=5)
btn_run = tk.Button(frame_btn, text="Run", overrelief="solid", width=15, command=toggleBtn)
btn_run.grid(row=0, column=1, pady=10, padx=5)


window.update()

########
# run_canvas()


#
window.mainloop()

