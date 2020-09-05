import tkinter as tk
import copy
from PIL import Image, ImageTk
import math
import cv2

class Canvas:
    w = 0
    h = 0
    ratio = 0
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

    def __init__(self, frame, w, h, case, op_x, op_y):
        self.w = w
        self.h = h
        self.ratio = 10
        self.patrol_r = 7
        self.target_r = 7
        self.operation_x = op_x
        self.operation_y = op_y
        self.start_x = (self.w - op_x * self.ratio) / 2
        self.start_y = self.h / 2 + (op_y * self.ratio) / 2
        self.tCase = case
        self.init_target = copy.deepcopy(self.tCase.target)
        self.init_patrol = copy.deepcopy(self.tCase.patrol)
        self.init_count = 1
        self.init_total_time = copy.deepcopy(self.tCase.total_time)


        # detection_img = ImageTk.PhotoImage(Image.open('image/detection.png'))
        # self.tk_image_list.append(detection_img)
        # patrol_img_cv2 = cv2.imread("Image/patrol_img.png", cv2.IMREAD_UNCHANGED)
        # self.cv_image_list.append(patrol_img_cv2)

        self.patrol_img_tk = []
        self.target_img_tk = []
        self.detection_img = []
        self.c_operation_section = []
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

    def set_operation(self, x1, y1, x2, y2):
        t_x1, t_y1 = self.converse(x1, y1)
        t_x2, t_y2 = self.converse(x2, y2)

        line = self.canvas.create_line(t_x1, t_y1, t_x2, t_y1, dash=(4, 4), fill="#f5f5dc")
        self.c_operation_section.append(line)
        line = self.canvas.create_line(t_x2, t_y1, t_x2, t_y2, dash=(4, 4), fill="#f5f5dc")
        self.c_operation_section.append(line)
        line = self.canvas.create_line(t_x1, t_y2, t_x2, t_y2, dash=(4, 4), fill="#f5f5dc")
        self.c_operation_section.append(line)
        line = self.canvas.create_line(t_x1, t_y1, t_x1, t_y2, dash=(4, 4), fill="#f5f5dc")
        self.c_operation_section.append(line)

    def rotate_cv2(self, angle):
        height, width, channel = self.patrol_img_cv2.shape
        matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
        dst = cv2.warpAffine(self.patrol_img_cv2, matrix, (width, height))

        return dst

    def get_angle_position(self, x1, y1, x2, y2):
        angle = 360 - (math.atan2(y2 - y1, x2 - x1) * (180.0 / math.pi))
        return angle

    def converse_x(self, x):
        return self.start_x + (x*10)

    def converse_y(self, y):
        return self.start_y - (y*10)

    def converse(self, x, y):
        return self.start_x + (x * 10), self.start_y - (y * 10)

    def get_angle(self, p1, p2):
        dy = p2[1] - p1[1]
        dx = p2[0] - p1[0]
        dx, dy = self.converse(dx, dy)
        angle = math.atan(dy/dx) * (180/math.pi)

        if dx < 0:
            angle += 180
        else:
            if dy < 0:
                angle += 360

        return angle

    def init_draw_patrol(self, patrol, target):
        for i in range(len(patrol)):
            temp_x, temp_y = patrol[i].get_position()
            temp_x, temp_y = self.converse(temp_x, temp_y)
            d_img = ImageTk.PhotoImage(Image.open('image/detection.png'))
            self.detection_img.append(d_img)

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
                    line = self.canvas.create_line(x1, y1, x2, y2, width=2, dash=(2, 2), fill="#86c5e5")
                    self.c_patrol_path[idx].append(line)

            ## draw patrol
            t_x1, t_y1 = patrol[i].get_path_index(0)
            t_x1, t_y1 = self.converse(t_x1, t_y1)
            t_x2, t_y2 = patrol[i].get_path_index(1)
            t_x2, t_y2 = self.converse(t_x2, t_y2)

            src = cv2.imread("Image/patrol_img.png", cv2.IMREAD_UNCHANGED)
            height, width, no_channels = src.shape
            angle = (math.atan2(t_x2 - t_x1, t_y2 - t_y1) * (180.0 / math.pi)) - 180
            matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
            dst = cv2.warpAffine(src, matrix, (width, height))
            img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(img)
            self.patrol_img_tk.append(ImageTk.PhotoImage(image=img))
            temp_c = self.canvas.create_image(temp_x - self.patrol_r, temp_y - self.patrol_r,
                                              image=self.patrol_img_tk[i], anchor=tk.NW)
            self.c_patrol.append(temp_c)

            ## draw detection range
            temp_c = self.canvas.create_image(temp_x - (self.ratio * patrol[i].detection_dist),
                                              temp_y - (self.ratio * patrol[i].detection_dist),
                                              image=self.detection_img[i], anchor=tk.NW)
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
            # temp_c = self.canvas.create_oval(temp_x - self.target_r,
            #                                  temp_y - self.target_r,
            #                                  temp_x + self.target_r,
            #                                  temp_y + self.target_r, fill='red')
            t_x1, t_y1 = target[i].get_path_index(0)
            t_x1, t_y1 = self.converse(t_x1, t_y1)
            t_x2, t_y2 = target[i].get_path_index(1)
            t_x2, t_y2 = self.converse(t_x2, t_y2)
            print(t_x1, t_y1, t_x2, t_y2)

            src = cv2.imread("Image/target_img.png", cv2.IMREAD_UNCHANGED)
            height, width, no_channels = src.shape
            angle = (math.atan2(t_x2 - t_x1, t_y2 - t_y1) * (180.0 / math.pi)) - 180
            print(angle)
            matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
            dst = cv2.warpAffine(src, matrix, (width, height))
            img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(img)
            self.target_img_tk.append(ImageTk.PhotoImage(image=img))
            temp_c = self.canvas.create_image(temp_x - self.target_r, temp_y - self.target_r,
                                              image=self.target_img_tk[i], anchor=tk.NW)
            self.c_target.append(temp_c)

    def update_draw_target(self, target_tg):
        for i in range(len(self.tCase.target)):
            if target_tg[i]:
                temp_x, temp_y = self.tCase.target[i].get_position()
                temp_x, temp_y = self.converse(temp_x, temp_y)
                self.canvas.coords(self.c_target[i],
                                   temp_x - self.target_r,
                                   temp_y - self.target_r)

    def update_draw_patrol(self, res, patrol_tg, target_tg):
        for i in range(len(self.tCase.patrol)):
            temp_x, temp_y = self.tCase.patrol[i].get_position()
            temp_x, temp_y = self.converse(temp_x, temp_y)
            # self.canvas.coords(self.c_patrol[i],
            #                    temp_x - self.ship_r,
            #                    temp_y - self.ship_r,
            #                    temp_x + self.ship_r,
            #                    temp_y + self.ship_r)
            self.canvas.coords(self.c_patrol[i], temp_x - self.patrol_r, temp_y - self.patrol_r)
            self.canvas.coords(self.c_patrol_detection[i],
                               temp_x - (self.ratio * self.tCase.patrol[i].detection_dist),
                               temp_y - (self.ratio * self.tCase.patrol[i].detection_dist))

        ### draw detection line
        for i in range(len(self.tCase.patrol)):
            if patrol_tg[i]:
                for j in range(len(self.tCase.target)):
                    if not target_tg[j]: continue
                    if res[i][j] != -1:
                        # print("i : {}, j : {} >> {} ".format(i, j, res[i][j]))
                        x1, y1 = self.tCase.patrol[i].get_position()
                        x1, y1 = self.converse(x1, y1)
                        x2, y2 = self.tCase.target[j].get_position()
                        x2, y2 = self.converse(x2, y2)

                        self.canvas.delete(self.c_patrol_detection_l[i][j])
                        self.c_patrol_detection_l[i][j] = self.canvas.create_line(x1, y1, x2, y2,
                                                                                  arrow=tk.LAST, dash=(4, 2),
                                                                                  fill="white")
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
            self.canvas.coords(self.c_patrol[i],
                               temp_x - self.patrol_r, temp_y - self.patrol_r)
            self.canvas.coords(self.c_patrol_detection[i],
                               temp_x - (self.ratio * self.tCase.patrol[i].detection_dist),
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
                line = self.canvas.create_line(x1, y1, x2, y2, width=2, dash=(2, 2), fill="#86c5e5")
                self.c_patrol_path[i].append(line)


    def set_detection_range_img(self, patrol):
        for i in range(len(self.c_patrol_detection)):
            im_temp = Image.open('image/detection.png')
            n_pixel = self.ratio * patrol[i].detection_dist * 2
            im_temp = im_temp.resize((n_pixel, n_pixel), Image.ANTIALIAS)
            self.detection_img[i] = ImageTk.PhotoImage(im_temp)
            self.canvas.itemconfigure(self.c_patrol_detection[i], image=self.detection_img[i])


    def update_detection_range_img(self, event, ent, idx):
        im_temp = Image.open('image/detection.png')
        n_pixel = self.ratio * self.tCase.patrol[idx].detection_dist * 2

        print(self.tCase.patrol[idx].detection_dist)
        self.tCase.patrol[idx].detection_dist = int(ent.get())
        print(self.tCase.patrol[idx].detection_dist)

        im_temp = im_temp.resize((n_pixel, n_pixel), Image.ANTIALIAS)
        self.detection_img[idx] = ImageTk.PhotoImage(im_temp)
        self.canvas.itemconfigure(self.c_patrol_detection[idx], image=self.detection_img[idx])


    def patrol_changed_path(self, changed):
        for i in range(len(changed)):
            if changed[i] == 1:
                self.set_patrol_img(i)
                # p = self.tCase.patrol[i]
                # next_path_idx = (p.path_idx + 1) % p.num_path
                # now_path_idx = p.path_idx % p.num_path
                # t_x1, t_y1 = p.get_path_index(now_path_idx)
                # t_x1, t_y1 = self.converse(t_x1, t_y1)
                # t_x2, t_y2 = p.get_path_index(next_path_idx)
                # t_x2, t_y2 = self.converse(t_x2, t_y2)
                #
                # src = cv2.imread("Image/patrol_img.png", cv2.IMREAD_UNCHANGED)
                # height, width, no_channels = src.shape
                # angle = (math.atan2(t_x2 - t_x1, t_y2 - t_y1) * (180.0 / math.pi)) - 180
                # matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
                # dst = cv2.warpAffine(src, matrix, (width, height))
                # img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGBA)
                # img = Image.fromarray(img)
                # self.patrol_img_tk[i] = ImageTk.PhotoImage(image=img)
                # self.canvas.itemconfigure(self.c_patrol[i], image=self.patrol_img_tk[i])

    def set_patrol_img(self, patrol_i):
        p = self.tCase.patrol[patrol_i]
        next_path_idx = (p.path_idx + 1) % p.num_path
        now_path_idx = p.path_idx % p.num_path
        t_x1, t_y1 = p.get_path_index(now_path_idx)
        t_x1, t_y1 = self.converse(t_x1, t_y1)
        t_x2, t_y2 = p.get_path_index(next_path_idx)
        t_x2, t_y2 = self.converse(t_x2, t_y2)

        src = cv2.imread("Image/patrol_img.png", cv2.IMREAD_UNCHANGED)
        height, width, no_channels = src.shape
        angle = (math.atan2(t_x2 - t_x1, t_y2 - t_y1) * (180.0 / math.pi)) - 180
        matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
        dst = cv2.warpAffine(src, matrix, (width, height))
        img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(img)
        self.patrol_img_tk[patrol_i] = ImageTk.PhotoImage(image=img)
        self.canvas.itemconfigure(self.c_patrol[patrol_i], image=self.patrol_img_tk[patrol_i])

    def set_target_img(self, target_i):
        t = self.tCase.target[target_i]
        next_path_idx = 1
        now_path_idx = 0
        t_x1, t_y1 = t.get_path_index(now_path_idx)
        t_x1, t_y1 = self.converse(t_x1, t_y1)
        t_x2, t_y2 = t.get_path_index(next_path_idx)
        t_x2, t_y2 = self.converse(t_x2, t_y2)

        src = cv2.imread("Image/target_img.png", cv2.IMREAD_UNCHANGED)
        height, width, no_channels = src.shape
        angle = (math.atan2(t_x2 - t_x1, t_y2 - t_y1) * (180.0 / math.pi)) - 180
        matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
        dst = cv2.warpAffine(src, matrix, (width, height))
        img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(img)
        self.target_img_tk[target_i] = ImageTk.PhotoImage(image=img)
        self.canvas.itemconfigure(self.c_target[target_i], image=self.target_img_tk[target_i])

# def get_attributes(widget):
#     widg = widget
#     keys = widg.keys()
#     for key in keys:
#         print("Attribute: {:<20}".format(key), end=' ')
#         value = widg[key]
#         vtype = type(value)
#         print('Type: {:<30} Value: {}'.format(str(vtype), value))


class ResultText:
    def __init__(self, frame, w, h):
        self.data = []
        self.text = tk.Text(frame, width=w, height=h, relief="solid", padx=5, pady=5)
        self.text.config(state=tk.DISABLED)

