import tkinter


class test:
    def __init__(self):
        self.c_x = 0

    def hi(self, x):
        x = self.c_x
        x += 1


t = test()
print(t.c_x)
t.hi(t.c_x)
print(t.c_x)