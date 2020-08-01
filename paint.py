# importing the required libraries 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt, QTimer
import Ship
import timeit
import sys 

class Demo(QWidget): 
	def __init__(self): 
		super().__init__() 
        self.resize(1200, 800)
        self.color = QColor(Qt.green)
        
        # self.drawShip = QRect(0,0,50,50)

		# # set the title 
		# self.setWindowTitle("Move") 

		# # setting the geometry of window 
		# self.setGeometry(0, 0, 400, 300) 

		# # creating a label widget 
		# self.widget = QLabel('Moved', self) 

		# # moving the widget 
		# # move(left, top) 
		# self.widget.move(50, 50)
    

		# show all the widgets 
		# self.show() 

        self.timer = QTimer(self)
        self.timer.setInterval(self, 100)
        self.timer.timeout.connect(self.updatePosition)
        self.timer.start()
        
    def drawShip(self, x, y):
        shipPainter = QPainter(self)
        shipPainter.setPan(QPen(Qt.green, 3, Qt.SolidLine))
        shipPainter.drawEllipse(x-3,y+3,6,6)
        
    def updatePosition(self, ship):
        cur_x, cur_y = ship.advance(2)
        drawShip(cur_x, cur_y)
        self.update()
    
    def detection(ship, target):
        dist = ship.distance(ship.getPosition(), target.getPosition)
        if dist <= 5 and timer == 0
            start_time = timeit_default_timer()
            timer = 1
            print("Dectection On", end='\n')
        elif dist > 5 and timer == 1
            end_time = timeit_default_timer()
            timer = 0
            print("Dectect time is {}".format(end_time-start_time), end='\n')
            print("Dectection Off", end='\n')
            


# create pyqt5 app 
App = QApplication(sys.argv) 


# create the instance of our Window
demo = Demo()
demo.show()

ship = Ship()
ship.set_speed(4)
ship.add_path(0, 0)
ship.add_path(0, 10)
ship.add_path(20, 10)
ship.add_path(20, 0)

target = Ship()
target.set_speed(5)
target.add_path(0, 20)
target.add_path(0, -40)

for _ in range(10):
    updatePosition(ship)
    updatePosition(target)
    detection(ship, target)


sys.exit(App.exec_())

## https://learndataanalysis.org/how-to-create-an-object-bouncing-effect-pyqt5-tutorial/