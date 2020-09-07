import tkinter as tk
import copy
import GUI

class typeCheck:
    tCase = None
    bbsType = None
    bbsLbl = None
    targetType = None
    rdioF = None
    rdioR = None

    def __init__(self, frame, tCase, info_table):
        self.tCase = tCase
        self.info_t = info_table
        self.initialize(frame)

    def initialize(self, frame):
        ## Check Graphic or Exe result
        # self.bbsType = tk.IntVar()
        # self.bbsLbl = tk.Label(frame, text="프로그램 유형 선택 : ")
        # self.bbsGraphic = tk.Radiobutton(frame, text="그래픽", variable=self.bbsType, value=1)
        # self.bbsGraphic.select()
        # self.bbsGraphic.invoke()
        # self.bbsResult = tk.Radiobutton(frame, text="실행 결과", variable=self.bbsType, value=2)

        ## Graphic > Check F or R
        self.targetType = tk.IntVar()
        self.rdioLbl = tk.Label(frame, text="Select Target Type : ", bg="white", padx=5, pady=5)
        self.rdioF = tk.Radiobutton(frame, text="Fixed", variable=self.targetType, value=1, bg="white", padx=5, pady=5)
        self.rdioR = tk.Radiobutton(frame, text="Random", variable=self.targetType, value=2, bg="white", padx=5, pady=5)

        self.rdioLbl.grid(row=1, column=0)
        self.rdioF.grid(row=1, column=1)
        self.rdioR.grid(row=1, column=2)
        self.rdioF.select()

        ## Result > Entry count
        self.countVal = tk.IntVar()
        self.countEntry = tk.Entry(frame,  width=10, textvariable=self.countVal, justify='center')
        vcmd = frame.register(self.callback)
        self.countEntry.config(validate='all', validatecommand=(vcmd, '%P'))
        self.printStr = tk.Label(frame, text=" 회")
        self.countVal.set(1)

        # self.bbsGraphic.config(command=self.bbsSelectG)
        # self.bbsResult.config(command=self.bbsSelectR)
        self.rdioF.config(command=self.RdiotoFixed)
        self.rdioR.config(command=self.RdiotoRandom)



    def RdiotoFixed(self):
        self.tCase.target = copy.deepcopy(self.tCase.init.target)
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

        self.bbs[1].text.pack_forget()
        self.bbs[0].canvas.pack()


    def bbsSelectR(self):
        self.rdioLbl.grid_forget()
        self.rdioF.grid_forget()
        self.rdioR.grid_forget()

        self.countEntry.grid(row=1, column=1,sticky=tk.E)
        self.printStr.grid(row=1, column=2, sticky=tk.W)

        print(self.bbs[0].canvas)
        self.bbs[0].canvas.pack_forget()
        self.bbs[1].text.pack()

    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False