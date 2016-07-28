import sys
from PyQt4 import QtGui, QtCore, uic
import socket_operations as socket
from mplCanvasWrapper import MplCanvasWrapper


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('ui/mainwindow.ui', self)
        with open("comple.py", "w") as pyfile:
            uic.compileUi('ui/mainwindow.ui', pyfile)

        self.move(10, 10)

        self.initCnavas()
        self.initDefaultUI()
        self.initConnect()

    def initCnavas(self):
        self.canvas_scale = 80
        self.acc_x = []
        self.acc_y = []
        self.acc_z = []
        self.acc_canvas = MplCanvasWrapper(
            self.groupBox_2,
            self.acc_x,
            self.acc_y,
            self.acc_z,
            "ACC"
        )
        self.acc_canvas.setGeometry(QtCore.QRect(0, 20, 991, 281))
        self.acc_canvas.startPlot()

        self.gyo_x = []
        self.gyo_y = []
        self.gyo_z = []
        self.gyo_canvas = MplCanvasWrapper(
            self.groupBox_3,
            self.gyo_x,
            self.gyo_y,
            self.gyo_z,
            "GYO"
        )
        self.gyo_canvas.setGeometry(QtCore.QRect(0, 20, 991, 281))
        self.gyo_canvas.startPlot()

    def initDefaultUI(self):
        self.record_data_checkBox.setChecked(True)
        self.stop_pushButton.setDisabled(True)
        self.open_data_pushButton.setDisabled(True)
        self.HOST_IP_lineEdit.setText("10.10.100.254")
        # self.HOST_IP_lineEdit.setText(socket.getIPAddress())
        self.port_num_lineEdit.setText("8899")
        self.updateStatusBar("Socket Closed")

    def initConnect(self):
        self.actionExit.triggered.connect(self.close)
        self.open_pushButton.clicked.connect(self.onOpenSocket)
        self.stop_pushButton.clicked.connect(self.onCloseSocket)
        self.canvas_start_pushButton.clicked.connect(self.onStartCanvas)
        self.canvas_pause_pushButton.clicked.connect(self.onPauseCanvas)
        self.horizontalSlider.setRange(30, 130)
        self.horizontalSlider.setValue(80)
        QtCore.QObject.connect(
            self.horizontalSlider,
            QtCore.SIGNAL("valueChanged(int)"),
            self.onScaleChanged
        )
        QtCore.QObject.connect(
            self.socket_type_comboBox,
            QtCore.SIGNAL("currentIndexChanged(int)"),
            self.onSocketTypeChanged
        )
        QtCore.QObject.connect(
            self.record_data_checkBox,
            QtCore.SIGNAL("stateChanged(int)"),
            self.onRecordDataStateChanged
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

    def onSocketTypeChanged(self, index):
        if index == 0:
            self.HOST_IP_lineEdit.setText("10.10.100.254")
        elif index == 1:
            self.HOST_IP_lineEdit.setText(socket.getIPAddress())

    def onScaleChanged(self, value):
        self.acc_canvas.setMaxArrayLength(value)
        self.gyo_canvas.setMaxArrayLength(value)

    def onStartCanvas(self):
        self.acc_canvas.startPlot()
        self.gyo_canvas.startPlot()

    def onPauseCanvas(self):
        self.acc_canvas.pausePlot()
        self.gyo_canvas.pausePlot()

    def onOpenSocket(self):
        ip = self.HOST_IP_lineEdit.text()
        portnum = self.port_num_lineEdit.text()
        type = self.socket_type_comboBox.currentText()
        self.socket_link = socket.Socket(
            ip,
            portnum,
            type,
            self,
            self.acc_canvas.generateData,
            self.gyo_canvas.generateData,
            self.updataACCLabel,
            self.updataGYOLabel
        )
        try:
            self.socket_link.creat()
            self.stop_pushButton.setEnabled(True)
            self.open_pushButton.setDisabled(True)
        except OSError as err:
            self.updateStatusBar(str(err))

    def onCloseSocket(self):
        self.socket_link.close()

    def onRecordDataStateChanged(self, state):
        if state == 2:
            import time
            path = time.strftime(
                '%Y-%m-%d_%H-%M-%S',
                time.localtime(time.time())
            ) + '.txt'
            self.socket_link.setDataPath(path)
            self.socket_link.enableRecoedData(True)
        else:
            self.socket_link.enableRecoedData(False)

    def updateStatusBar(self, msg):
        self.statusBar.showMessage(msg)

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
    try:
        win.onOpenSocket()
    except:
        pass
    sys.exit(app.exec_())
