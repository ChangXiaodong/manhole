from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from array import array
import time
import random
import threading


X_MINUTES = 1
Y_MAX = 65535
Y_MIN = 1
INTERVAL = 0.05
MAXCOUNTER = 100


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax.legend()
        self.ax.set_ylim(Y_MIN, Y_MAX)
        self.curveObj = None
        self.x_line, = self.ax.plot([], [], 'b', lw=2)
        self.y_line, = self.ax.plot([], [], 'r', lw=2)
        self.z_line, = self.ax.plot([], [], 'g', lw=2)

    def plot(self, x_value, y_value, z_value, count):
        self.x_line.set_data(count, x_value)
        self.y_line.set_data(count, y_value)
        self.z_line.set_data(count, z_value)
        self.ax.set_xlim(count[0], count[-1])
        ticklabels = self.ax.xaxis.get_ticklabels()
        for tick in ticklabels:
            tick.set_rotation(25)

        self.draw()


class MplCanvasWrapper(QtGui.QWidget):
    def __init__(self, parent=None,x_line_array=[],y_line_array=[],z_line_array=[]):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.frame_count_array = []
        self.x_line_array = x_line_array
        self.y_line_array = y_line_array
        self.z_line_array = z_line_array
        self.initDataGenerator()
        self.frame_count = 0

    def startPlot(self):
        self.__generating = True

    def pausePlot(self):
        self.__generating = False
        pass

    def initDataGenerator(self):
        self.__generating = False
        self.__exit = False
        self.tData = threading.Thread(name="dataGenerator", target=self.generateData)
        self.tData.start()

    def releasePlot(self):
        self.__exit = True
        self.tData.join()

    def generateData(self):
        counter = 0
        while (True):
            if self.__exit:
                break
            if self.__generating:
                self.frame_count += 1
                self.frame_count_array.append(self.frame_count)
                self.x_line_array.append(random.randint(Y_MIN, Y_MAX))
                self.y_line_array.append(random.randint(Y_MIN, Y_MAX))
                self.z_line_array.append(random.randint(Y_MIN, Y_MAX))

                self.canvas.plot(
                    self.x_line_array,
                    self.y_line_array,
                    self.z_line_array,
                    self.frame_count_array
                )
                if counter >= MAXCOUNTER:
                    self.x_line_array.pop(0)
                    self.y_line_array.pop(0)
                    self.z_line_array.pop(0)
                    self.frame_count_array.pop(0)
                else:
                    counter += 1
            time.sleep(INTERVAL)