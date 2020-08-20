import ship
import sys
import os
import copy
import re
import random
from tkinter import *


class testCase():
    def __init__(self):
        self.patrol = []
        self.target = []
        self.time = 1
        self.accum_t = 0
        self.accel = 60
        self.total_accum_t = []
        self.total_time = 0
        self.accum_time = []
        self.ftime = []

    def get_all_position(self):
        data = []
        for ele in self.patrol:
            t_data = ele.get_position()
            data.append(t_data)
        return data

    def update_time(self):
        ## coordinate change after self.time

        detect = [[0 for col in range(len(self.patrol))] for row in range(len(self.target))]

        for i in range(len(self.patrol)):
            self.patrol[i].advance(self.time)
        #   print("Patrol {} Position at time {} is".format(i, self.patrol[i].time), end=' ')
        #   print(" {0} {1}".format(self.patrol[i].x, self.patrol[i].y), end='\n')
        # print("\n")
        for j in range(len(self.target)):
            self.target[j].advance(self.time)
        #   print("Target {} Position at time {} is".format(j, self.target[j].time), end=' ')
        #   print(" {0} {1}".format(self.target[j].x, self.target[j].y), end='\n')
        # print("---------------------------------------")

        # for i in range(len(self.patrol)):
        #     find = 0
        #     for j in range(len(self.target)):
        #         bool, dist = self.patrol[i].detection(self.target[j])
        #         if dist <= self.patrol[i].detection_dist:
        #             detect[i][j] = dist
        #             find += 1
        #             self.accum_time[i][j] += self.time
        #             # print("-------------------------- {} {}, dist is {}".format(i,j, dist))
        #             if self.ftime[i][j] == -1:
        #                 self.ftime[i][j] = self.accum_t
        #                 # print("{} {} first find".format(i,j))
        #         else:
        #             # print("{} {} dist = {} NO!!!".format(i, j, dist))
        #             # print("\n")
        #             detect[i][j] = -1
        #     if find > 0:
        #         self.total_accum_t[i] += self.time
        #         # print("find num = {}\n".format(find))

        for i in range(len(self.patrol)):
            find = 0
            for j in range(len(self.target)):
                dist = ship.distance(self.patrol[i].get_position(), self.target[j].get_position())
                if dist <= self.patrol[i].detection_dist:
                    detect[i][j] = dist
                    find += 1
                    self.accum_time[i][j] += self.time
                    # print("-------------------------- {} {}, dist is {}".format(i,j, dist))
                    if self.ftime[i][j] == -1:
                        self.ftime[i][j] = self.accum_t
                        # print("{} {} first find".format(i,j))
                else:
                    # print("{} {} dist = {} NO!!!".format(i, j, dist))
                    # print("\n")
                    detect[i][j] = -1
            if find > 0:
                self.total_accum_t[i] += self.time
                # print("find num = {}\n".format(find))

        return detect

    def set_rand_unit(self, p, tt):
        self.patrol = p
        self.target = self.set_rand_target(tt)

        for i in range(len(self.patrol)):
            self.accum_time.append([])
            for j in range(len(self.target)):
                self.accum_time[i].append(0)

        for i in range(len(self.patrol)):
            self.ftime.append([])
            for j in range(len(self.target)):
                self.ftime[i].append(-1)

        for i in range(len(self.patrol)):
            self.total_accum_t.append(0)

    def set_fixed_unit(self, p, t):
        self.patrol = p
        self.target = t

        for i in range(len(self.patrol)):
            self.accum_time.append([])
            for j in range(len(self.target)):
                self.accum_time[i].append(0)

        for i in range(len(self.patrol)):
            self.ftime.append([])
            for j in range(len(self.target)):
                self.ftime[i].append(-1)

        for i in range(len(self.patrol)):
            self.total_accum_t.append(0)

    def set_total_time(self, tt):
        self.total_time = tt

    def set_rand_target(self, tt):
        ### setting random target point
        target = []
        for i in range(3):
            a = ship.LineUnit()

            ran = random.randint(0, 4)
            if ran == 0:
                sx = random.randint(-20, 0)
                sy = random.randint(10, 20)
            elif ran == 1:
                sx = random.randint(0, 20)
                sy = random.randint(10, 20)
            elif ran == 2:
                sx = random.randint(20, 40)
                sy = random.randint(10, 20)
            elif ran == 3:
                sx = random.randint(-20, 0)
                sy = random.randint(0, 10)
            elif ran == 4:
                sx = random.randint(20, 40)
                sy = random.randint(0, 10)

            rx = random.randint(0, 20)
            ry = random.randint(0, 10)

            dy = ry - sy
            dx = rx - sx
            if dy > 0:
                n = (40 - sy) / dy
                ey = 40
                ex = sx + n * dx
            elif dy < 0:
                n = (-40 - sy) / dy
                ey = -40
                ex = sx + n * dx
            ## dy == 0 and ry == 10
            elif ry == 5:
                ry = 8
                dy = ry - sy
                if dy > 0:
                    n = (40 - sy) / dy
                    ey = 40
                    ex = sx + n * dx
                elif dy < 0:
                    n = (-40 - sy) / dy
                    ey = -40
                    ex = sx + n * dx
            ## dy == 0 and ry != 10
            else:
                ry = 10
                dy = ry - sy
                if dy > 0:
                    n = (40 - sy) / dy
                    ey = 40
                    ex = sx + n * dx
                elif dy < 0:
                    n = (-40 - sy) / dy
                    ey = -40
                    ex = sx + n * dx

            target_knot = random.randint(10, 15)

            a.set_knot(target_knot)
            a.add_path(sx, sy)
            a.add_path(ex, ey)
            a.set_delay(random.randint(0, tt / 4))

            target.append(a)

        return target

    def get_target(self):
        return self.target


