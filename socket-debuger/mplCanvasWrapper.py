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
INTERVAL = 0.01


class MplCanvas(FigureCanvas):
    def __init__(self,lengend="", clear_line=None):
        self.clear_line = clear_line
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.x_line, = self.ax.plot([], [], 'b', lw=2, label=lengend+"-x")
        self.y_line, = self.ax.plot([], [], 'r', lw=2, label=lengend+"-y")
        self.z_line, = self.ax.plot([], [], 'g', lw=2, label=lengend+"-z")
        self.ax.legend(loc="upper left")
        self.ax.set_ylim(Y_MIN, Y_MAX)


    def plot(self, x_value, y_value, z_value, count):
        self.x_line.set_data(count, x_value)
        self.y_line.set_data(count, y_value)
        self.z_line.set_data(count, z_value)
        self.ax.set_xlim(count[0], count[-1])
        try:
            self.draw()
        except RuntimeError:
            self.clear_line()
            self.ax.set_xlim(0, 100)




class MplCanvasWrapper(QtGui.QWidget):
    def __init__(self, parent=None,x_line_array=[],y_line_array=[],z_line_array=[],legend=""):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas(legend, self.clearLineData)
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.frame_count_array = []
        self.x_line_array = x_line_array
        self.y_line_array = y_line_array
        self.z_line_array = z_line_array
        self.initDataGenerator()
        self.frame_count = 0
        self.max_array_length = 80

    def setMaxArrayLength(self, value):
        self.max_array_length = value

    def startPlot(self):
        self.__generating = True

    def pausePlot(self):
        self.__generating = False
        pass

    def initDataGenerator(self):
        self.__generating = False
        self.__exit = False
        self.tData = threading.Thread(
            name="updateFigure",
            target=self.updateFigure
        )
        self.tData.setDaemon(True)
        self.tData.start()

    def releasePlot(self):
        self.__exit = True
        self.tData.join()

    def updateFigure(self):
        while (True):
            if self.__exit:
                break
            if self.__generating:
                while self.frame_count != len(self.frame_count_array):
                    self.canvas.plot(
                        self.x_line_array,
                        self.y_line_array,
                        self.z_line_array,
                        self.frame_count_array
                    )
                    while len(self.x_line_array) >= self.max_array_length:
                        self.x_line_array.pop(0)
                        self.y_line_array.pop(0)
                        self.z_line_array.pop(0)
                        self.frame_count_array.pop(0)
                    self.frame_count = len(self.frame_count_array)

            time.sleep(INTERVAL)

    def generateData(self, x, y, z, count):
        self.x_line_array.append(x)
        self.y_line_array.append(y)
        self.z_line_array.append(z)
        self.frame_count_array.append(count)

    def clearLineData(self):
        self.x_line_array = []
        self.y_line_array = []
        self.z_line_array = []
        self.frame_count_array = []