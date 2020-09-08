from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

class Matplot:
    def __init__(self, frame):
        self.detection_time_data = [[], [], []]
        self.time = 0
        self.frame = frame
        self.plt = pyplot

    def append_detection_time(self, data):
        dtime = self.detection_time_data
        length = len(self.detection_time_data[0])

        # print(data)
        for d in range(len(data)):
            dtime[d] = dtime[d] + data[d]
        self.time += len(data[0])

        print(self.time)

        if (self.time >= 100):
            self.func.notebook_active()
            self.set_plt()

    def set_func(self, func):
        self.func = func

    def set_plt(self):
        dtime = self.detection_time_data
        # self.plt.plot([i + 1 for i in range(self.time)], dtime[0])
        # self.plt.plot([i + 1 for i in range(self.time)], dtime[1])
        # self.plt.plot([i + 1 for i in range(self.time)], dtime[2])
        # self.plt.xlabel('Time')
        # self.plt.ylabel('Detection_Time(min)')
        # self.plt.title('탐지 시간 그래프')
        # self.plt.legend(['Patrol 1', 'Patrol 2', 'Patrol 3'])

        figure = self.plt.Figure(figsize=(25, 5), dpi=100)
        plot1 = figure.add_subplot(111)
        # line = FigureCanvasTkAgg(figure, self.frame)
        # line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        plot1.plot(dtime[0], label='Patrol_1')
        plot1.plot(dtime[1], label='Patrol_2')
        plot1.plot(dtime[2], label='Patrol_3')
        # plot1.xlabel('Time')
        # plot1.ylabel('Detection_Time(min)')
        # plot1.title('탐지 시간 그래프')
        # plot1.legend(['Patrol 1', 'Patrol 2', 'Patrol 3'])


        canvas = FigureCanvasTkAgg(figure, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        toolbar = NavigationToolbar2Tk(canvas, self.frame)
        toolbar.update()
        canvas.get_tk_widget().pack()


        # df2 = df2[['Year', 'Unemployment_Rate']].groupby('Year').sum()
        # df2.plot(kind='line', legend=True, ax=ax2, color='r', marker='o', fontsize=10)
        # ax2.set_title('Year Vs. Unemployment Rate')