def run_rand_case(tt, p):
    case = testCase()
    case.set_rand_unit(p, tt)
    case.set_total_time(tt)

    print("\n\nIf targets are this coordinate\n")
    for i in range(len(case.target)):
        print(" target {} >> x = {}, y = {}".format(i, case.target[i].path[0][0], case.target[i].path[0][1]))

    while case.accum_t < case.total_time:
        case.update_time()
        case.accum_t += case.time

    for i in range(len(case.patrol)):
        print("Patrol {}'s detectioin".format(i))
        print(" total detection time = {}".format(case.total_accum_t[i]))
        for j in range(len(case.target)):
            print("  target {} : {}, ftime = {}".format(j, case.accum_time[i][j], case.ftime[i][j]), end='\n')

    res = []
    res_t = case.get_target()
    for i in range(len(case.patrol)):
        res.append(case.total_accum_t[i])

    return res, res_t


def run_fixed_case(tt, p, t):
    case = testCase()
    case.set_fixed_unit(p, t)
    case.set_total_time(tt)

    # print("\n\nIf targets are this fixed coordinate")
    # for i in range(len(case.target)):
    #   print(" target {} >> x = {}, y = {}".format(i,case.target[i].path[0][0], case.target[i].path[0][1]))
    # print("\n")

    while case.accum_t < case.total_time:
        case.update_time()
        # for i in range(3):
        #   print("target {} ".format(i), end='')
        #   case.target[i].print_position()
        case.accum_t += case.time

    for i in range(len(case.patrol)):
        print("{} 번 경로의 탐지 결과".format(i + 1))
        print(" 총 탐지 시간 = {} 분".format(case.total_accum_t[i]))
        for j in range(len(case.target)):
            print("  target {} : 첫 발견 시간 = {} 분, 탐지 시간 = {} 분".format(j + 1, case.ftime[i][j], case.accum_time[i][j]),
                  end='\n')
        print("\n")
    res = []
    res_t = case.get_target()
    for i in range(len(case.patrol)):
        res.append(case.total_accum_t[i])

    return res, res_t



