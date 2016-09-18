# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1600, 800)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setAcceptDrops(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/form.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAnimated(False)
        MainWindow.setTabShape(QtGui.QTabWidget.Triangular)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.settings_groupBox = QtGui.QGroupBox(self.centralWidget)
        self.settings_groupBox.setGeometry(QtCore.QRect(10, 10, 271, 221))
        self.settings_groupBox.setObjectName(_fromUtf8("settings_groupBox"))
        self.layoutWidget = QtGui.QWidget(self.settings_groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 241, 191))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout_2.setContentsMargins(10, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(5)
        self.gridLayout_2.setVerticalSpacing(15)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.Port_num_comboBox = QtGui.QComboBox(self.layoutWidget)
        self.Port_num_comboBox.setMinimumSize(QtCore.QSize(110, 0))
        self.Port_num_comboBox.setMaximumSize(QtCore.QSize(110, 20))
        self.Port_num_comboBox.setObjectName(_fromUtf8("Port_num_comboBox"))
        self.gridLayout_2.addWidget(self.Port_num_comboBox, 0, 1, 1, 1)
        self.HOSI_IP_Label = QtGui.QLabel(self.layoutWidget)
        self.HOSI_IP_Label.setObjectName(_fromUtf8("HOSI_IP_Label"))
        self.gridLayout_2.addWidget(self.HOSI_IP_Label, 1, 0, 1, 1)
        self.BaudRate_lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.BaudRate_lineEdit.setMaximumSize(QtCore.QSize(110, 20))
        self.BaudRate_lineEdit.setObjectName(_fromUtf8("BaudRate_lineEdit"))
        self.gridLayout_2.addWidget(self.BaudRate_lineEdit, 1, 1, 1, 1)
        self.record_data_checkBox = QtGui.QCheckBox(self.layoutWidget)
        self.record_data_checkBox.setObjectName(_fromUtf8("record_data_checkBox"))
        self.gridLayout_2.addWidget(self.record_data_checkBox, 2, 0, 1, 1)
        self.open_data_pushButton = QtGui.QPushButton(self.layoutWidget)
        self.open_data_pushButton.setMinimumSize(QtCore.QSize(110, 28))
        self.open_data_pushButton.setMaximumSize(QtCore.QSize(110, 28))
        self.open_data_pushButton.setObjectName(_fromUtf8("open_data_pushButton"))
        self.gridLayout_2.addWidget(self.open_data_pushButton, 2, 1, 1, 1)
        self.open_pushButton = QtGui.QPushButton(self.layoutWidget)
        self.open_pushButton.setMinimumSize(QtCore.QSize(110, 28))
        self.open_pushButton.setMaximumSize(QtCore.QSize(110, 28))
        self.open_pushButton.setObjectName(_fromUtf8("open_pushButton"))
        self.gridLayout_2.addWidget(self.open_pushButton, 3, 0, 1, 1)
        self.socket_type_label = QtGui.QLabel(self.layoutWidget)
        self.socket_type_label.setObjectName(_fromUtf8("socket_type_label"))
        self.gridLayout_2.addWidget(self.socket_type_label, 0, 0, 1, 1)
        self.stop_pushButton = QtGui.QPushButton(self.layoutWidget)
        self.stop_pushButton.setMinimumSize(QtCore.QSize(110, 28))
        self.stop_pushButton.setMaximumSize(QtCore.QSize(110, 28))
        self.stop_pushButton.setObjectName(_fromUtf8("stop_pushButton"))
        self.gridLayout_2.addWidget(self.stop_pushButton, 3, 1, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 330, 271, 241))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget1 = QtGui.QWidget(self.groupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(12, 32, 231, 199))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.acc_x_Label = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(14)
        font.setItalic(False)
        self.acc_x_Label.setFont(font)
        self.acc_x_Label.setText(_fromUtf8(""))
        self.acc_x_Label.setObjectName(_fromUtf8("acc_x_Label"))
        self.gridLayout.addWidget(self.acc_x_Label, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.acc_y_Label = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(14)
        font.setItalic(False)
        self.acc_y_Label.setFont(font)
        self.acc_y_Label.setText(_fromUtf8(""))
        self.acc_y_Label.setObjectName(_fromUtf8("acc_y_Label"))
        self.gridLayout.addWidget(self.acc_y_Label, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.acc_z_Label = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(14)
        font.setItalic(False)
        self.acc_z_Label.setFont(font)
        self.acc_z_Label.setText(_fromUtf8(""))
        self.acc_z_Label.setObjectName(_fromUtf8("acc_z_Label"))
        self.gridLayout.addWidget(self.acc_z_Label, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.gyo_x_Label = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(14)
        font.setItalic(False)
        self.gyo_x_Label.setFont(font)
        self.gyo_x_Label.setText(_fromUtf8(""))
        self.gyo_x_Label.setObjectName(_fromUtf8("gyo_x_Label"))
        self.gridLayout.addWidget(self.gyo_x_Label, 3, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.gyo_y_Label = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(14)
        font.setItalic(False)
        self.gyo_y_Label.setFont(font)
        self.gyo_y_Label.setText(_fromUtf8(""))
        self.gyo_y_Label.setObjectName(_fromUtf8("gyo_y_Label"))
        self.gridLayout.addWidget(self.gyo_y_Label, 4, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.gyo_z_Label = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(14)
        font.setItalic(False)
        self.gyo_z_Label.setFont(font)
        self.gyo_z_Label.setText(_fromUtf8(""))
        self.gyo_z_Label.setObjectName(_fromUtf8("gyo_z_Label"))
        self.gridLayout.addWidget(self.gyo_z_Label, 5, 1, 1, 1)
        self.groupBox_4 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 220, 271, 111))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.layoutWidget2 = QtGui.QWidget(self.groupBox_4)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 20, 236, 81))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.layoutWidget2)
        self.gridLayout_3.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout_3.setContentsMargins(10, 11, 11, 11)
        self.gridLayout_3.setHorizontalSpacing(5)
        self.gridLayout_3.setVerticalSpacing(15)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalSlider = QtGui.QSlider(self.layoutWidget2)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.gridLayout_3.addWidget(self.horizontalSlider, 0, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.layoutWidget2)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        self.canvas_start_pushButton = QtGui.QPushButton(self.layoutWidget2)
        self.canvas_start_pushButton.setMinimumSize(QtCore.QSize(110, 28))
        self.canvas_start_pushButton.setMaximumSize(QtCore.QSize(110, 28))
        self.canvas_start_pushButton.setObjectName(_fromUtf8("canvas_start_pushButton"))
        self.gridLayout_3.addWidget(self.canvas_start_pushButton, 1, 0, 1, 1)
        self.canvas_pause_pushButton = QtGui.QPushButton(self.layoutWidget2)
        self.canvas_pause_pushButton.setMinimumSize(QtCore.QSize(110, 28))
        self.canvas_pause_pushButton.setMaximumSize(QtCore.QSize(110, 28))
        self.canvas_pause_pushButton.setObjectName(_fromUtf8("canvas_pause_pushButton"))
        self.gridLayout_3.addWidget(self.canvas_pause_pushButton, 1, 1, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_2.setEnabled(True)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 580, 271, 151))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.layoutWidget3 = QtGui.QWidget(self.groupBox_2)
        self.layoutWidget3.setGeometry(QtCore.QRect(20, 10, 231, 141))
        self.layoutWidget3.setObjectName(_fromUtf8("layoutWidget3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.layoutWidget3)
        self.gridLayout_4.setMargin(11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.x_legend_label = QtGui.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Yu Gothic UI Semibold"))
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.x_legend_label.setFont(font)
        self.x_legend_label.setMouseTracking(False)
        self.x_legend_label.setWordWrap(False)
        self.x_legend_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextEditable)
        self.x_legend_label.setObjectName(_fromUtf8("x_legend_label"))
        self.gridLayout_4.addWidget(self.x_legend_label, 0, 0, 1, 1)
        self.y_legend_label = QtGui.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Yu Gothic UI Semibold"))
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.y_legend_label.setFont(font)
        self.y_legend_label.setMouseTracking(False)
        self.y_legend_label.setWordWrap(False)
        self.y_legend_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextEditable)
        self.y_legend_label.setObjectName(_fromUtf8("y_legend_label"))
        self.gridLayout_4.addWidget(self.y_legend_label, 1, 0, 1, 1)
        self.z_legend_label = QtGui.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Yu Gothic UI Semibold"))
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.z_legend_label.setFont(font)
        self.z_legend_label.setMouseTracking(False)
        self.z_legend_label.setWordWrap(False)
        self.z_legend_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextEditable)
        self.z_legend_label.setObjectName(_fromUtf8("z_legend_label"))
        self.gridLayout_4.addWidget(self.z_legend_label, 2, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        self.tabWidget.setGeometry(QtCore.QRect(290, 0, 1301, 731))
        self.tabWidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName(_fromUtf8("tab_1"))
        self.acc_groupBox = QtGui.QGroupBox(self.tab_1)
        self.acc_groupBox.setGeometry(QtCore.QRect(0, 0, 1311, 361))
        self.acc_groupBox.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.acc_groupBox.setAutoFillBackground(True)
        self.acc_groupBox.setObjectName(_fromUtf8("acc_groupBox"))
        self.gyo_groupBox = QtGui.QGroupBox(self.tab_1)
        self.gyo_groupBox.setGeometry(QtCore.QRect(0, 360, 1311, 351))
        self.gyo_groupBox.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.gyo_groupBox.setAutoFillBackground(True)
        self.gyo_groupBox.setObjectName(_fromUtf8("gyo_groupBox"))
        self.tabWidget.addTab(self.tab_1, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.frame = QtGui.QFrame(self.tab_2)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1311, 711))
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.result_label = QtGui.QLabel(self.frame)
        self.result_label.setGeometry(QtCore.QRect(420, 180, 681, 261))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("黑体"))
        font.setPointSize(72)
        self.result_label.setFont(font)
        self.result_label.setObjectName(_fromUtf8("result_label"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.groupBox_3 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 580, 261, 80))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.layoutWidget4 = QtGui.QWidget(self.groupBox_3)
        self.layoutWidget4.setGeometry(QtCore.QRect(10, 20, 241, 51))
        self.layoutWidget4.setObjectName(_fromUtf8("layoutWidget4"))
        self.gridLayout_6 = QtGui.QGridLayout(self.layoutWidget4)
        self.gridLayout_6.setMargin(11)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.algorithm_pushButton = QtGui.QPushButton(self.layoutWidget4)
        self.algorithm_pushButton.setObjectName(_fromUtf8("algorithm_pushButton"))
        self.gridLayout_6.addWidget(self.algorithm_pushButton, 0, 0, 1, 1)
        self.calibrate_pushButton = QtGui.QPushButton(self.layoutWidget4)
        self.calibrate_pushButton.setObjectName(_fromUtf8("calibrate_pushButton"))
        self.gridLayout_6.addWidget(self.calibrate_pushButton, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1600, 26))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionExit = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("icons/exit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon1)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionExit)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.Port_num_comboBox, self.BaudRate_lineEdit)
        MainWindow.setTabOrder(self.BaudRate_lineEdit, self.record_data_checkBox)
        MainWindow.setTabOrder(self.record_data_checkBox, self.open_data_pushButton)
        MainWindow.setTabOrder(self.open_data_pushButton, self.open_pushButton)
        MainWindow.setTabOrder(self.open_pushButton, self.stop_pushButton)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "小虾米", None))
        self.settings_groupBox.setTitle(_translate("MainWindow", "UART Settings", None))
        self.HOSI_IP_Label.setText(_translate("MainWindow", "Baud Rate", None))
        self.record_data_checkBox.setText(_translate("MainWindow", "Record Data", None))
        self.open_data_pushButton.setText(_translate("MainWindow", "Open Data", None))
        self.open_pushButton.setText(_translate("MainWindow", "UART Open", None))
        self.socket_type_label.setText(_translate("MainWindow", "Serial Port", None))
        self.stop_pushButton.setText(_translate("MainWindow", "UART Stop", None))
        self.groupBox.setTitle(_translate("MainWindow", "Display", None))
        self.label.setText(_translate("MainWindow", "ACC-X:", None))
        self.label_2.setText(_translate("MainWindow", "ACC-Y:", None))
        self.label_3.setText(_translate("MainWindow", "ACC-Z:", None))
        self.label_4.setText(_translate("MainWindow", "GYO-X:", None))
        self.label_5.setText(_translate("MainWindow", "GYO-Y:", None))
        self.label_6.setText(_translate("MainWindow", "GYO-Z:", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "Canvas Settings", None))
        self.label_7.setText(_translate("MainWindow", "Scale:", None))
        self.canvas_start_pushButton.setText(_translate("MainWindow", "Canvas Start", None))
        self.canvas_pause_pushButton.setText(_translate("MainWindow", "Canvas Pause", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Legend", None))
        self.x_legend_label.setText(_translate("MainWindow", "X:----------", None))
        self.y_legend_label.setText(_translate("MainWindow", "y:----------", None))
        self.z_legend_label.setText(_translate("MainWindow", "Z:----------", None))
        self.acc_groupBox.setTitle(_translate("MainWindow", "ACC", None))
        self.gyo_groupBox.setTitle(_translate("MainWindow", "GYO", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "Live", None))
        self.result_label.setText(_translate("MainWindow", "井盖正常", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Algorithm", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Algorithm Settings", None))
        self.algorithm_pushButton.setText(_translate("MainWindow", "Start Monitor", None))
        self.calibrate_pushButton.setText(_translate("MainWindow", "Calibrate", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))

