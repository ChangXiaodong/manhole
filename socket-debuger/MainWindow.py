import sys
from PyQt4 import QtGui, QtCore, uic
import socket_operations

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('ui/mainwindow.ui', self)
        # with open("comple.py","w") as pyfile:
        #     uic.compileUi('ui/mainwindow.ui',pyfile)


        self.initDefaultUI()
        self.initConnect()

    def initDefaultUI(self):
        self.record_data_checkBox.setChecked(True)
        self.stop_pushButton.setDisabled(True)
        self.open_data_pushButton.setDisabled(True)
        self.HOST_IP_lineEdit.setText(socket_operations.getIPAddress())
        self.port_num_lineEdit.setText("60000")
        self.updateStatusBar("Socket Closed")

    def initConnect(self):
        self.actionExit.triggered.connect(self.close)
        self.open_pushButton.clicked.connect(self.onOpenSocket)
        self.stop_pushButton.clicked.connect(self.onCloseSocket)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            try:
                self.socket_link.close()
            except AttributeError:
                pass
            event.accept()
        else:
            event.ignore()

    def onOpenSocket(self):
        ip = self.HOST_IP_lineEdit.text()
        portnum = self.port_num_lineEdit.text()
        type = self.socket_type_comboBox.currentText()
        self.socket_link = socket_operations.Socket(
            ip,
            portnum,
            type,
            self.updateStatusBar,
            self
        )
        try:
            self.socket_link.creat()
            self.stop_pushButton.setEnabled(True)
            self.open_pushButton.setDisabled(True)
        except OSError as err:
            self.updateStatusBar(str(err))


    def onCloseSocket(self):
        self.socket_link.close()
        self.open_pushButton.setEnabled(True)
        self.stop_pushButton.setDisabled(True)
        self.updateStatusBar("Socket Closed")



    def updateStatusBar(self, msg):
        self.statusBar.showMessage(msg)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    try:
        win.onOpenSocket()
    except:
        pass
    sys.exit(app.exec_())