def cal_case(tt, cnt, p, t):
    max_detection_time = []
    accum_detection_time = []
    find_count = [0, 0, 0]
    max_target_list = []

    # ### run rand case
    run_p = copy.deepcopy(p)
    case_res, case_target = run_rand_case(tt, run_p)

    for i in range(3):
        max_detection_time.append(case_res[i])
        accum_detection_time.append(case_res[i])
        max_target_list.append(case_target)
        if case_res[i] > 0:
            find_count[i] += 1

    for i in range(cnt - 1):
        run_p = copy.deepcopy(p)
        case_res, case_target = run_rand_case(tt, run_p)

        for j in range(3):
            if (case_res[j] >= max_detection_time[j]):
                max_detection_time[j] = case_res[j]
                max_target_list[j] = case_target
            accum_detection_time[j] += case_res[j]
            if case_res[j] > 0:
                find_count[j] += 1

    ### print option
    print("\n--------------------------\n\n총 탐색 시간 : {} 분".format(int(tt)))
    print("탐색 속력 : {} Knot\n\n--------------------------\n".format(p[0].knot))

    #  run fixed case with print
    run_p = copy.deepcopy(p)
    run_t = copy.deepcopy(t)
    print("고정된 Target 실행 결과")
    case_res, case_target = run_fixed_case(tt, run_p, run_t)

    #### print part
    print("--------------------------\n\n{} 번의 임의 실행 결과\n".format(cnt))
    # for i in range(3):
    #   print("{}번이 최대 접촉할 때의 target 좌표".format(i+1))
    #   for j in range(3):
    #     print(" target {} >> x = {}, y = {}".format(j+1,max_target_list[i][j].path[0][0], max_target_list[i][j].path[0][1]))
    #   print("\n")
    for i in range(3):
        tmp = int((100 * accum_detection_time[i] / cnt) / int(tt))
        print("{}번 경로\n 최대 접촉 시간 : {}".format(i + 1, max_detection_time[i]))
        print(" {} 번 탐지 횟수 : {} / {} 회, 평균 접촉 시간 : {} 분 -> 탐지율 : {} %\n".format(i + 1, cnt, find_count[i],
                                                                                accum_detection_time[i] / cnt, tmp))


def readFile():
    file = open("./data/사전 데이터 입력.txt", 'r', encoding="utf-8")

    patrol = []
    target = []

    for i in range(3):
        a = ship.CycleUnit()
        patrol.append(a)
        b = ship.LineUnit()
        target.append(b)

    temp = file.readline()
    total_time = re.split(': ', temp)[1]
    total_time = float(total_time)

    temp = file.readline()
    count = re.split(': ', temp)[1]
    count = int(count)

    ### setting patrol
    for i in range(3):
        desc = file.readline()

        temp = file.readline()
        knot = re.split(': ', temp)[1]

        temp = file.readline()
        path_line = re.split(': ', temp)[1]
        temp = file.readline()
        detect_dist = re.split(': ', temp)[1]

        patrol[i].set_knot(int(knot))
        path = re.split('; |, ', path_line)
        size = int(len(path) / 2)
        for j in range(size):
            patrol[i].add_path(int(path[j * 2]), int(path[j * 2 + 1]))
            # print("path {} {}".format(path[j * 2], path[j*2 + 1]))
        patrol[i].set_detection(int(detect_dist))

    ## setting target
    for i in range(3):
        desc = file.readline()

        temp = file.readline()
        knot = re.split(': ', temp)[1]

        temp = file.readline()
        path_line = re.split(': ', temp)[1]

        target[i].set_knot(int(knot))
        path = re.split('; |, ', path_line)
        size = int(len(path) / 2)
        for j in range(size):
            target[i].add_path(int(path[j * 2]), int(path[j * 2 + 1]))
            # print("path {} {}".format(path[j * 2], path[j*2 + 1]))
        # target[i].set_delay(random.randint(0,10))

    return total_time, count, patrol, target

if __name__ == "__main__":
    print("함정 탐지 시뮬레이션")

    k = input("\n\n시작하시려면 아무 키나 누르십시오...")
    total_time, count, patrol, target = readFile()
    cal_case(total_time, count, patrol, target)
    #
    # test_read()
    k = input("\nPress close to exit")

    # window = Tk()
    # window.title("Ship Detection Program")
    # window.resizable(0, 0)
    # canvas = Canvas(window, width=640, height=640, bg="white")
    # canvas.pack()
    #
    # canvas_start_x = 50
    # canvas_start_y = 50
    # canvas_x = 300
    # canvas_y = 300
    #
    # window.mainloop()