# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from PyQt4 import QtGui, QtCore, uic
import monitor_thread_operations as socket
import PyQt4.Qwt5 as Qwt
import globals
import Queue
import os
import time
import xlwt
import algorithm


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('ui/mainwindow.ui', self)
        with open("comple.py", "w") as pyfile:
            uic.compileUi('ui/mainwindow.ui', pyfile)

        self.move(10, 10)

        self.init_component()
        self.init_defaultUI()
        self.init_cnavas()

        self.init_connect()
        self.init_data_path()


    def init_data_path(self):
        if not os.path.exists("Data/"):
            os.makedirs("Data/")
        self.data_path = "Data/"

    def init_component(self):
        self.timer = QtCore.QTimer()
        self.livefeed = globals.LiveDataFeed()
        self.gyo_livefeed = globals.LiveDataFeed()
        self.acc_samples = [[], [], []]
        self.gyo_samples = [[], [], []]
        self.scale_value = globals.DEFAULT_SCALE
        self.update_label_count = 0
        self.excel_data = []
        self.update_statusbar_count = 0
        self.__enableRecoedData = True
        self.__enablecanvas = False
        self.__enable_identify = False
        self.tab_index = 0
        self.__calibrate_once = False
        self.identify_result_memory = 0

    def plot_factory(self, parent_object):
        plot = Qwt.QwtPlot(parent_object)
        plot.setCanvasBackground(QtCore.Qt.black)
        plot.setAxisScale(Qwt.QwtPlot.xBottom, 0, 10, 1)
        plot.setAxisScale(Qwt.QwtPlot.yLeft, globals.YMIN, globals.YMAX, (globals.YMAX - globals.YMIN) / 10)
        plot.replot()

        curve = [None] * 3
        pen = [QtGui.QPen(QtGui.QColor('limegreen')), QtGui.QPen(QtGui.QColor('red')),
               QtGui.QPen(QtGui.QColor('yellow'))]
        for i in range(3):
            curve[i] = Qwt.QwtPlotCurve('')
            curve[i].setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
            pen[i].setWidth(2)
            curve[i].setPen(pen[i])
            curve[i].attach(plot)

        plot_layout = QtGui.QGridLayout()
        plot_layout.addWidget(plot, 0, 0, 8, 7)
        parent_object.setLayout(plot_layout)

        return plot, curve

    def init_cnavas(self):
        self.acc_plot, self.acc_curve = self.plot_factory(self.acc_groupBox)
        self.gyo_plot, self.gyo_curve = self.plot_factory(self.gyo_groupBox)

    def init_defaultUI(self):
        self.stop_pushButton.setDisabled(True)
        self.canvas_start_pushButton.setDisabled(True)
        self.canvas_pause_pushButton.setDisabled(True)
        self.recordButton.setDisabled(True)
        self.BaudRate_lineEdit.setText("115200")
        self.updateStatusBar("UART Closed")
        self.settings = {}
        avaliable_serial_port = globals.enumerate_serial_ports()
        if avaliable_serial_port:
            for port in avaliable_serial_port:
                self.Port_num_comboBox.addItem(port)
        green = QtGui.QPalette()
        green.setColor(QtGui.QPalette.Foreground, QtGui.QColor('limegreen'))
        self.x_legend_label.setPalette(green)
        red = QtGui.QPalette()
        red.setColor(QtGui.QPalette.Foreground, QtGui.QColor('red'))
        self.y_legend_label.setPalette(red)
        yellow = QtGui.QPalette()
        yellow.setColor(QtGui.QPalette.Foreground, QtGui.QColor('yellow'))
        self.z_legend_label.setPalette(yellow)
        self.on_timer_count = 0

    def init_connect(self):
        self.actionExit.triggered.connect(self.close)
        self.open_pushButton.clicked.connect(self.on_open_serial)
        self.stop_pushButton.clicked.connect(self.on_close_serial)
        self.canvas_start_pushButton.clicked.connect(self.on_start_canvas)
        self.canvas_pause_pushButton.clicked.connect(self.on_pause_canvas)
        self.recordButton.clicked.connect(self.on_record)

        QtCore.QObject.connect(
            self.Port_num_comboBox,
            QtCore.SIGNAL("currentIndexChanged(int)"),
            self.on_portnum_changed
        )
        QtCore.QObject.connect(
            self.timer,
            QtCore.SIGNAL("timeout()"),
            self.on_timer
        )
        QtCore.QObject.connect(
            self.tabWidget,
            QtCore.SIGNAL("currentChanged(int)"),
            self.on_tab_changed
        )

    def on_record(self):
        self.receive_thread.force_record()
        self.updateStatusBar("Force Record")


    def on_tab_changed(self,index):
        self.tab_index = index
        if index==0:
            self.groupBox_2.setVisible(True)
        else:
            self.groupBox_2.setVisible(False)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            try:
                self.socket_link.close()
                self.acc_canvas.releasePlot()
                self.gyo_canvas.releasePlot()
            except AttributeError:
                pass
            event.accept()
        else:
            event.ignore()

    def on_portnum_changed(self, index):
        print self.Port_num_comboBox.currentText()

    def read_serial_data(self):
        qdata = list(globals.get_all_from_queue(self.data_q))
        if len(qdata) > 0:
            data = dict(timestamp=qdata[-1][1],
                        frame_count=qdata[-1][2],
                        acc_x=qdata[-1][0][0],
                        acc_y=qdata[-1][0][1],
                        acc_z=qdata[-1][0][2],
                        gyo_x=qdata[-1][0][3],
                        gyo_y=qdata[-1][0][4],
                        gyo_z=qdata[-1][0][5]
                        )
            self.livefeed.add_data(data)
            return dict(acc_x=qdata[-1][0][0],
                        acc_y=qdata[-1][0][1],
                        acc_z=qdata[-1][0][2],
                        gyo_x=qdata[-1][0][3],
                        gyo_y=qdata[-1][0][4],
                        gyo_z=qdata[-1][0][5]
                        )
        return None

    def update_plot(self, data):

        self.acc_samples[0].append((data['frame_count'], data['acc_x']))
        if len(self.acc_samples[0]) > max(100,self.scale_value):
            self.acc_samples[0].pop(0)

        self.acc_samples[1].append((data['frame_count'], data['acc_y']))
        if len(self.acc_samples[1]) > max(100,self.scale_value):
            self.acc_samples[1].pop(0)

        self.acc_samples[2].append((data['frame_count'], data['acc_z']))
        if len(self.acc_samples[2]) > max(100,self.scale_value):
            self.acc_samples[2].pop(0)

        self.gyo_samples[0].append((data['frame_count'], data['gyo_x']))
        if len(self.gyo_samples[0]) > max(100, self.scale_value):
            self.gyo_samples[0].pop(0)

        self.gyo_samples[1].append((data['frame_count'], data['gyo_y']))
        if len(self.gyo_samples[1]) > max(100, self.scale_value):
            self.gyo_samples[1].pop(0)

        self.gyo_samples[2].append((data['frame_count'], data['gyo_z']))
        if len(self.gyo_samples[2]) > max(100, self.scale_value):
            self.gyo_samples[2].pop(0)

        tdata = [s[0] for s in self.acc_samples[2]]

        for i in range(3):
            data[i] = [s[1] for s in self.acc_samples[i]]
            self.acc_curve[i].setData(tdata, data[i])
        for i in range(3):
            data[i] = [s[1] for s in self.gyo_samples[i]]
            self.gyo_curve[i].setData(tdata, data[i])
        self.acc_plot.setAxisScale(Qwt.QwtPlot.xBottom, tdata[-1]-self.scale_value, max(1, tdata[-1]))
        self.acc_plot.replot()

        self.gyo_plot.setAxisScale(Qwt.QwtPlot.xBottom, tdata[-1] - self.scale_value, max(1, tdata[-1]))
        self.gyo_plot.replot()

    def update_label(self, data_dict):
        def update(data):
            self.updataACCLabel(data["acc_x"],
                                data["acc_y"],
                                data["acc_z"]
                                )
            self.updataGYOLabel(data["gyo_x"],
                                data["gyo_y"],
                                data["gyo_z"]
                                )
        self.update_label_count += 1
        if self.update_label_count >= 10:
            self.update_label_count = 0
            update(data_dict)

    def on_timer(self):
        self.on_timer_count += 1
        if self.on_timer_count == 50:
            self.on_timer_count = 0
            msg = globals.get_item_from_queue(self.msg_q)
            if msg:
                self.updateStatusBar(msg)
        data_dict = self.read_serial_data()
        if data_dict:
            self.update_label(data_dict)
        if self.livefeed.has_new_data:
            data = self.livefeed.read_data()
            if self.__enablecanvas is True and self.tab_index == 0:
                self.update_plot(data)

    def on_start_canvas(self):
        self.__enablecanvas = True
        self.canvas_pause_pushButton.setEnabled(True)
        self.canvas_start_pushButton.setDisabled(True)

    def on_pause_canvas(self):
        self.__enablecanvas = False
        self.canvas_pause_pushButton.setDisabled(True)
        self.canvas_start_pushButton.setEnabled(True)

    def on_identify_state_changed(self):
        if self.__enable_identify is False:     #identify running
            self.__enable_identify = True
            self.algorithm_pushButton.setText("Stop Monitor")

            self.identify = algorithm.ManholeAlgorithm()
        else:
            self.__enable_identify = False
            self.algorithm_pushButton.setText("Start Monitor")

            self.identify = None

    def on_calibrate(self):
        self.__calibrate_once = True

    def on_identify(self, data_dict):
        if self.identify:
            result = self.identify.variance_identify(data_dict)
            if result != self.identify_result_memory:
                self.identify_result_memory = result
                if result == 1:
                    self.result_label.setText(u"井盖开启")
                elif result == 2:
                    self.result_label.setText(u"井盖沉降")
                else:
                    self.result_label.setText(u"井盖正常")

    def on_open_serial(self):
        self.data_q = Queue.Queue()
        self.error_q = Queue.Queue()
        self.msg_q = Queue.Queue()

        if self.settings.has_key("port"):
            self.stop_pushButton.setEnabled(True)
            self.open_pushButton.setDisabled(True)
        else:
            self.settings["port"] = str(self.Port_num_comboBox.currentText())
            self.settings["baudrate"] = int(self.BaudRate_lineEdit.text())
            if self.settings["port"] == "":
                QtGui.QMessageBox.critical(self, 'Serial port error',
                                           "unknow port num")
                self.settings = {}
                return
            try:
                self.receive_thread = socket.myThread(
                    self.settings,
                    self.data_q,
                    self.error_q,
                    self.msg_q
                )
                self.receive_thread.setDaemon(True)
                self.receive_thread.start()
                com_error = globals.get_item_from_queue(self.error_q)
                if com_error is not None:
                    QtGui.QMessageBox.critical(self, 'ComMonitorThread error',
                                         com_error)
                    self.receive_thread = None
                    return

            except OSError as err:
                self.updateStatusBar(str(err))
        self.monitor_active = True
        self.Port_num_comboBox.setDisabled(True)
        self.stop_pushButton.setEnabled(True)
        self.open_pushButton.setDisabled(True)
        self.canvas_start_pushButton.setEnabled(True)
        self.canvas_pause_pushButton.setEnabled(True)
        self.BaudRate_lineEdit.setDisabled(True)
        self.recordButton.setEnabled(True)
        self.updateStatusBar("UART Opened")
        self.timer.start(15)
        self.on_start_canvas()

    def on_close_serial(self):
        if self.receive_thread is not None:
            self.receive_thread.join(1000)
            self.receive_thread = None
        self.monitor_active = False
        self.settings = {}
        self.timer.stop()
        self.stop_pushButton.setDisabled(True)
        self.open_pushButton.setEnabled(True)
        self.Port_num_comboBox.setEnabled(True)
        self.canvas_start_pushButton.setDisabled(True)
        self.canvas_pause_pushButton.setDisabled(True)
        self.algorithm_pushButton.setDisabled(True)
        self.calibrate_pushButton.setDisabled(True)
        self.updateStatusBar("monitor stoped")

    def updateStatusBar(self, msg):
        self.statusBar.showMessage(msg)
        self.update_statusbar_count += 1

    def updataACCLabel(self, x, y, z):
        self.acc_x_Label.setText(str(x))
        self.acc_y_Label.setText(str(y))
        self.acc_z_Label.setText(str(z))

    def updataGYOLabel(self, x, y, z):
        self.gyo_x_Label.setText(str(x))
        self.gyo_y_Label.setText(str(y))
        self.gyo_z_Label.setText(str(z))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.on_open_serial()
    sys.exit(app.exec_())
