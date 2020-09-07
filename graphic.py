import tkinter as tk
import copy
import case
import operation
import sInfoTbl
import GUI
import time
import re
import cv2
import math
from tkinter.messagebox import showinfo
import type
from PIL import Image, ImageTk

class Graphic:
    def __init__(self, frame, window_update):
        self.window_update = window_update

        self.frame_bbs = tk.Frame(frame, padx=10, pady=10, bg="white")
        self.frame_info = tk.Frame(frame, padx=10, pady=10, bg="white")
        self.frame_btn = tk.Frame(frame, padx=10, pady=10, bg="white")
        self.frame_opt = tk.Frame(self.frame_bbs, bg="white")

        self.frame_bbs.grid(row=0, column=0)
        self.frame_info.grid(row=0, column=1, sticky="N")
        self.frame_btn.grid(row=1, column=1)
        self.frame_opt.pack(anchor=tk.E)

        self.frame_info_tbl = tk.Frame(self.frame_info, bg="white")
        self.frame_info_lbl = tk.Frame(self.frame_info, bg="white")
        self.frame_info_type = tk.Frame(self.frame_info, bg="white")

        self.frame_info_lbl.grid(row=0)
        self.frame_info_type.grid(row=1)
        self.frame_info_tbl.grid(row=2)

        self.operation = operation.Operation()
        self.tCase = case.testCase(self.operation)
        self.tCase.set_init()

        ## -1 == 첫 시작, 0 = stop, 1 = run, 2 = end
        self.running = -1

        self.idata = self.read_file_formatting(self.tCase.patrol, self.tCase.target)
        self.info_lbl = tk.Label(self.frame_info_lbl, text="Ship Info.", bg="white")
        self.info_lbl.pack()
        self.info_tbl = sInfoTbl.Table(self.frame_info_tbl, self.idata, self.tCase)

        self.tCase.set_fixed_unit(self.tCase.patrol, self.tCase.target)

        self.option_list = [1, 0.75, 0.5]
        self.option_var = tk.DoubleVar()
        self.option_var.trace("w", self.callback_opt)
        self.option_var.set(self.option_list[0])

        self.opt_lbl = tk.Label(self.frame_opt, text="배속 : ", bg="white")

        self.opt = tk.OptionMenu(self.frame_opt, self.option_var, *self.option_list)
        self.opt.config(width=5)
        self.opt.pack(side="right")
        self.opt_lbl.pack(side="right")

        self.cvs = GUI.Canvas(self.frame_bbs, 550, 400, self.tCase, self.operation.x, self.operation.y)
        self.cvs.init_draw_patrol(self.tCase.patrol, self.tCase.target)
        self.cvs.init_draw_target(self.tCase.target)
        self.cvs.set_operation(0, 0, self.operation.x, self.operation.y)


        # progress_bar = tk.ttk.Progressbar(self.frame_pgb, maximum=100, length=300, mode="determinate")
        # progress_bar.pack()
        # progress_bar.pack_forget()

        # bbs = [self.cvs, resText]
        self.type = type.typeCheck(self.frame_info_type, self.tCase, self.info_tbl)

        self.btn_reset = tk.Button(self.frame_btn, text="Reset", overrelief="solid", width=15, command=self.reset_info, bg="white")
        self.btn_reset.grid(row=0, column=0, pady=10, padx=5)
        self.btn_run = tk.Button(self.frame_btn, text="Run", overrelief="solid", width=15, command=self.toggleBtn, bg="white")
        self.btn_run.grid(row=0, column=1, pady=10, padx=5)

        for i in range(len(self.info_tbl.path_list)):
            self.info_tbl.path_list[i].bind("<Delete>", lambda event, idx=i: self.delete_path(event, idx))
            self.info_tbl.path_list[i].bind('<Double-Button-1>', lambda event, idx=i: self.edit_path(event, idx))
        for i in range(len(self.info_tbl.path_entry)):
            self.info_tbl.path_entry[i].bind("<Return>", lambda event, idx=i: self.insert_path(event, idx))
        for i in range(len(self.info_tbl.drange_entry)):
            self.info_tbl.drange_entry[i].bind("<Return>",
                                        lambda event, ent=self.info_tbl.drange_entry[i], idx=i: self.update_detection_range_img(
                                            event, ent, idx))

        # print(self.cvs.set_detection_range_img(tCase.patrol))
        self.set_heading_func()
        self.set_property_func()

        self.window_update()


    def path_to_string(self, s):
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

    def path_to_string_nl(self, s):
        res = ""
        i = 0
        for i in range(len(s)):
            res += str(s[i][0])
            res += ", "
            res += str(s[i][1])
            res += '\n'
        res = res[:-1]

        return res

    def read_file_formatting(self, patrol, target):
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
            data[i][-1] = self.path_to_string_nl(patrol[i].get_path())
            # 탐지 범위
            data[i][-2] = patrol[i].get_detection_dist()
            # Knot
            data[i][-3] = patrol[i].get_knot()
            # target detection time
            for j in range(len(target)):
                data[i][4 + j] = 0

        return data

    def run_canvas(self):
        if self.type.targetType == 2:
            self.tCase.target = self.tCase.set_rand_target(self.tCase.total_time)
        for t in self.tCase.target:
            print("x = {}, y = {}, delay = {}".format(t.x, t.y, t.delay))

        self.running = 1

        while self.tCase.count < int(self.tCase.total_time):
            self.tCase.count += self.tCase.time
            if self.running == 1:
                ## update time with position and return detection res
                res, path_changed = self.tCase.update_time(self.info_tbl.patrol_btn_tg, self.info_tbl.target_btn_tg)
                self.cvs.patrol_changed_path(path_changed)

                # get now patrol position to list
                patrol_all_p = self.tCase.get_all_position()
                # re-draw target
                self.cvs.update_draw_target(self.info_tbl.target_btn_tg)
                for i in range(len(self.tCase.target)):
                    self.cvs.set_target_img(i)
                # re-draw patrol with detection range and detection line
                self.cvs.update_draw_patrol(res, self.info_tbl.patrol_btn_tg, self.info_tbl.target_btn_tg)
                # update x,y
                self.info_tbl.update_position(patrol_all_p)
                self.info_tbl.update_now_detection(res)
                self.info_tbl.update_res_detection(self.tCase)

                # print(info_t.tbl[8][1]['disabledbackground'])
                # info_t.tbl[8][1].configure(disabledbackground="#666666")
                # print(info_t.tbl[8][1]['disabledbackground'])
                self.window_update()
                # print(info_t.tbl[8][1]['background'])
                time.sleep(0.03)
            else:
                return i
                # print("waiting start")
                # # waiting.wait(lambda: run_ready(), timeout_seconds=120, waiting_for="something to be ready")
                # print("waiting end")

        ## stop이 아니면 > 루프가 끝났다면
        if self.running != 0:
            self.btn_run['state'] = tk.DISABLED

    def reset_info(self):
        self.running = -1
        self.tCase.count = 0

        self.btn_run['state'] = tk.NORMAL
        self.type.rdioR['state'] = tk.NORMAL
        self.type.rdioF['state'] = tk.NORMAL
        for i in self.info_tbl.path_entry:
            i['state'] = tk.NORMAL
        for i in range(len(self.tCase.patrol)):
            self.info_tbl.drange_entry[i]['state'] = tk.NORMAL
            self.info_tbl.knot_entry[i]['state'] = tk.NORMAL
            self.info_tbl.path_list[i]['state'] = tk.NORMAL
            self.info_tbl.path_entry[i]['state'] = tk.NORMAL
            self.info_tbl.patrol_btn[i]['state'] = tk.NORMAL
            self.info_tbl.target_btn[i]['state'] = tk.NORMAL
        if self.btn_run['text'] == 'Stop':
            self.btn_run['text'] = 'Run'

        self.tCase.patrol = copy.deepcopy(self.tCase.init.patrol)
        for i in range(len(self.tCase.total_accum_t)):
            self.tCase.total_accum_t[i] = 0
        for i in range(len(self.tCase.accum_time)):
            for j in range(len(self.tCase.accum_time[i])):
                self.tCase.accum_time[i][j] = 0

        if self.type.targetType.get() == 2:
            self.type.RdiotoRandom()
        else:
            self.tCase.target = copy.deepcopy(self.tCase.init.target)
        self.idata = self.read_file_formatting(self.tCase.patrol, self.tCase.target)
        self.tCase.accum_t = 0
        self.info_tbl.reset()
        self.tCase.count = 0

        self.tCase.set_fixed_unit(self.tCase.patrol, self.tCase.target)

        for i in range(len(self.cvs.c_patrol)):
            temp_x, temp_y = self.tCase.patrol[i].get_position()
            temp_x, temp_y = self.cvs.converse(temp_x, temp_y)
            # print("c_patorl {} = {}".format(i, canvas.coords(c_patrol[i])))

            self.cvs.canvas.coords(self.cvs.c_patrol[i], temp_x - self.cvs.patrol_r, temp_y - self.cvs.patrol_r)
            # print("c_patorl {} = {}".format(i, canvas.coords(c_patrol[i])))
            ## init size c_patrol_detection
            self.cvs.set_detection_range_img(self.tCase.patrol)
            self.cvs.canvas.coords(self.cvs.c_patrol_detection[i], temp_x - (self.cvs.ratio * 5), temp_y - (self.cvs.ratio * 5))
            self.cvs.set_patrol_img(i)
        for i in range(len(self.cvs.c_target)):
            temp_x, temp_y = self.tCase.target[i].get_position()
            temp_x, temp_y = self.cvs.converse(temp_x, temp_y)
            self.cvs.canvas.coords(self.cvs.c_target[i], temp_x - self.cvs.target_r, temp_y - self.cvs.target_r)
        for i in range(len(self.cvs.c_patrol_detection_l)):
            for j in range(len(self.cvs.c_patrol_detection_l[i])):
                self.cvs.canvas.delete(self.cvs.c_patrol_detection_l[i][j])

        ## update for path
        self.cvs.update_init_draw_patrol()
        self.info_tbl.refresh_all_path()

        for i in range(len(self.tCase.patrol)):
            self.info_tbl.data_t[8][i].set(self.tCase.patrol[i].detection_dist)
            self.info_tbl.data_t[7][i].set(self.tCase.patrol[i].knot)

        ## reset patrol tg
        btn_tg = self.info_tbl.patrol_btn_tg
        for i in range(len(btn_tg)):
            btn_tg[i] = False
            self.heading_patrol_toggle(i)

        ## reset target tgg
        btn_tg = self.info_tbl.target_btn_tg
        for i in range(len(btn_tg)):
            btn_tg[i] = False
            self.property_target_toggle(i)

    def toggleBtn(self):
        if (self.btn_run['text'] == 'Run'):
            self.type.rdioF['state'] = tk.DISABLED
            self.type.rdioR['state'] = tk.DISABLED
            for i in self.info_tbl.path_entry:
                i['state'] = tk.DISABLED
            for i in range(len(self.tCase.patrol)):
                self.info_tbl.drange_entry[i]['state'] = tk.DISABLED
                self.info_tbl.knot_entry[i]['state'] = tk.DISABLED
                self.info_tbl.path_list[i]['state'] = tk.DISABLED
                self.info_tbl.path_entry[i]['state'] = tk.DISABLED
                self.info_tbl.patrol_btn[i]['state'] = tk.DISABLED
                self.info_tbl.target_btn[i]['state'] = tk.DISABLED

            self.btn_run['text'] = 'Stop'
            self.running = 1

            ## get setting val
            self.tCase.set_info_data(self.info_tbl)
            self.cvs.set_detection_range_img(self.tCase.patrol)
            self.run_canvas()

        elif (self.btn_run['text'] == 'Stop'):
            self.btn_run['text'] = 'Run'
            self.running = 0

    def run_ready(self):
        if self.running == 1:
            return True
        return False

    def delete_path(self, event, idx):
        if self.running == -1:
            origin = self.info_tbl.path_list[idx]

            ## selection = list_box에서 선택된 것들의 리스트 // 단일선택만 되니 [0]만 존재
            selection = origin.curselection()
            # sel_val = origin.get(selection)
            # sel_val = re.split(', ', sel_val)
            # print(sel_val)
            # print(selection[0])
            if selection:
                if self.tCase.patrol[idx].delete_path(selection[0]):
                    print(selection[0])
                    if selection[0] in [0, origin.size() - 1]:
                        origin.delete(origin.size() - 1)
                        origin.delete(0)
                        origin.insert("end", origin.get(0))
                    else:
                        origin.delete(selection)
                    self.cvs.update_init_draw_patrol()

    def insert_path(self, event, idx):
        if self.running == -1:
            origin = self.info_tbl.path_entry[idx].get()
            input_index = self.info_t.path_list[idx].size() - 1
            if origin.find(": ") != -1:
                temp = re.split(': ', origin)
                input_index = int(temp[0])
                origin = temp[1]
            input = re.split(', ', origin)
            if len(input) == 2:
                if str.isdigit(input[0]) and str.isdigit(input[1]):
                    self.tCase.patrol[idx].add_path_index(input_index, int(input[0]), int(input[1]))
                    self.info_tbl.path_list[idx].insert(input_index, origin)
                    self.info_tbl.path_entry[idx].delete(0, 'end')
            self.cvs.update_init_draw_patrol()

    def edit_path(self, event, idx):
        if self.running == -1:
            origin = self.info_tbl.path_list[idx]
            selection = origin.curselection()

            res = tk.simpledialog.askstring("Patrol Path", "경로를 입력해주십시오.")
            if self.is_path_format(res):
                if selection[0] in [0, origin.size() - 1]:
                    origin.delete(0)
                    origin.insert(0, res)
                    origin.delete(origin.size() - 1)
                    origin.insert(origin.size(), res)

                    self.tCase.patrol[idx].update_path(0, res)
                    self.tCase.patrol[idx].update_path(origin.size() - 1, res)
                else:
                    origin.delete(selection[0])
                    origin.insert(selection[0], res)
                    self.tCase.patrol[idx].update_path(selection[0], res)

                self.showinfo('경로를 수정합니다', res)
                self.cvs.update_init_draw_patrol()
            else:
                self.show_canceled()

    def show_canceled(self):
        showinfo('Canceled', 'You canceled')

    def is_path_format(self, path_str):
        input = re.split(', ', path_str)
        if len(input) == 2:
            if str.isdigit(input[0]) and str.isdigit(input[1]):
                return True
        return False

    def set_heading_func(self):
        for i in range(len(self.info_tbl.patrol_btn)):
            self.info_tbl.patrol_btn[i].config(command=lambda idx=i: self.heading_patrol_toggle(idx))

    def set_property_func(self):
        for i in range(len(self.info_tbl.target_btn)):
            self.info_tbl.target_btn[i].config(command=lambda idx=i: self.property_target_toggle(idx))

    def heading_patrol_toggle(self, idx):
        ## false
        if self.info_tbl.patrol_btn_tg[idx]:
            self.info_tbl.patrol_btn[idx]['background'] = "#808080"
            self.info_tbl.patrol_btn[idx]['fg'] = "#a0a0a0"
            for i in range(len(self.cvs.c_patrol_path[idx])):
                self.cvs.canvas.itemconfigure(self.cvs.c_patrol_path[idx][i], state=tk.HIDDEN)
            self.cvs.canvas.itemconfigure(self.cvs.c_patrol[idx], state=tk.HIDDEN)
            self.cvs.canvas.itemconfigure(self.cvs.c_patrol_detection[idx], state=tk.HIDDEN)
            self.info_tbl.patrol_off(idx)
        else:
            self.info_tbl.patrol_btn[idx]['background'] = "white"
            self.info_tbl.patrol_btn[idx]['fg'] = "blue"
            for i in range(len(self.cvs.c_patrol_path[idx])):
                self.cvs.canvas.itemconfigure(self.cvs.c_patrol_path[idx][i], state=tk.NORMAL)
            self.cvs.canvas.itemconfigure(self.cvs.c_patrol[idx], state=tk.NORMAL)
            self.cvs.canvas.itemconfigure(self.cvs.c_patrol_detection[idx], state=tk.NORMAL)
            self.info_tbl.patrol_on(idx)

        self.info_tbl.patrol_btn_tg[idx] = not self.info_tbl.patrol_btn_tg[idx]

    def property_target_toggle(self, idx):
        ## false
        if self.info_tbl.target_btn_tg[idx]:
            self.info_tbl.target_btn[idx]['background'] = "#808080"
            self.info_tbl.target_btn[idx]['fg'] = "#a0a0a0"
            self.info_tbl.target_off(idx)
            self.cvs.canvas.itemconfigure(self.cvs.c_target[idx], state=tk.HIDDEN)
        else:
            self.info_tbl.target_btn[idx]['background'] = "white"
            self.info_tbl.target_btn[idx]['fg'] = "blue"
            self.info_tbl.target_on(idx)
            self.cvs.canvas.itemconfigure(self.cvs.c_target[idx], state=tk.NORMAL)

        self.info_tbl.target_btn_tg[idx] = not self.info_tbl.target_btn_tg[idx]

    def update_detection_range_img(self, event, ent, idx):
        im_temp = Image.open('detection.png')
        self.tCase.patrol[idx].detection_dist = int(ent.get())
        n_pixel = self.cvs.ratio * self.tCase.patrol[idx].detection_dist * 2

        im_temp = im_temp.resize((n_pixel, n_pixel), Image.ANTIALIAS)
        self.cvs.detection_img[idx] = ImageTk.PhotoImage(im_temp)
        self.cvs.canvas.itemconfigure(self.cvs.c_patrol_detection[idx], image=self.cvs.detection_img[idx])

        temp_x, temp_y = self.tCase.patrol[idx].get_position()
        temp_x, temp_y = self.cvs.converse(temp_x, temp_y)
        self.cvs.canvas.coords(self.cvs.c_patrol_detection[idx], temp_x - (self.cvs.ratio * self.cvs.tCase.patrol[idx].detection_dist),
                          temp_y - (self.cvs.ratio * self.cvs.tCase.patrol[idx].detection_dist))

    def progress_update(self, value):
        self.progress_bar["value"] = value
        self.window_update()

    def callback_opt(self, *args):
        self.tCase.set_time(self.option_var.get())
        print(self.option_var.get())

    def draw_init_patrol_cv(self):
        imgtk_list = []
        for i in range(len(self.tCase.patrol)):
            src = cv2.imread("Image/patrol_img.png", cv2.IMREAD_UNCHANGED)

            t_x1, t_y1 = self.tCase.patrol[i].get_path_index(0)
            t_x1, t_y1 = self.cvs.converse(t_x1, t_y1)
            t_x2, t_y2 = self.tCase.patrol[i].get_path_index(1)
            t_x2, t_y2 = self.cvs.converse(t_x2, t_y2)
            height, width, no_channels = src.shape
            angle = 360 - (math.atan2(t_x2 - t_x1, t_y2 - t_y2) * (180.0 / math.pi))
            matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
            dst = cv2.warpAffine(src, matrix, (width, height))

            img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            imgtk_list.append(imgtk)
            # img_pil = ImageTk.PhotoImage(Image.open('image/patrol_img.png'))

        for i in range(len(self.tCase.patrol)):
            temp_x, temp_y = self.tCase.patrol[i].get_position()
            temp_x, temp_y = self.cvs.converse(temp_x, temp_y)
            temp_c = self.cvs.canvas.create_image(temp_x - 7.5, temp_y - 7.5, image=imgtk_list[i], anchor=tk.NW)
            self.cvs.c_patrol.append(temp_c)