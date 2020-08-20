import tkinter as tk
import copy
import GUI

class typeCheck:
    tCase = None
    init_target = None
    bbsType = None
    bbsLbl = None
    bbsGraphic = None
    bbsResult = None
    targetType = None
    rdioF = None
    rdioR = None

    def __init__(self, frame, tCase, init_target, info_table, BBS):
        self.tCase = tCase
        self.init_target = init_target
        self.info_t = info_table
        self.bbs = BBS
        self.initialize(frame)

    def initialize(self, frame):
        ## Check Graphic or Exe result
        self.bbsType = tk.IntVar()
        self.bbsLbl = tk.Label(frame, text="프로그램 유형 선택 : ")
        self.bbsGraphic = tk.Radiobutton(frame, text="그래픽", variable=self.bbsType, value=1)
        self.bbsGraphic.select()
        self.bbsGraphic.invoke()
        self.bbsResult = tk.Radiobutton(frame, text="실행 결과", variable=self.bbsType, value=2)

        self.bbsLbl.grid(row=0, column=0)
        self.bbsGraphic.grid(row=0, column=1)
        self.bbsResult.grid(row=0, column=2)

        ## Graphic > Check F or R
        self.targetType = tk.IntVar()
        self.rdioLbl = tk.Label(frame, text="Select Target Type : ")
        self.rdioF = tk.Radiobutton(frame, text="Fixed", variable=self.targetType, value=1)
        self.rdioR = tk.Radiobutton(frame, text="Random", variable=self.targetType, value=2)

        self.rdioLbl.grid(row=1, column=0)
        self.rdioF.grid(row=1, column=1)
        self.rdioR.grid(row=1, column=2)
        self.rdioF.select()

        ## Result > Entry count
        self.countVal = tk.IntVar()
        self.countEntry = tk.Entry(frame,  width=10, textvariable=self.countVal, justify='center')
        self.printStr = tk.Label(frame, text=" 회")
        self.countVal.set(1)

        self.bbsGraphic.config(command=self.bbsSelectG)
        self.bbsResult.config(command=self.bbsSelectR)
        self.rdioF.config(command=self.RdiotoFixed)
        self.rdioR.config(command=self.RdiotoRandom)



    def RdiotoFixed(self):
        self.tCase.target = copy.deepcopy(self.init_target)
        for t in self.tCase.target:
            print("x = {}, y = {}, delay = {}".format(t.x, t.y, t.delay))

    def RdiotoRandom(self):
        self.tCase.target = self.tCase.set_rand_target(self.tCase.total_time)
        for t in self.tCase.target:
            print("x = {}, y = {}, delay = {}".format(t.x, t.y, t.delay))

    def bbsSelectG(self):
        self.rdioLbl.grid(row=1, column=0)
        self.rdioF.grid(row=1, column=1)
        self.rdioR.grid(row=1, column=2)
        self.rdioF.select()
        self.rdioF.invoke()

        self.countEntry.grid_forget()
        self.printStr.grid_forget()

    def bbsSelectR(self):
        self.rdioLbl.grid_forget()
        self.rdioF.grid_forget()
        self.rdioR.grid_forget()

        self.countEntry.grid(row=1, column=1,sticky=tk.E)
        self.printStr.grid(row=1, column=2, sticky=tk.W)