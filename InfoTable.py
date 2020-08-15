import tkinter.ttk
import tkinter as tk



def update_info(info_t, data):
    # temp = info_t.selection_set("x")
    # print(temp)
    # info_t.delete(temp)
    # temp = info_t.selection_set("y")
    # info_t.delete(temp)
    pass

def path_to_string(s):
    res = ""
    for i in range(len(s)-1):
        res += str(s[i][0])
        res += ", "
        res += str(s[i][1])
        res += " > "
    res += str(s[i][0])
    res += ", "
    res += str(s[i][1])

    return res


def read_file_formatting(self, patrol, target):
    data = []

    for i in range(len(patrol)):
        data.append([])
        for j in range(len(target)+7):
            data[i].append(0)

    for i in range(len(patrol)):
        data[i][0] = patrol[i].get_x()
        data[i][1] = patrol[i].get_y()
        # 현 탐지
        data[i][2] = 0
        # 총 탐지
        data[i][3] = 0
        # 경로
        data[i][-1] = self.path_to_string(patrol[i].get_path())
        # 탐지 범위
        data[i][-2] = patrol[i].get_detection_dist()
        # Knot
        data[i][-3] = patrol[i].get_knot()
        # target detection time
        for j in range(len(target)):
            data[i][4+j] = 0

    return data


def init_info(frame_i, init_data):
    ## setting info
    info_lbl = tk.Label(frame_i, text="Ship Info")
    info_lbl.pack()
    # setting treeView
    info_tree = tk.ttk.Treeview(frame_i, columns=["함정 1", "함정 2", "함정 3"], displaycolumns=["함정 1", "함정 2", "함정 3"])
    info_tree.pack()

    # 0행
    info_tree.column("#0", width=30, anchor="center")
    info_tree.heading("#0", text="속성")
    # 1행
    info_tree.column("#1", width=70, anchor="w")
    info_tree.heading("#1", text="함정 1", anchor="center")
    # 2행
    info_tree.column("#2", width=70, anchor="w")
    info_tree.heading("#2", text="함정 2", anchor="center")
    # 3행
    info_tree.column("#3", width=70, anchor="w")
    info_tree.heading("#3", text="함정 3", anchor="center")

    ## insert table
    data = []
    for i in range(len(init_data)):
        data.append(init_data[i][0])
    info_tree.insert('', "end", text="X", values=data, iid="x")


    data = []
    for i in range(len(init_data)):
        data.append(init_data[i][1])
    info_tree.insert('', "end", text="Y", values=data, iid="y")


    data = []
    for i in range(len(init_data)):
        data.append(init_data[i][2])
    info_tree.insert('', "end", text="Now_d", values=data, iid="nd" + str(i))

    data = []
    for i in range(len(init_data)):
        data.append(init_data[i][3])
    info_tree.insert('', "end", text="Total_d", values=data, iid="td" + str(i))

    data = []
    for i in range(len(init_data)):
        data.append(init_data[i][4])
    info_tree.insert('', "end", text="T1", values=data, iid="t1" + str(i))

    data = []
    for i in range(len(init_data)):
        data.append(init_data[i][5])
    info_tree.insert('', "end", text="T2", values=data, iid="t2" + str(i))

    data = []
    for i in range(len(init_data)):
        data.append(init_data[i][6])
    info_tree.insert('', "end", text="T3", values=data, iid="t3" + str(i))

    data = []
    for i in range(len(init_data)):
        data.append(init_data[i][7])
    info_tree.insert('', "end", text="Knot", values=data, iid="knot" + str(i))

    data = []
    for i in range(len(init_data)):
        data.append(init_data[i][8])
    info_tree.insert('', "end", text="D_range", values=data, iid="dr" + str(i))

    data = []
    for i in range(len(init_data)):
        data.append(init_data[i][9])
    info_tree.insert('', "end", text="Path", values=data, iid="path" + str(i))

    # for i in range(3):
    #     info_tree.insert('', "end", text="X", values=init_data[i][0], iid="x" + str(i))
    # for i in range(3):
    #     info_tree.insert('', "end", text="Y", values=init_data[i][1], iid="y" + str(i))
    # for i in range(len(init_data)):
    #     info_tree.insert('', "end", text="Now_d", values=init_data[i][2], iid="nd" + str(i))
    # for i in range(len(init_data)):
    #     info_tree.insert('', "end", text="Total_d", values=init_data[i][3], iid="td" + str(i))
    # for i in range(len(init_data)):
    #     info_tree.insert('', "end", text="T1_d", values=init_data[i][4], iid="1d" + str(i))
    # for i in range(len(init_data)):
    #     info_tree.insert('', "end", text="T2_d", values=init_data[i][5], iid="2d" + str(i))
    # for i in range(len(init_data)):
    #     info_tree.insert('', "end", text="T3_d", values=init_data[i][6], iid="3d" + str(i))
    # for i in range(len(init_data)):
    #     info_tree.insert('', "end", text="Knot", values=init_data[i][7], iid="knot" + str(i))
    # for i in range(len(init_data)):
    #     info_tree.insert('', "end", text="D_range", values=init_data[i][8], iid="dr" + str(i))
    # for i in range(len(init_data)):
    #     info_tree.insert('', "end", text="Path", values=init_data[i][9], iid="path" + str(i))

    return info_tree

