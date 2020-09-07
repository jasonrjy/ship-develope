import tkinter as tk
import tkinter.ttk
import tkinter.font
from tkinter.messagebox import showinfo
import tkinter.simpledialog
import case
import operation
import sInfoTbl
import copy
import re
import GUI

class resText:
    def __init__(self, frame, window_update):
        self.window_update = window_update

        self.frame_text = tk.Frame(frame, padx=10, pady=10, bg="white")
        self.frame_info = tk.Frame(frame, padx=10, pady=10, bg="white")
        self.frame_btn = tk.Frame(frame, padx=10, pady=10, bg="white")
        self.frame_pgb = tk.Frame(frame, padx=10, pady=10, bg="white")

        self.frame_text.grid(row=0, column=0)
        self.frame_info.grid(row=0, column=1, sticky="N")
        self.frame_btn.grid(row=1, column=1)
        self.frame_pgb.grid(row=1, column=0)

        self.frame_info_tbl = tk.Frame(self.frame_info, bg="white")
        self.frame_info_lbl = tk.Frame(self.frame_info, bg="white")
        self.frame_info_opt = tk.Frame(self.frame_info, bg="white", pady=5)
        self.frame_info_opt_cnt = tk.Frame(self.frame_info_opt, bg="white")

        self.frame_info_lbl.grid(row=0)
        self.frame_info_opt.grid(row=1)
        self.frame_info_tbl.grid(row=2)
        self.frame_info_opt_cnt.pack()

        self.resText = GUI.ResultText(self.frame_text, 75, 23)

        self.operation = operation.Operation()
        self.tCase = case.testCase(self.operation)
        self.tCase.set_init()

        self.idata = self.read_file_formatting(self.tCase.patrol, self.tCase.target)
        self.info_lbl = tk.Label(self.frame_info_lbl, text="Ship Info.", bg="white")
        self.info_lbl.pack()
        self.info_cnt_lbl = tk.Label(self.frame_info_opt, text="")

        self.countVal = tk.IntVar()
        self.countEntry = tk.Entry(self.frame_info_opt_cnt, width=10, textvariable=self.countVal,
                                   justify='center', bg="white")
        vcmd = frame.register(self.callback)
        self.countEntry.config(validate='all', validatecommand=(vcmd, '%P'))
        self.printStr = tk.Label(self.frame_info_opt_cnt, text="실행 횟수 : ", bg="white")
        self.printStr.pack(side=tk.LEFT)
        self.countEntry.pack(side=tk.LEFT)
        self.countVal.set(1)

        self.info_tbl = sInfoTbl.Table(self.frame_info_tbl, self.idata, self.tCase)

        self.tCase.set_fixed_unit(self.tCase.patrol, self.tCase.target)

        self.progress_bar = tk.ttk.Progressbar(self.frame_pgb, maximum=100, length=300, mode="determinate")
        self.progress_bar.pack()
        self.progress_bar.pack_forget()

        self.btn_reset = tk.Button(self.frame_btn, text="Reset", overrelief="solid", width=15, command=self.reset_info,
                                   bg="white")
        self.btn_reset.grid(row=0, column=0, pady=10, padx=5)
        self.btn_run = tk.Button(self.frame_btn, text="Run", overrelief="solid", width=15, command=self.toggleBtn,
                                 bg="white")
        self.btn_run.grid(row=0, column=1, pady=10, padx=5)

        for i in range(len(self.info_tbl.path_list)):
            self.info_tbl.path_list[i].bind("<Delete>", lambda event, idx=i: self.delete_path(event, idx))
            self.info_tbl.path_list[i].bind('<Double-Button-1>', lambda event, idx=i: self.edit_path(event, idx))
        for i in range(len(self.info_tbl.path_entry)):
            self.info_tbl.path_entry[i].bind("<Return>", lambda event, idx=i: self.insert_path(event, idx))
        # for i in range(len(self.info_tbl.drange_entry)):
        #     self.info_tbl.drange_entry[i].bind("<Return>",
        #                                 lambda event, ent=self.info_tbl.drange_entry[i], idx=i: self.update_detection_range_img(
        #                                     event, ent, idx))

        self.set_heading_func()
        self.set_property_func()

        self.window_update()


    def reset_info(self):
        self.running = -1
        self.tCase.count = 0

        self.btn_run['state'] = tk.NORMAL
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

        # if self.type.targetType.get() == 2:
        #     self.type.RdiotoRandom()
        # else:
        #     self.tCase.target = copy.deepcopy(self.tCase.init.target)

        self.idata = self.read_file_formatting(self.tCase.patrol, self.tCase.target)
        self.tCase.accum_t = 0
        self.info_tbl.reset()
        self.tCase.count = 0

        self.tCase.set_fixed_unit(self.tCase.patrol, self.tCase.target)

        ## update for path
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
        for i in self.info_tbl.path_entry:
            i['state'] = tk.DISABLED
        for i in range(len(self.tCase.patrol)):
            self.info_tbl.drange_entry[i]['state'] = tk.DISABLED
            self.info_tbl.knot_entry[i]['state'] = tk.DISABLED
            self.info_tbl.path_list[i]['state'] = tk.DISABLED
            self.info_tbl.path_entry[i]['state'] = tk.DISABLED
            self.info_tbl.patrol_btn[i]['state'] = tk.DISABLED
            self.info_tbl.target_btn[i]['state'] = tk.DISABLED
        self.btn_run['state'] = tk.DISABLED

        self.running = 1

        ## get setting val
        self.tCase.set_info_data(self.info_tbl)
        self.run_result()

        self.btn_run['state'] = tk.NORMAL
        for i in self.info_tbl.path_entry:
            i['state'] = tk.NORMAL
        for i in range(len(self.tCase.patrol)):
            self.info_tbl.drange_entry[i]['state'] = tk.NORMAL
            self.info_tbl.knot_entry[i]['state'] = tk.NORMAL
            self.info_tbl.path_list[i]['state'] = tk.NORMAL
            self.info_tbl.path_entry[i]['state'] = tk.NORMAL
            self.info_tbl.patrol_btn[i]['state'] = tk.NORMAL
            self.info_tbl.target_btn[i]['state'] = tk.NORMAL

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

    def insert_path(self, event, idx):
        if self.running == -1:
            origin = self.info_tbl.path_entry[idx].get()
            input_index = self.info_tbl.path_list[idx].size() - 1
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

                showinfo('경로를 수정합니다', res)
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
            self.info_tbl.patrol_off(idx)
        else:
            self.info_tbl.patrol_btn[idx]['background'] = "white"
            self.info_tbl.patrol_btn[idx]['fg'] = "blue"
            self.info_tbl.patrol_on(idx)

        self.info_tbl.patrol_btn_tg[idx] = not self.info_tbl.patrol_btn_tg[idx]

    def property_target_toggle(self, idx):
        ## false
        if self.info_tbl.target_btn_tg[idx]:
            self.info_tbl.target_btn[idx]['background'] = "#808080"
            self.info_tbl.target_btn[idx]['fg'] = "#a0a0a0"
            self.info_tbl.target_off(idx)
        else:
            self.info_tbl.target_btn[idx]['background'] = "white"
            self.info_tbl.target_btn[idx]['fg'] = "blue"
            self.info_tbl.target_on(idx)

        self.info_tbl.target_btn_tg[idx] = not self.info_tbl.target_btn_tg[idx]

    def progress_update(self, value):
        self.progress_bar["value"] = value
        self.window_update()

    def run_result(self):
        self.running = 1
        cnt = int(self.countVal.get())

        font = tk.font.Font(weight="bold", size=10)
        self.resText.text.config(state=tk.NORMAL, font=font)
        # progress_bar.start(10)
        self.progress_bar.pack()
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = cnt

        case.cal_case_write_text(self.tCase.total_time, cnt, self.tCase.patrol, self.tCase.target, self.resText,
                                 self.info_tbl.patrol_btn_tg, self.info_tbl.target_btn_tg,
                                 self.progress_update, self.operation)
        self.resText.text.config(state=tk.DISABLED)
        self.progress_bar.pack_forget()

    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
