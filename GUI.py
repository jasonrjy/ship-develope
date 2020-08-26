import tkinter as tk
import copy
from PIL import Image, ImageTk

class Canvas:
    w = 0
    h = 0
    ratio = 0
    ship_r = 0
    start_x = 0
    start_y = 0
    c_patrol = []
    c_patrol_detection = []
    c_patrol_detection_l = []
    c_patrol_path = []
    c_target = []
    tCase = None
    init_target = None
    init_patrol = None
    init_count = 1
    init_total_time = 0
    img = None

    def __init__(self, frame, w, h, case):
        self.w = w
        self.h = h
        self.ratio = 10
        self.ship_r = 5
        self.start_x = (self.w - 20 * self.ratio) / 2
        self.start_y = self.h / 2 + (10 * self.ratio) / 2
        self.tCase = case
        self.init_target = copy.deepcopy(self.tCase.target)
        self.init_patrol = copy.deepcopy(self.tCase.patrol)
        self.init_count = 1
        self.init_total_time = copy.deepcopy(self.tCase.total_time)
        self.img = ImageTk.PhotoImage(Image.open('detection.png'))
        self.images = []

        self.c_patrol_path = []

        self.canvas = tk.Canvas(frame, width=w, height=h, bg="black", relief="solid")
        # op_x1 = 0
        # op_x2 = 20
        # op_y1 = 0
        # op_y2 = 10
        # op_x1, op_y1 = self.converse(op_x1, op_y1)
        # op_x2, op_y2 = self.converse(op_x2, op_y2)
        # # self.canvas.create_rectangle(op_x1, op_y1, op_x2, op_y2, fill="#d3d3d3")
        self.canvas.pack()

    def converse_x(self, x):
        return self.start_x + (x*10)

    def converse_y(self, y):
        return self.start_y - (y*10)

    def converse(self, x, y):
        return self.start_x + (x * 10), self.start_y - (y * 10)

    def init_draw_patrol(self, patrol, target):
        for i in range(len(patrol)):
            temp_x, temp_y = patrol[i].get_position()
            temp_x, temp_y = self.converse(temp_x, temp_y)
            self.images.append(self.img)
            # print("oooorigin w = {}, h = {}".format(self.images[i].width(), self.images[i].height()))

            ## draw path
            idx = -1
            for p in patrol:
                cur_path = p.get_path()
                num = len(cur_path) - 1
                idx += 1
                self.c_patrol_path.append([])
                for j in range(num):
                    x1 = self.converse_x(cur_path[j][0])
                    y1 = self.converse_y(cur_path[j][1])
                    x2 = self.converse_x(cur_path[j + 1][0])
                    y2 = self.converse_y(cur_path[j + 1][1])
                    line = self.canvas.create_line(x1, y1, x2, y2, dash=(2, 2), fill="#86c5e5")
                    self.c_patrol_path[idx].append(line)
            ## draw patrol
            temp_c = self.canvas.create_oval(temp_x - self.ship_r, temp_y - self.ship_r, temp_x + self.ship_r, temp_y + self.ship_r,
                                        fill='green', outline="green")
            self.c_patrol.append(temp_c)
            ## draw detection range
            temp_c = self.canvas.create_image(temp_x - (self.ratio * patrol[i].detection_dist),
                                         temp_y - (self.ratio * patrol[i].detection_dist), image=self.images[i], anchor=tk.NW)
            self.c_patrol_detection.append(temp_c)

        for i in range(len(patrol)):
            self.c_patrol_detection_l.append([])
            for j in range(len(target)):
                self.c_patrol_detection_l[i].append([])

    def init_draw_target(self, target):
        for i in range(len(self.tCase.target)):
            temp_x, temp_y = self.tCase.target[i].get_position()
            temp_x, temp_y = self.converse(temp_x, temp_y)
            ## draw target
            temp_c = self.canvas.create_oval(temp_x - self.ship_r, temp_y - self.ship_r, temp_x + self.ship_r, temp_y + self.ship_r, fill='red')
            self.c_target.append(temp_c)

    def update_draw_target(self):
        for i in range(len(self.tCase.target)):
            temp_x, temp_y = self.tCase.target[i].get_position()
            temp_x, temp_y = self.converse(temp_x, temp_y)
            self.canvas.coords(self.c_target[i], temp_x - self.ship_r, temp_y - self.ship_r, temp_x + self.ship_r, temp_y + self.ship_r)

    def update_draw_patrol(self, res):
        for i in range(len(self.tCase.patrol)):
            temp_x, temp_y = self.tCase.patrol[i].get_position()
            temp_x, temp_y = self.converse(temp_x, temp_y)
            self.canvas.coords(self.c_patrol[i], temp_x - self.ship_r, temp_y - self.ship_r, temp_x + self.ship_r, temp_y + self.ship_r)
            self.canvas.coords(self.c_patrol_detection[i], temp_x - (self.ratio * self.tCase.patrol[i].detection_dist), temp_y - (self.ratio * self.tCase.patrol[i].detection_dist))

        ### draw detection line
        for i in range(len(self.tCase.patrol)):
            for j in range(len(self.tCase.target)):
                if res[i][j] != -1:
                    # print("i : {}, j : {} >> {} ".format(i, j, res[i][j]))
                    x1, y1 = self.tCase.patrol[i].get_position()
                    x1, y1 = self.converse(x1, y1)
                    x2, y2 = self.tCase.target[j].get_position()
                    x2, y2 = self.converse(x2, y2)

                    self.canvas.delete(self.c_patrol_detection_l[i][j])
                    self.c_patrol_detection_l[i][j] = self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, dash=(4, 2), fill="white")
                else:
                    self.canvas.delete(self.c_patrol_detection_l[i][j])

    def update_init_draw_patrol(self):

        for i in range(len(self.c_patrol_path)):
            for j in range(len(self.c_patrol_path[i])):
                self.canvas.delete(self.c_patrol_path[i][j])
        self.c_patrol_path = []

        for i in range(len(self.tCase.patrol)):
            temp_x, temp_y = self.tCase.patrol[i].get_position()
            temp_x, temp_y = self.converse(temp_x, temp_y)
            self.canvas.coords(self.c_patrol[i], temp_x - self.ship_r, temp_y - self.ship_r, temp_x + self.ship_r,
                               temp_y + self.ship_r)
            self.canvas.coords(self.c_patrol_detection[i], temp_x - (self.ratio * self.tCase.patrol[i].detection_dist),
                               temp_y - (self.ratio * self.tCase.patrol[i].detection_dist))

            cur_path = self.tCase.patrol[i].get_path()
            num = len(cur_path) - 1
            self.c_patrol_path.append([])
            ## draw path
            for j in range(num):
                x1 = self.converse_x(cur_path[j][0])
                y1 = self.converse_y(cur_path[j][1])
                x2 = self.converse_x(cur_path[j + 1][0])
                y2 = self.converse_y(cur_path[j + 1][1])
                line = self.canvas.create_line(x1, y1, x2, y2, dash=(2, 2), fill="green")
                self.c_patrol_path[i].append(line)


    def set_detection_range_img(self, patrol):
        for i in range(len(self.c_patrol_detection)):
            im_temp = Image.open('detection.png')
            n_pixel = self.ratio * patrol[i].detection_dist * 2
            im_temp = im_temp.resize((n_pixel, n_pixel), Image.ANTIALIAS)
            self.images[i] = ImageTk.PhotoImage(im_temp)
            self.canvas.itemconfigure(self.c_patrol_detection[i], image=self.images[i])


class ResultText:
    def __init__(self, frame, w, h):
        self.data = []
        self.text = tk.Text(frame, width=w, height=h, relief="solid", padx=5, pady=5)

