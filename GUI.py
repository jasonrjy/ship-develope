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

        self.canvas = tk.Canvas(frame, width=w, height=h, bg="white")
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

            ## draw path
            for p in patrol:
                cur_path = p.get_path()
                num = len(cur_path) - 1
                for j in range(num):
                    x1 = self.converse_x(cur_path[j][0])
                    y1 = self.converse_y(cur_path[j][1])
                    x2 = self.converse_x(cur_path[j + 1][0])
                    y2 = self.converse_y(cur_path[j + 1][1])
                    self.canvas.create_line(x1, y1, x2, y2, dash=(2, 2), fill="green")
            ## draw patrol
            temp_c = self.canvas.create_oval(temp_x - self.ship_r, temp_y - self.ship_r, temp_x + self.ship_r, temp_y + self.ship_r,
                                        fill='green')
            self.c_patrol.append(temp_c)
            ## draw detection range
            temp_c = self.canvas.create_image(temp_x - (self.ratio * patrol[i].detection_dist),
                                         temp_y - (self.ratio * patrol[i].detection_dist), image=self.img, anchor=tk.NW)
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
            self.canvas.coords(self.c_patrol_detection[i], temp_x - (self.ratio * 5), temp_y - (self.ratio * 5))

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
                    self.c_patrol_detection_l[i][j] = self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, dash=(4, 2))
                else:
                    self.canvas.delete(self.c_patrol_detection_l[i][j])
