# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
from PyQt4 import QtGui, QtCore, uic
import monitor_thread_operations as socket
import PyQt4.Qwt5 as Qwt
import Queue
import os
import algorithm, camera_capture, globals


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('../ui/mainwindow.ui', self)
        with open("comple.py", "w") as pyfile:
            uic.compileUi('../ui/mainwindow.ui', pyfile)

        self.move(10, 10)

        self.init_component()
        self.init_defaultUI()
        self.init_cnavas()

        self.init_connect()
        self.init_data_path()

    def init_data_path(self):
        if not os.path.exists("../Data/"):
            os.makedirs("../Data/")
        self.data_path = "../Data/"

    def init_component(self):
        self.timer = QtCore.QTimer()
        self.data_q = Queue.Queue()
        self.error_q = Queue.Queue()
        self.msg_q = Queue.Queue()
        self.active_q = Queue.Queue()
        self.receive_thread = None
        self.scale_value = globals.DEFAULT_SCALE
        self.update_label_count = 0
        self.update_statusbar_count = 0
        self.__enableRecoedData = True
        self.__enablecanvas = False
        self.__enable_identify = False
        self.tab_index = 0
        self.__calibrate_once = False
        self.identify_result_memory = 0
        self.camera = None
        self.data_source = "uart"
        self.open_cnt = 0
        self.uart_mode = "live"

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
        self.disconnect_pushButton.setDisabled(True)
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
        self.recordButton.clicked.connect(self.on_record)
        self.actionUpdate_uart_port.triggered.connect(self.on_update_uart_port)
        self.actionCamera1.triggered.connect(self.on_open_camera1)
        self.actionCamera2.triggered.connect(self.on_open_camera2)
        self.actionClose.triggered.connect(self.on_close_camera)
        self.acc_scale_up_Button.clicked.connect(self.on_acc_scale_up)
        self.acc_scale_down_Button.clicked.connect(self.on_acc_scale_down)
        self.gyo_scale_up_Button.clicked.connect(self.on_gyo_scale_up)
        self.gyo_scale_down_Button.clicked.connect(self.on_gyo_scale_down)
        self.sequence_radioButton.clicked.connect(self.on_seq_radio)
        self.single_radioButton.clicked.connect(self.on_single_radio)
        self.read_config_pushButton.clicked.connect(self.on_read_config)
        self.write_config_pushButton.clicked.connect(self.on_write_config)
        self.connect_pushButton.clicked.connect(self.on_connect_socket)
        self.disconnect_pushButton.clicked.connect(self.on_disconnect_socket)
        self.static_radioButton.clicked.connect(self.on_static_radio)
        self.live_radioButton.clicked.connect(self.on_live_radio)

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

    def on_static_radio(self):
        self.uart_mode = "static"

    def on_live_radio(self):
        self.uart_mode = "live"

    def on_seq_radio(self):
        self.receive_thread.set_single_mode(False)
        self.updateStatusBar("Sequence Captured")

    def on_single_radio(self):
        self.receive_thread.set_single_mode(True)
        self.updateStatusBar("Single Captured")

    def on_open_camera1(self):
        if self.camera:
            self.camera.close()
            self.camera.open_camera(0)
        else:
            self.camera = camera_capture.Camera(self.msg_q, 0)
            self.camera.setDaemon(True)
            self.camera.start()
        if self.receive_thread:
            self.receive_thread.camera = self.camera
        self.updateStatusBar("Camera 1 opened")

    def on_open_camera2(self):
        if self.camera:
            self.camera.close()
            self.camera.open_camera(1)
        else:
            self.camera = camera_capture.Camera(self.msg_q, 1)
            self.camera.setDaemon(True)
            self.camera.start()
        if self.receive_thread:
            self.receive_thread.camera = self.camera
        self.updateStatusBar("Camera 2 opened")

    def on_close_camera(self):
        self.camera.close()

    def on_acc_scale_up(self):
        if self.acc_scale + 1 < 4:
            self.receive_thread.send([
                0x7D,
                self.acc_scale + 1, self.acc_fchoice, self.acc_dlpf,
                self.gyo_scale, self.gyo_fchoice, self.gyo_dlpf,
                0x7F
            ])

    def on_acc_scale_down(self):
        if self.acc_scale - 1 >= 0:
            self.receive_thread.send([
                0x7D,
                self.acc_scale - 1, self.acc_fchoice, self.acc_dlpf,
                self.gyo_scale, self.gyo_fchoice, self.gyo_dlpf,
                0x7F
            ])

    def on_gyo_scale_up(self):
        if self.gyo_scale + 1 < 4:
            self.receive_thread.send([
                0x7D,
                self.acc_scale, self.acc_fchoice, self.acc_dlpf,
                self.gyo_scale + 1, self.gyo_fchoice, self.gyo_dlpf,
                0x7F
            ])

    def on_gyo_scale_down(self):
        if self.gyo_scale - 1 >= 0:
            self.receive_thread.send([
                0x7D,
                self.acc_scale, self.acc_fchoice, self.acc_dlpf,
                self.gyo_scale - 1, self.gyo_fchoice, self.gyo_dlpf,
                0x7F
            ])

    def on_read_config(self):
        self.acc_fchoice_lineEdit.setText(str(self.acc_fchoice))
        self.acc_dlpf_cfg_lineEdit.setText(str(self.acc_dlpf))
        self.acc_fs_sel_lineEdit.setText(str(self.acc_scale))
        self.gyo_fchoice_lineEdit.setText(str(self.gyo_fchoice))
        self.gyo_dlpf_cfg_lineEdit.setText(str(self.gyo_dlpf))
        self.gyo_fs_sel_lineEdit.setText(str(self.gyo_scale))
        self.acc_scale_label.setText(str(self.acc_scale_text))
        self.gyo_scale_label.setText(str(self.gyo_scale_text))
        acc_band_width = ""
        gyo_band_width = ""

        if self.acc_fchoice == 1:
            acc_band_width = "1.13K"
        else:
            if self.acc_dlpf == 0:
                acc_band_width = "460"
            elif self.acc_dlpf == 1:
                acc_band_width = "184"
            elif self.acc_dlpf == 2:
                acc_band_width = "92"
            elif self.acc_dlpf == 3:
                acc_band_width = "41"
            elif self.acc_dlpf == 4:
                acc_band_width = "20"
            elif self.acc_dlpf == 5:
                acc_band_width = "10"
            elif self.acc_dlpf == 6:
                acc_band_width = "5"
            elif self.acc_dlpf == 7:
                acc_band_width = "460"
        if self.gyo_fchoice == 1 or self.gyo_fchoice == 3:
            gyo_band_width = "8800"
        elif self.gyo_fchoice == 2:
            gyo_band_width = "3600"
        else:
            if self.gyo_dlpf == 0:
                gyo_band_width = "250"
            elif self.gyo_dlpf == 1:
                gyo_band_width = "184"
            elif self.gyo_dlpf == 2:
                gyo_band_width = "92"
            elif self.gyo_dlpf == 3:
                gyo_band_width = "41"
            elif self.gyo_dlpf == 4:
                gyo_band_width = "20"
            elif self.gyo_dlpf == 5:
                gyo_band_width = "10"
            elif self.gyo_dlpf == 6:
                gyo_band_width = "5"
            elif self.gyo_dlpf == 7:
                gyo_band_width = "3600"
        self.acc_bw_label.setText(acc_band_width)
        self.gyo_bw_label.setText(gyo_band_width)

    def on_write_config(self):
        acc_scale = abs(int(self.acc_fs_sel_lineEdit.text()))
        acc_dlpf = abs(int(self.acc_dlpf_cfg_lineEdit.text()))
        acc_fchoice = abs(int(self.acc_fchoice_lineEdit.text()))
        gyo_scale = abs(int(self.gyo_fs_sel_lineEdit.text()))
        gyo_dlpf = abs(int(self.gyo_dlpf_cfg_lineEdit.text()))
        gyo_fchoice = abs(int(self.gyo_fchoice_lineEdit.text()))
        if acc_scale > 3:
            acc_scale = 3
        if acc_dlpf > 7:
            acc_dlpf = 7
        if acc_fchoice > 1:
            acc_fchoice = 1
        if gyo_scale > 3:
            gyo_scale = 3
        if gyo_dlpf > 7:
            gyo_dlpf = 7
        if gyo_fchoice > 3:
            gyo_fchoice = 3

        self.updateStatusBar("acc_scale:{} acc_dlpf:{} acc_fchoice:{} gyo_scale:{} gyo_dlpf:{} gyo_fchoice:{}".format(
            acc_scale, acc_dlpf, acc_fchoice, gyo_scale, gyo_dlpf, gyo_fchoice
        ))
        self.receive_thread.send([0x7D, acc_scale, acc_fchoice, acc_dlpf, gyo_scale, gyo_fchoice, gyo_dlpf, 0x7F])

    def on_calibrate(self):
        self.receive_thread.send([0x01])
        self.__calibrate_once = True

    def on_update_uart_port(self):
        self.Port_num_comboBox.clear()
        avaliable_serial_port = globals.enumerate_serial_ports()
        if avaliable_serial_port:
            for port in avaliable_serial_port:
                self.Port_num_comboBox.addItem(port)

    def on_record(self):
        self.receive_thread.force_record()
        self.updateStatusBar("Force Record")

    def on_tab_changed(self, index):
        self.tab_index = index
        if index == 0:
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
        print(self.Port_num_comboBox.currentText())

    def read_serial_data(self):
        qdata = list(globals.get_all_from_queue(self.data_q))
        if len(qdata) > 0:
            return dict(acc_x=qdata[-1][0][0],
                        acc_y=qdata[-1][0][1],
                        acc_z=qdata[-1][0][2],
                        gyo_x=qdata[-1][0][3],
                        gyo_y=qdata[-1][0][4],
                        gyo_z=qdata[-1][0][5],
                        acc_scale=qdata[-1][0][6],
                        acc_fchoice=qdata[-1][0][7],
                        acc_dlpf=qdata[-1][0][8],
                        gyo_scale=qdata[-1][0][9],
                        gyo_fchoice=qdata[-1][0][10],
                        gyo_dlpf=qdata[-1][0][11]
                        )
        return None

    def update_plot(self, data):

        self.acc_curve[0].setData(range(len(data['acc_x'])), data['acc_x'])
        self.acc_curve[1].setData(range(len(data['acc_y'])), data['acc_y'])
        self.acc_curve[2].setData(range(len(data['acc_z'])), data['acc_z'])

        self.gyo_curve[0].setData(range(len(data['gyo_x'])), data['gyo_x'])
        self.gyo_curve[1].setData(range(len(data['gyo_y'])), data['gyo_y'])
        self.gyo_curve[2].setData(range(len(data['gyo_z'])), data['gyo_z'])
        self.acc_plot.setAxisScale(Qwt.QwtPlot.xBottom, 0, data['acc_x'].__len__())
        self.acc_plot.replot()

        self.gyo_plot.setAxisScale(Qwt.QwtPlot.xBottom, 0, data['gyo_x'].__len__())
        self.gyo_plot.replot()

    def update_label(self, data_dict):
        def update(data):
            self.updataACCLabel(data["acc_x"],
                                data["acc_y"],
                                data["acc_z"],
                                data["acc_scale"]
                                )
            self.updataGYOLabel(data["gyo_x"],
                                data["gyo_y"],
                                data["gyo_z"],
                                data["gyo_scale"]
                                )

        def open_detection(x, y, z):
            import math
            if z == 0:
                z = 1
            angle = math.atan((x ** 2 + y ** 2) ** 0.5 / z)
            angle = abs(int(angle * 360))
            if angle > 100:
                self.open_cnt += 1
            else:
                self.open_cnt = 0
            if self.open_cnt > 3:
                self.status_label.setText(u"井盖开启")
            else:
                self.status_label.setText(u"井盖正常")

        open_detection(data_dict["acc_x"], data_dict["acc_y"], data_dict["acc_z"], )

        self.acc_scale = data_dict["acc_scale"]
        self.acc_fchoice = data_dict["acc_fchoice"]
        self.acc_dlpf = data_dict["acc_dlpf"]
        self.gyo_scale = data_dict["gyo_scale"]
        self.gyo_fchoice = data_dict["gyo_fchoice"]
        self.gyo_dlpf = data_dict["gyo_dlpf"]

        if self.data_source == "uart":
            self.update_label_count += 1
            if self.update_label_count >= 10:
                self.update_label_count = 0
                update(data_dict)
        else:
            update(data_dict)

    def on_timer(self):
        self.on_timer_count += 1
        if self.on_timer_count == 5:
            self.on_timer_count = 0
            msg = globals.get_item_from_queue(self.msg_q)
            if msg:
                self.updateStatusBar(msg)
        data_dict = self.read_serial_data()
        if data_dict:
            self.update_label(data_dict)
        active_data = globals.get_item_from_queue(self.active_q)
        if active_data:
            self.update_plot(active_data)

    def on_identify_state_changed(self):
        if self.__enable_identify is False:  # identify running
            self.__enable_identify = True
            self.algorithm_pushButton.setText("Stop Monitor")

            self.identify = algorithm.ManholeAlgorithm()
        else:
            self.__enable_identify = False
            self.algorithm_pushButton.setText("Start Monitor")

            self.identify = None

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
        self.receive_thread = None

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
                if self.uart_mode == "live":
                    self.receive_thread = socket.myThread(
                        self.settings,
                        self.data_q,
                        self.active_q,
                        self.error_q,
                        self.msg_q,
                        self.camera
                    )
                else:
                    self.receive_thread = socket.staticThread(
                        self.settings,
                        self.data_q,
                        self.active_q,
                        self.error_q,
                        self.msg_q,
                        self.camera
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
        self.BaudRate_lineEdit.setDisabled(True)
        self.recordButton.setEnabled(True)
        self.updateStatusBar("UART Opened")
        self.data_source = "uart"
        self.timer.start(15)

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
        self.recordButton.setDisabled(True)
        self.updateStatusBar("monitor stoped")

    def on_connect_socket(self):
        self.receive_thread = None
        self.settings["server_ip"] = self.server_ip_lineEdit.text()
        self.settings["port"] = self.server_port_lineEdit.text()
        self.receive_thread = socket.myThread(
            self.settings,
            self.data_q,
            self.active_q,
            self.error_q,
            self.msg_q,
            self.camera,
            device="wifi"
        )
        self.receive_thread.setDaemon(True)
        self.receive_thread.start()
        self.monitor_active = True
        self.canvas_start_pushButton.setEnabled(True)
        self.canvas_pause_pushButton.setEnabled(True)
        self.server_ip_lineEdit.setDisabled(True)
        self.server_port_lineEdit.setDisabled(True)
        self.recordButton.setEnabled(True)
        self.disconnect_pushButton.setEnabled(True)
        self.connect_pushButton.setDisabled(True)
        self.updateStatusBar("TCP Connected")
        self.data_source = "wifi"
        self.timer.start(15)

    def on_disconnect_socket(self):
        if self.receive_thread is not None:
            self.receive_thread.join(1000)
            self.receive_thread = None
        self.monitor_active = False
        self.timer.stop()
        self.disconnect_pushButton.setDisabled(True)
        self.connect_pushButton.setEnabled(True)
        self.canvas_start_pushButton.setDisabled(True)
        self.canvas_pause_pushButton.setDisabled(True)
        self.recordButton.setDisabled(True)
        self.server_ip_lineEdit.setEnabled(True)
        self.server_port_lineEdit.setEnabled(True)
        self.updateStatusBar("monitor stoped")

    def updateStatusBar(self, msg):
        self.statusBar.showMessage(msg)
        self.update_statusbar_count += 1

    def updataACCLabel(self, x, y, z, scale):
        self.acc_x_Label.setText(str(x))
        self.acc_y_Label.setText(str(y))
        self.acc_z_Label.setText(str(z))
        self.acc_scale = scale
        if scale == 0:
            self.acc_scale_text = "2"
        elif scale == 1:
            self.acc_scale_text = "4"
        elif scale == 2:
            self.acc_scale_text = "8"
        else:
            self.acc_scale_text = "16"
        self.acc_scale_Label.setText(self.acc_scale_text)

    def updataGYOLabel(self, x, y, z, scale):
        self.gyo_x_Label.setText(str(x))
        self.gyo_y_Label.setText(str(y))
        self.gyo_z_Label.setText(str(z))
        self.gyo_scale = scale
        if scale == 0:
            self.gyo_scale_text = "250"
        elif scale == 1:
            self.gyo_scale_text = "500"
        elif scale == 2:
            self.gyo_scale_text = "1000"
        else:
            self.gyo_scale_text = "2000"
        self.gyo_scale_Label.setText(self.gyo_scale_text)

    def open_camera(self):
        try:
            if self.receive_thread:
                self.camera = camera_capture.Camera(self.msg_q, 1)
                self.camera.setDaemon(True)
                self.camera.start()
                self.receive_thread.camera = self.camera
        except AttributeError:
            print("Unknown Data Source")


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()

    # win.on_open_serial()
    # win.on_connect_socket()
    # win.open_camera()
    sys.exit(app.exec_())
