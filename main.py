import copy
import tkinter as tk
import time
import case
from PIL import Image, ImageTk, ImageDraw
import sInfoTbl
import GUI

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
window.geometry("800x500")
window.resizable(0, 0)

frame_info = tk.Frame(window)
frame_bbs = tk.Frame(window)
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


def RdiotoFixed():
    tCase.target = copy.deepcopy(init_target)
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
        print(i)
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

def reset_info():
    global running, store_time
    running = -1
    store_time = 0

    btn_run['state'] = tk.NORMAL
    rdioR['state'] = tk.NORMAL
    rdioF['state'] = tk.NORMAL
    if btn_run['text'] == 'Stop':
        btn_run['text'] = 'Run'

    tCase.patrol = copy.deepcopy(init_patrol)
    for i in range(len(tCase.total_accum_t)):
        tCase.total_accum_t[i] = 0
    for i in range(len(tCase.accum_time)):
        for j in range(len(tCase.accum_time[i])):
            tCase.accum_time[i][j] = 0

    if radioValue.get() == 2:
        RdiotoRandom()
    else:
        tCase.target = copy.deepcopy(init_target)
    idata = read_file_formatting(tCase.patrol, tCase.target)
    tCase.accum_t = 0
    info_t.reset()
    count = 0

    tCase.set_fixed_unit(tCase.patrol, tCase.target)

    for i in range(len(c_patrol)):
        temp_x, temp_y = tCase.patrol[i].get_position()
        temp_x, temp_y = converse(temp_x, temp_y)
        # print("c_patorl {} = {}".format(i, canvas.coords(c_patrol[i])))

        canvas.coords(c_patrol[i], temp_x - ship_r, temp_y - ship_r, temp_x + ship_r, temp_y + ship_r)
        # print("c_patorl {} = {}".format(i, canvas.coords(c_patrol[i])))
        canvas.coords(c_patrol_detection[i], temp_x - (ratio * 5), temp_y - (ratio * 5))
    for i in range(len(c_target)):
        temp_x, temp_y = tCase.target[i].get_position()
        temp_x, temp_y = converse(temp_x, temp_y)
        canvas.coords(c_target[i], temp_x - ship_r, temp_y - ship_r, temp_x + ship_r, temp_y + ship_r)
    for i in range(len(c_patrol_detection_l)):
        for j in range(len(c_patrol_detection_l[i])):
            canvas.delete(c_patrol_detection_l[i][j])
    #
    # init_draw_patrol(tCase.patrol, tCase.target)
    # init_draw_target(tCase.target)


def toggleBtn():
    global running

    if(btn_run['text']=='Run'):
        rdioF['state'] = tk.DISABLED
        rdioR['state'] = tk.DISABLED
        btn_run['text']='Stop'
        running = 1
        run_canvas()

    elif(btn_run['text']=='Stop'):
        btn_run['text']='Run'
        running = 0


def run_ready():
    global running
    if running == 1:
        print(running)
        return True
    print(running)
    return False

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

cvs = GUI.Canvas(frame_bbs, 400, 300, tCase)
cvs.init_draw_patrol(tCase.patrol, tCase.target)
cvs.init_draw_target(tCase.target)


btn_reset = tk.Button(frame_btn, text="Reset", overrelief="solid", width=15, command=reset_info)
btn_reset.grid(row=0, column=0, pady=10, padx=5)
btn_run = tk.Button(frame_btn, text="Run", overrelief="solid", width=15, command=toggleBtn)
btn_run.grid(row=0, column=1, pady=10, padx=5)


window.update()

########
# run_canvas()


#
window.mainloop()

