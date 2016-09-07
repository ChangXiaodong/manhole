import sys
from PyQt4 import QtGui, QtCore, uic
import monitor_thread_operations as socket
import PyQt4.Qwt5     as Qwt
import globals
import Queue
import os
import time
import xlwt


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
        self.__enablecanvas = True

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
        self.record_data_checkBox.setChecked(True)
        self.stop_pushButton.setDisabled(True)
        self.open_data_pushButton.setDisabled(True)
        self.canvas_start_pushButton.setDisabled(True)
        self.canvas_pause_pushButton.setDisabled(True)
        self.BaudRate_lineEdit.setText("115200")
        # self.HOST_IP_lineEdit.setText(socket.getIPAddress())
        self.updateStatusBar("UART Closed")
        self.settings = {}
        for port in globals.enumerate_serial_ports():
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


    def init_connect(self):
        self.actionExit.triggered.connect(self.close)
        self.open_pushButton.clicked.connect(self.on_open_serial)
        self.stop_pushButton.clicked.connect(self.on_close_serial)
        self.canvas_start_pushButton.clicked.connect(self.on_start_canvas)
        self.canvas_pause_pushButton.clicked.connect(self.on_pause_canvas)
        self.horizontalSlider.setRange(0, 1000)
        self.horizontalSlider.setValue(500)
        QtCore.QObject.connect(
            self.horizontalSlider,
            QtCore.SIGNAL("valueChanged(int)"),
            self.onScaleChanged
        )
        QtCore.QObject.connect(
            self.Port_num_comboBox,
            QtCore.SIGNAL("currentIndexChanged(int)"),
            self.on_portnum_changed
        )
        QtCore.QObject.connect(
            self.record_data_checkBox,
            QtCore.SIGNAL("stateChanged(int)"),
            self.on_record_data_state_changed
        )
        QtCore.QObject.connect(
            self.timer,
            QtCore.SIGNAL("timeout()"),
            self.on_timer
        )

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

    def onScaleChanged(self, value):
        self.updateStatusBar("Update Speed = %s Hz" % value)
        self.scale_value = 1000-value
        if self.timer.isActive():
            update_freq = max(1, value)
            self.timer_interval = 1000.0 / update_freq
            self.timer.setInterval(self.timer_interval)

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

    def update_plot(self):
        if self.livefeed.has_new_data:
            data = self.livefeed.read_data()
            if(self.__enableRecoedData == True):
                timestamp = str(time.strftime(
                                    '%Y-%m-%d %H:%M:%S ',
                                    time.localtime(data['timestamp'])
                                ))
                self.excel_data.append([timestamp,
                                     data['acc_x'], data['acc_y'], data['acc_z'],
                                     data['gyo_x'], data['gyo_y'], data['gyo_z']
                                     ])
                if len(self.excel_data) > 1000:
                    for item in self.excel_data:
                        self.worksheet.write(self.excel_row, 0, label=item[0])
                        self.worksheet.write(self.excel_row, 1, label=item[1])
                        self.worksheet.write(self.excel_row, 2, label=item[2])
                        self.worksheet.write(self.excel_row, 3, label=item[3])
                        self.worksheet.write(self.excel_row, 4, label=item[4])
                        self.worksheet.write(self.excel_row, 5, label=item[5])
                        self.worksheet.write(self.excel_row, 6, label=item[6])
                        self.excel_row += 1

                    self.excel.save(self.data_path)
                    self.updateStatusBar('transfert data to excel after 1000 samples')
                    self.excel_data = []

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
        if self.timer_interval < 100:
            self.update_label_count += 1
            if self.update_label_count >= 30:
                self.update_label_count = 0
                update(data_dict)
        else:

            update(data_dict)

    def on_timer(self):
        data_dict = self.read_serial_data()
        if(self.__enablecanvas == True):
            self.update_plot()
        if data_dict:
            self.update_label(data_dict)

    def on_start_canvas(self):
        self.__enablecanvas = True

    def on_pause_canvas(self):
        self.__enablecanvas = False

    def on_open_serial(self):
        self.data_path += str(time.strftime(
                            '%Y-%m-%d_%H-%M-%S ',
                            time.localtime(time.time())))+".xls"
        self.excel = xlwt.Workbook(encoding='ascii')
        self.worksheet = self.excel.add_sheet('Data')
        self.excel_row = 0
        self.data_q = Queue.Queue()
        self.error_q = Queue.Queue()

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
                    self.error_q
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
        self.updateStatusBar("UART Opened")
        update_freq = self.horizontalSlider.value()
        if update_freq > 0:
            self.timer_interval = 1000.0 / update_freq
            self.timer.start(self.timer_interval)

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
        self.updateStatusBar("monitor stoped")

    def on_record_data_state_changed(self, state):
        if state == 2:
            self.__enableRecoedData = True
        else:
            self.__enableRecoedData = False

    def updateStatusBar(self, msg):
        self.statusBar.showMessage(msg + ":%s" % self.update_statusbar_count)
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
