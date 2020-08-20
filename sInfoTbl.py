from tkinter import *
import copy

## reference https://www.geeksforgeeks.org/create-table-using-tkinter/
class Table:

    def __init__(self, frame, data, tCase):

        self.init_patrol = copy.deepcopy(tCase.patrol)
        self.init_target = copy.deepcopy(tCase.target)
        self.tCase = tCase
        self.target = copy.copy(tCase.target)

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
        col = len(data[0])+1
        row = len(data)+1
        self.data_t = []

        for i in range(col):
            self.data_t.append([])
            for j in range(row):
                ## first
                if i == 0 and j == 0:
                    lbl = Label(frame, text="", width=10, bg="white")
                    lbl.grid(row=i, column=j)
                ## heading
                elif i == 0:
                    str_h = "Patrol"+str(j)
                    lbl = Label(frame, text=str_h, width=10, bg="white")
                    lbl.grid(row=i, column=j)
                ## property
                elif j == 0:
                    lbl = Label(frame, text=property_data[i-1], width=10, bg="white")
                    lbl.grid(row=i, column=j)
                ## path
                elif j == row-1:
                    sv = StringVar()
                    sv.set(data[j - 1][i - 1])
                    self.data_t[i - 1].append(sv)
                    # print("i = {}, j = {}".format(i, j))
                    # print(data_t[i-1][j-1])
                    lbl = Label(frame, textvariable=self.data_t[i - 1][j - 1], width=10, bg="white", )
                    lbl.grid(row=i, column=j)

                ## else data
                else:
                    sv = StringVar()
                    sv.set(data[j - 1][i - 1])
                    self.data_t[i-1].append(sv)
                    # print("i = {}, j = {}".format(i, j))
                    # print(data_t[i-1][j-1])
                    lbl = Label(frame, textvariable=self.data_t[i-1][j-1], width=10, bg="white")
                    lbl.grid(row=i, column=j)

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






