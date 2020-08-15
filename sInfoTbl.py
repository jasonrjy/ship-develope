from tkinter import *

## reference https://www.geeksforgeeks.org/create-table-using-tkinter/
class Table:
    # def __init__(self, root):
    #
    #     # code for creating table
    #     for i in range(total_rows):
    #         for j in range(total_columns):
    #             self.e = Entry(root, width=20, fg='blue',
    #                            font=('Arial', 8, 'bold'))
    #
    #             self.e.grid(row=i, column=j)
    #             self.e.insert(END, lst[i][j])
    #
    #         # take the data

    def __init__(self, frame, data):
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
                    self.e = Label(frame, text="", width=10, bg="white")
                    self.e.grid(row=i, column=j)
                ## heading
                elif i == 0:
                    str_h = "Patrol"+str(j)
                    self.e = Label(frame, text=str_h, width=10, bg="white")
                    self.e.grid(row=i, column=j)
                ## property
                elif j == 0:
                    self.e = Label(frame, text=property_data[i-1], width=10, bg="white")
                    self.e.grid(row=i, column=j)
                ## data
                else:
                    sv = StringVar()
                    sv.set(data[j - 1][i - 1])
                    self.data_t[i-1].append(sv)
                    # print("i = {}, j = {}".format(i, j))
                    # print(data_t[i-1][j-1])
                    self.e = Label(frame, textvariable=self.data_t[i-1][j-1], width=10, bg="white")
                    self.e.grid(row=i, column=j)

    def update_position(self, edit):
        print(self.data_t)
        print(edit)
        for i in range(len(self.data_t[0])):
            for j in range(2):
                data = round(edit[i][j], 2)
                self.data_t[j][i].set(data)




