from tkinter import *
import copy
import re

## reference https://www.geeksforgeeks.org/create-table-using-tkinter/
class Table:

    def __init__(self, frame, data, tCase):

        self.init_patrol = copy.deepcopy(tCase.patrol)
        self.init_target = copy.deepcopy(tCase.target)
        self.tCase = tCase
        self.target = copy.copy(tCase.target)

        self.path_entry = []
        self.path_list = []
        self.knot_entry = []
        self.drange_entry = []
        self.patrol_btn = []
        self.patrol_btn_tg = []

        # f_tbl = Frame(frame)
        # f_lbl = Frame(frame)
        # f_chk = Frame(frame)
        #
        # f_tbl.grid(row=2)
        # f_chk.grid(row=1)
        # f_lbl.grid(row=0)
        #
        # ## Check
        # self.radioValue = IntVar()
        # rdioLbl = Label(f_chk, text="Select Target Type : ")
        # rdioF = Radiobutton(f_chk, text="Fixed", variable=self.radioValue, value=1, command=self.toFixed)
        # rdioF.select()
        # rdioR = Radiobutton(f_chk, text="Random", variable=self.radioValue, value=2, command=self.toRandom)
        #
        # rdioLbl.grid(row=0, column=0)
        # rdioF.grid(row=0, column=1)
        # rdioR.grid(row=0, column=2)
        #
        # # Label
        # head_lbl = Label(f_lbl, text="Ship Info.")
        # head_lbl.grid(row=0)

        property_data = ["X", "Y", "Now_d", "Total_d", "Knot", "D_range", "Path"]
        option_num_data = len(data)
        for i in range(option_num_data):
            property_data.insert(4 + i, "T"+str(i+1)+"_d")

        ## setting
        col = len(data[0])+2
        row = len(data)+1
        self.data_t = []
        for i in range(col):
            self.data_t.append([])
            for j in range(row):
                ## first
                if i == 0 and j == 0:
                    lbl = Label(frame, text="", width=10, bg="white")
                    lbl.grid(row=i, column=j)
                ## heading_patrol
                elif i == 0:
                    str_h = "Patrol"+str(j)
                    self.patrol_btn_tg.append(True)
                    btn = Button(frame, text=str_h, width=10, bg="white", relief="solid")
                    # , command=lambda idx=j-1: self.headingToggle(idx)
                    btn.grid(row=i, column=j)
                    self.patrol_btn.append(btn)

                ## property
                elif j == 0:
                    ## path
                    if i == col - 2:
                        lbl = Label(frame, text=property_data[i - 1], height=5, width=10, bg="white")
                        lbl.grid(row=i, column=j)
                    elif i >= col - 1:
                        lbl = Label(frame, text="Add Path", width=10, bg="white")
                        lbl.grid(row=i, column=j)
                    else:
                        lbl = Label(frame, text=property_data[i-1], width=10, bg="white")
                        lbl.grid(row=i, column=j)
                ## path
                elif i == col-2:
                    listBox = Listbox(frame, bg="white", height=5, width=10, justify=CENTER)
                    path = re.split('\n', data[j - 1][-1])
                    for t in range(len(path)):
                        listBox.insert(t, path[t])
                    listBox.grid(row=i, column=j)
                    # listBox.bind("<Delete>", lambda event, idx=j - 1: self.delete_path(event, idx))
                    self.path_list.append(listBox)

                ## path entry
                elif i == col-1:
                    ent = Entry(frame, width=10, bg="white", justify='center')
                    self.path_entry.append(ent)
                    ent.grid(row=i, column=j)
                    vcmd = frame.register(self.callbackPath)
                    ent.config(validate='all', validatecommand=(vcmd, '%P', '%S'))
                    # ent.bind("<Return>", lambda: self.insert_path(self,  j - 1))
                    # ent.bind("<Return>", lambda event, idx=j-1: self.insert_path(event, idx))

                ## D_range
                elif i == col - 3:
                    sv = StringVar()
                    sv.set(data[j - 1][i - 1])
                    self.data_t[i - 1].append(sv)
                    # print("i = {}, j = {}".format(i, j))
                    # print(data_t[i-1][j-1])
                    ent = Entry(frame, textvariable=self.data_t[i - 1][j - 1], width=10, bg="white", justify='center')
                    ent.grid(row=i, column=j)
                    vcmd = frame.register(self.callback)
                    ent.config(validate='all', validatecommand=(vcmd, '%P'))
                    self.drange_entry.append(ent)
                ## knot
                elif i == col - 4:
                    sv = StringVar()
                    sv.set(data[j - 1][i - 1])
                    self.data_t[i - 1].append(sv)
                    # print("i = {}, j = {}".format(i, j))
                    # print(data_t[i-1][j-1])
                    ent = Entry(frame, textvariable=self.data_t[i - 1][j - 1], width=10, bg="white", justify='center')
                    ent.grid(row=i, column=j)
                    vcmd = frame.register(self.callback)
                    ent.config(validate='all', validatecommand=(vcmd, '%P'))
                    self.knot_entry.append(ent)

                ## else data
                else:
                    sv = StringVar()
                    sv.set(data[j - 1][i - 1])
                    self.data_t[i-1].append(sv)
                    # print("i = {}, j = {}".format(i, j))
                    # print(data_t[i-1][j-1])
                    lbl = Label(frame, textvariable=self.data_t[i-1][j-1], width=10, bg="white")
                    lbl.grid(row=i, column=j)

        # self.set_heading_func()

    def update_position(self, edit):
        for i in range(len(self.data_t[0])):
            for j in range(2):
                data = round(edit[i][j], 2)
                self.data_t[j][i].set(data)

    def update_now_detection(self, data):
        for i in range(len(self.data_t[0])):
            now_d = ""
            count_none = 0
            num = len(data[i])
            for j in range(num):
                if data[i][j] != -1:
                    count_none += 1
                    if count_none != 1:
                        now_d += ", "
                    now_d += "T"
                    now_d += str(j+1)

            if count_none == 0:
                self.data_t[2][i].set("None")
            else:
                self.data_t[2][i].set(now_d)


    def update_res_detection(self, case):
        for i in range(len(case.patrol)):
            self.data_t[3][i].set(case.total_accum_t[i])
            for j in range(len(case.target)):
                self.data_t[4+j][i].set(case.accum_time[i][j])

    def reset(self):
        ## i = property, j = patrol num
        for j in range(len(self.data_t[0])):
            self.data_t[0][j].set(self.init_patrol[j].get_x())
            self.data_t[1][j].set(self.init_patrol[j].get_y())
            self.data_t[2][j].set("None")
            self.data_t[3][j].set(0)
            self.data_t[4][j].set(0)
            self.data_t[5][j].set(0)
            self.data_t[6][j].set(0)

        # for i in range(len(self.data_t)):
        #     print("i start")
        #     for j in range(len(self.data_t[i])):
        #         print(str(self.data_t[i][j].get()))

    def callback(self, P):
        # if input.isdigit():
        #     print(input)
        #     return True
        #
        # elif input is "":
        #     print(input)
        #     return True
        #
        # else:
        #     print(input)
        #     return False
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def callbackPath(self, P, S):
        if str.isdigit(P) or P == "":
            return True
        elif S ==" " or S =="," or str.isdigit(S):
            return True
        else:
            return False

    def insert_path_to_entry(self, event, idx):
        origin = self.path_entry[idx].get()

        input = re.split(', ', origin)
        if len(input) == 2:
            if str.isdigit(input[0]) and str.isdigit(input[1]):
                self.tCase.patrol[idx].add_path(int(input[0]), int(input[1]))
                self.path_list[idx].insert(self.path_list[idx].size()-1, origin)
                self.path_entry[idx].delete(0, 'end')

    def delete_path(self, event, idx):
        origin = self.path_list[idx]

        selection = origin.curselection()
        if selection:
            origin.delete(selection)

    def refresh_all_path(self):
        ip = self.init_patrol
        for i in range(len(ip)):
            self.path_list[i].delete(0, 'end')
            for j in range(len(ip[i].path)):
                temp = ""
                temp += str(ip[i].path[j][0])
                temp += ", "
                temp += str(ip[i].path[j][1])
                self.path_list[i].insert(j, temp)

    def set_heading_func(self):
        for i in range(len(self.patrol_btn)):
            print("!")
            self.patrol_btn[i]['command'] = "lambda event, idx=i: headingToggle(event, idx)"
            self.patrol_btn_tg.append(True)
            print(self.patrol_btn[i]['command'])

    def headingToggle(self, idx):
        print(idx)
        if self.patrol_btn_tg[idx]:
            self.patrol_btn[idx]['background'] = "black"
            self.patrol_btn[idx]['fg'] = "green"
        else:
            self.patrol_btn[idx]['background'] = "white"
            self.patrol_btn[idx]['fg'] = "black"

        self.patrol_btn_tg[idx] = not self.patrol_btn_tg[idx]



