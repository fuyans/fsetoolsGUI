# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_0103_merging_flow.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(884, 697)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(35, 35, 35, 35)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(796, 566))
        self.widget.setMaximumSize(QSize(796, 566))
        self.pushButton_calculate = QPushButton(self.widget)
        self.pushButton_calculate.setObjectName(u"pushButton_calculate")
        self.pushButton_calculate.setGeometry(QRect(700, 540, 96, 26))
        self.pushButton_test = QPushButton(self.widget)
        self.pushButton_test.setObjectName(u"pushButton_test")
        self.pushButton_test.setGeometry(QRect(585, 540, 96, 26))
        self.label_image_context = QLabel(self.widget)
        self.label_image_context.setObjectName(u"label_image_context")
        self.label_image_context.setGeometry(QRect(0, 0, 796, 566))
        self.label_image_context.setPixmap(QPixmap(u"../../../../../../../Library/Mobile Documents/6LVTQB9699~com~seriflabs~affinitydesigner/Documents/FSEUTIL/png/0103_back_794_560.png"))
        self.groupBox_outputs = QGroupBox(self.widget)
        self.groupBox_outputs.setObjectName(u"groupBox_outputs")
        self.groupBox_outputs.setGeometry(QRect(400, 435, 391, 81))
        self.lineEdit_out_W_FE = QLineEdit(self.groupBox_outputs)
        self.lineEdit_out_W_FE.setObjectName(u"lineEdit_out_W_FE")
        self.lineEdit_out_W_FE.setGeometry(QRect(210, 50, 91, 21))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_out_W_FE.sizePolicy().hasHeightForWidth())
        self.lineEdit_out_W_FE.setSizePolicy(sizePolicy)
        self.lineEdit_out_W_FE.setMinimumSize(QSize(0, 0))
        self.lineEdit_out_W_FE.setMaximumSize(QSize(16777215, 16777215))
        self.label_12 = QLabel(self.groupBox_outputs)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 50, 181, 21))
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QSize(20, 0))
        self.label_12.setMaximumSize(QSize(16777215, 16777215))
        self.label_25 = QLabel(self.groupBox_outputs)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(315, 50, 51, 21))
        self.checkBox_out_check = QCheckBox(self.groupBox_outputs)
        self.checkBox_out_check.setObjectName(u"checkBox_out_check")
        self.checkBox_out_check.setGeometry(QRect(10, 25, 371, 21))
        self.groupBox_inputs = QGroupBox(self.widget)
        self.groupBox_inputs.setObjectName(u"groupBox_inputs")
        self.groupBox_inputs.setGeometry(QRect(400, 215, 396, 206))
        self.label_in_D_unit = QLabel(self.groupBox_inputs)
        self.label_in_D_unit.setObjectName(u"label_in_D_unit")
        self.label_in_D_unit.setGeometry(QRect(315, 100, 66, 21))
        self.label_in_D_unit.setMinimumSize(QSize(0, 0))
        self.label_in_D_unit.setMaximumSize(QSize(16777215, 16777215))
        self.label_in_N_unit = QLabel(self.groupBox_inputs)
        self.label_in_N_unit.setObjectName(u"label_in_N_unit")
        self.label_in_N_unit.setGeometry(QRect(315, 150, 66, 21))
        self.label_in_N_unit.setMinimumSize(QSize(0, 0))
        self.label_in_N_unit.setMaximumSize(QSize(16777215, 16777215))
        self.label_in_S_dn_unit = QLabel(self.groupBox_inputs)
        self.label_in_S_dn_unit.setObjectName(u"label_in_S_dn_unit")
        self.label_in_S_dn_unit.setGeometry(QRect(315, 50, 66, 21))
        self.label_in_S_dn_unit.setMinimumSize(QSize(0, 0))
        self.label_in_S_dn_unit.setMaximumSize(QSize(16777215, 16777215))
        self.label_in_S_up = QLabel(self.groupBox_inputs)
        self.label_in_S_up.setObjectName(u"label_in_S_up")
        self.label_in_S_up.setGeometry(QRect(315, 25, 66, 21))
        self.label_in_S_up.setMinimumSize(QSize(0, 0))
        self.label_in_S_up.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_in_S_up = QLineEdit(self.groupBox_inputs)
        self.lineEdit_in_S_up.setObjectName(u"lineEdit_in_S_up")
        self.lineEdit_in_S_up.setGeometry(QRect(210, 25, 91, 21))
        sizePolicy.setHeightForWidth(self.lineEdit_in_S_up.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_S_up.setSizePolicy(sizePolicy)
        self.lineEdit_in_S_up.setMinimumSize(QSize(0, 0))
        self.lineEdit_in_S_up.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_in_S_up.setBaseSize(QSize(0, 0))
        self.lineEdit_in_S_dn = QLineEdit(self.groupBox_inputs)
        self.lineEdit_in_S_dn.setObjectName(u"lineEdit_in_S_dn")
        self.lineEdit_in_S_dn.setGeometry(QRect(210, 50, 91, 21))
        sizePolicy.setHeightForWidth(self.lineEdit_in_S_dn.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_S_dn.setSizePolicy(sizePolicy)
        self.lineEdit_in_S_dn.setMinimumSize(QSize(0, 0))
        self.lineEdit_in_S_dn.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_in_S_dn.setBaseSize(QSize(0, 0))
        self.lineEdit_in_D = QLineEdit(self.groupBox_inputs)
        self.lineEdit_in_D.setObjectName(u"lineEdit_in_D")
        self.lineEdit_in_D.setGeometry(QRect(210, 100, 91, 21))
        sizePolicy.setHeightForWidth(self.lineEdit_in_D.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_D.setSizePolicy(sizePolicy)
        self.lineEdit_in_D.setMinimumSize(QSize(0, 0))
        self.lineEdit_in_D.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_in_D.setBaseSize(QSize(0, 0))
        self.lineEdit_in_N = QLineEdit(self.groupBox_inputs)
        self.lineEdit_in_N.setObjectName(u"lineEdit_in_N")
        self.lineEdit_in_N.setGeometry(QRect(210, 150, 91, 21))
        sizePolicy.setHeightForWidth(self.lineEdit_in_N.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_N.setSizePolicy(sizePolicy)
        self.lineEdit_in_N.setMinimumSize(QSize(0, 0))
        self.lineEdit_in_N.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_in_N.setBaseSize(QSize(0, 0))
        self.label_in_N = QLabel(self.groupBox_inputs)
        self.label_in_N.setObjectName(u"label_in_N")
        self.label_in_N.setGeometry(QRect(10, 150, 181, 21))
        sizePolicy.setHeightForWidth(self.label_in_N.sizePolicy().hasHeightForWidth())
        self.label_in_N.setSizePolicy(sizePolicy)
        self.label_in_N.setMinimumSize(QSize(0, 0))
        self.label_in_N.setMaximumSize(QSize(16777215, 16777215))
        self.label_in_S_dn = QLabel(self.groupBox_inputs)
        self.label_in_S_dn.setObjectName(u"label_in_S_dn")
        self.label_in_S_dn.setGeometry(QRect(10, 50, 181, 21))
        sizePolicy.setHeightForWidth(self.label_in_S_dn.sizePolicy().hasHeightForWidth())
        self.label_in_S_dn.setSizePolicy(sizePolicy)
        self.label_in_S_dn.setMinimumSize(QSize(0, 0))
        self.label_in_S_dn.setMaximumSize(QSize(16777215, 16777215))
        self.label_in_S_up_label = QLabel(self.groupBox_inputs)
        self.label_in_S_up_label.setObjectName(u"label_in_S_up_label")
        self.label_in_S_up_label.setGeometry(QRect(10, 25, 181, 21))
        self.label_in_S_up_label.setMinimumSize(QSize(0, 0))
        self.label_in_S_up_label.setMaximumSize(QSize(16777215, 16777215))
        self.label_in_B = QLabel(self.groupBox_inputs)
        self.label_in_B.setObjectName(u"label_in_B")
        self.label_in_B.setGeometry(QRect(10, 125, 181, 21))
        self.label_in_B.setMinimumSize(QSize(0, 0))
        self.label_in_B.setMaximumSize(QSize(16777215, 16777215))
        self.label_in_W_SE = QLabel(self.groupBox_inputs)
        self.label_in_W_SE.setObjectName(u"label_in_W_SE")
        self.label_in_W_SE.setGeometry(QRect(10, 75, 181, 21))
        self.label_in_W_SE.setMinimumSize(QSize(0, 0))
        self.label_in_W_SE.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_in_B = QLineEdit(self.groupBox_inputs)
        self.lineEdit_in_B.setObjectName(u"lineEdit_in_B")
        self.lineEdit_in_B.setGeometry(QRect(210, 125, 91, 21))
        sizePolicy.setHeightForWidth(self.lineEdit_in_B.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_B.setSizePolicy(sizePolicy)
        self.lineEdit_in_B.setMinimumSize(QSize(0, 0))
        self.lineEdit_in_B.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_in_B.setBaseSize(QSize(0, 0))
        self.lineEdit_in_W_SE = QLineEdit(self.groupBox_inputs)
        self.lineEdit_in_W_SE.setObjectName(u"lineEdit_in_W_SE")
        self.lineEdit_in_W_SE.setGeometry(QRect(210, 75, 91, 21))
        sizePolicy.setHeightForWidth(self.lineEdit_in_W_SE.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_W_SE.setSizePolicy(sizePolicy)
        self.lineEdit_in_W_SE.setMinimumSize(QSize(0, 0))
        self.lineEdit_in_W_SE.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_in_W_SE.setBaseSize(QSize(0, 0))
        self.label_in_B_unit = QLabel(self.groupBox_inputs)
        self.label_in_B_unit.setObjectName(u"label_in_B_unit")
        self.label_in_B_unit.setGeometry(QRect(315, 125, 66, 21))
        self.label_in_B_unit.setMinimumSize(QSize(0, 0))
        self.label_in_B_unit.setMaximumSize(QSize(16777215, 16777215))
        self.label_in_W_SE_unit = QLabel(self.groupBox_inputs)
        self.label_in_W_SE_unit.setObjectName(u"label_in_W_SE_unit")
        self.label_in_W_SE_unit.setGeometry(QRect(315, 75, 66, 21))
        self.label_in_W_SE_unit.setMinimumSize(QSize(0, 0))
        self.label_in_W_SE_unit.setMaximumSize(QSize(16777215, 16777215))
        self.label_27 = QLabel(self.groupBox_inputs)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setGeometry(QRect(10, 100, 181, 21))
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        self.label_27.setMinimumSize(QSize(0, 0))
        self.label_27.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_in_X = QLineEdit(self.groupBox_inputs)
        self.lineEdit_in_X.setObjectName(u"lineEdit_in_X")
        self.lineEdit_in_X.setGeometry(QRect(210, 175, 91, 21))
        sizePolicy.setHeightForWidth(self.lineEdit_in_X.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_X.setSizePolicy(sizePolicy)
        self.lineEdit_in_X.setMinimumSize(QSize(0, 0))
        self.lineEdit_in_X.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_in_X.setBaseSize(QSize(0, 0))
        self.label_in_X_unit = QLabel(self.groupBox_inputs)
        self.label_in_X_unit.setObjectName(u"label_in_X_unit")
        self.label_in_X_unit.setGeometry(QRect(315, 175, 66, 21))
        self.label_in_X_unit.setMinimumSize(QSize(0, 0))
        self.label_in_X_unit.setMaximumSize(QSize(16777215, 16777215))
        self.label_28 = QLabel(self.groupBox_inputs)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setGeometry(QRect(10, 175, 181, 21))
        sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        self.label_28.setMinimumSize(QSize(0, 0))
        self.label_28.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_options = QGroupBox(self.widget)
        self.groupBox_options.setObjectName(u"groupBox_options")
        self.groupBox_options.setGeometry(QRect(400, 100, 396, 101))
        self.radioButton_opt_scenario_1 = QRadioButton(self.groupBox_options)
        self.radioButton_opt_scenario_1.setObjectName(u"radioButton_opt_scenario_1")
        self.radioButton_opt_scenario_1.setGeometry(QRect(15, 25, 356, 18))
        self.radioButton_opt_scenario_2 = QRadioButton(self.groupBox_options)
        self.radioButton_opt_scenario_2.setObjectName(u"radioButton_opt_scenario_2")
        self.radioButton_opt_scenario_2.setGeometry(QRect(15, 50, 351, 18))
        self.radioButton_opt_scenario_3 = QRadioButton(self.groupBox_options)
        self.radioButton_opt_scenario_3.setObjectName(u"radioButton_opt_scenario_3")
        self.radioButton_opt_scenario_3.setGeometry(QRect(15, 75, 361, 18))
        self.label_image_figure = QLabel(self.widget)
        self.label_image_figure.setObjectName(u"label_image_figure")
        self.label_image_figure.setGeometry(QRect(0, 80, 342, 284))
        self.label_image_figure.setPixmap(QPixmap(u"../../../../../../../Library/Mobile Documents/6LVTQB9699~com~seriflabs~affinitydesigner/Documents/FSEUTIL/png/0103_figure_1_342_284.png"))
        self.label_image_context.raise_()
        self.pushButton_calculate.raise_()
        self.pushButton_test.raise_()
        self.groupBox_outputs.raise_()
        self.groupBox_inputs.raise_()
        self.groupBox_options.raise_()
        self.label_image_figure.raise_()

        self.verticalLayout.addWidget(self.widget)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 884, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.radioButton_opt_scenario_1, self.radioButton_opt_scenario_2)
        QWidget.setTabOrder(self.radioButton_opt_scenario_2, self.radioButton_opt_scenario_3)
        QWidget.setTabOrder(self.radioButton_opt_scenario_3, self.lineEdit_in_S_up)
        QWidget.setTabOrder(self.lineEdit_in_S_up, self.lineEdit_in_S_dn)
        QWidget.setTabOrder(self.lineEdit_in_S_dn, self.lineEdit_in_W_SE)
        QWidget.setTabOrder(self.lineEdit_in_W_SE, self.lineEdit_in_D)
        QWidget.setTabOrder(self.lineEdit_in_D, self.lineEdit_in_B)
        QWidget.setTabOrder(self.lineEdit_in_B, self.lineEdit_in_N)
        QWidget.setTabOrder(self.lineEdit_in_N, self.lineEdit_in_X)
        QWidget.setTabOrder(self.lineEdit_in_X, self.checkBox_out_check)
        QWidget.setTabOrder(self.checkBox_out_check, self.lineEdit_out_W_FE)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.pushButton_calculate.setToolTip(QCoreApplication.translate("MainWindow", u"Click (or press Enter) to calculate.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_calculate.setStatusTip(QCoreApplication.translate("MainWindow", u"Click (or press Enter) to calculate.", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_calculate.setText(QCoreApplication.translate("MainWindow", u"Calculate", None))
#if QT_CONFIG(tooltip)
        self.pushButton_test.setToolTip(QCoreApplication.translate("MainWindow", u"Click to generate example input parameters.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_test.setStatusTip(QCoreApplication.translate("MainWindow", u"Click to generate example input parameters.", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_test.setText(QCoreApplication.translate("MainWindow", u"Example", None))
        self.label_image_context.setText("")
        self.groupBox_outputs.setTitle(QCoreApplication.translate("MainWindow", u"Outputs", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_out_W_FE.setToolTip(QCoreApplication.translate("MainWindow", u"Solved minimum final exit door width. Double click to select the value.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lineEdit_out_W_FE.setStatusTip(QCoreApplication.translate("MainWindow", u"Solved minimum final exit door width. Double click to select the value.", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(tooltip)
        self.label_12.setToolTip(QCoreApplication.translate("MainWindow", u"Solved minimum final exit door width.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_12.setStatusTip(QCoreApplication.translate("MainWindow", u"Solved minimum final exit door width.", None))
#endif // QT_CONFIG(statustip)
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>W<span style=\" vertical-align:sub;\">FE</span>, calculated final exit width</p></body></html>", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"mm", None))
#if QT_CONFIG(tooltip)
        self.checkBox_out_check.setToolTip(QCoreApplication.translate("MainWindow", u"This indicates whether the condition True (ticked) or False.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.checkBox_out_check.setStatusTip(QCoreApplication.translate("MainWindow", u"This indicates whether the condition True (ticked) or False.", None))
#endif // QT_CONFIG(statustip)
        self.checkBox_out_check.setText(QCoreApplication.translate("MainWindow", u"Check if \"(B+N)>60 and D<2\" is True.", None))
        self.groupBox_inputs.setTitle(QCoreApplication.translate("MainWindow", u"Inputs", None))
        self.label_in_D_unit.setText(QCoreApplication.translate("MainWindow", u"m", None))
        self.label_in_N_unit.setText(QCoreApplication.translate("MainWindow", u"person", None))
        self.label_in_S_dn_unit.setText(QCoreApplication.translate("MainWindow", u"mm", None))
        self.label_in_S_up.setText(QCoreApplication.translate("MainWindow", u"mm", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_in_S_up.setToolTip(QCoreApplication.translate("MainWindow", u"Positive float. Width of the stair to upper levels.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lineEdit_in_S_up.setStatusTip(QCoreApplication.translate("MainWindow", u"Positive float. Width of the stair to upper levels.", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(tooltip)
        self.lineEdit_in_S_dn.setToolTip(QCoreApplication.translate("MainWindow", u"Positive float. Width of the stair to lower (basement) levels.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lineEdit_in_S_dn.setStatusTip(QCoreApplication.translate("MainWindow", u"Positive float. Width of the stair to lower (basement) levels.", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(tooltip)
        self.lineEdit_in_D.setToolTip(QCoreApplication.translate("MainWindow", u"Positive float. Distance between building final exit to door of ground level or lower stair.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lineEdit_in_D.setStatusTip(QCoreApplication.translate("MainWindow", u"Positive float. Distance between building final exit to door of ground level or lower stair.", None))
#endif // QT_CONFIG(statustip)
        self.lineEdit_in_D.setText("")
#if QT_CONFIG(tooltip)
        self.lineEdit_in_N.setToolTip(QCoreApplication.translate("MainWindow", u"Positive integer. Number of persons from ground level.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lineEdit_in_N.setStatusTip(QCoreApplication.translate("MainWindow", u"Positive integer. Number of persons from ground level.", None))
#endif // QT_CONFIG(statustip)
        self.lineEdit_in_N.setText("")
#if QT_CONFIG(tooltip)
        self.label_in_N.setToolTip(QCoreApplication.translate("MainWindow", u"Number of persons from ground level.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_in_N.setStatusTip(QCoreApplication.translate("MainWindow", u"Number of persons from ground level.", None))
#endif // QT_CONFIG(statustip)
        self.label_in_N.setText(QCoreApplication.translate("MainWindow", u"N, no. persons from find ext. level", None))
#if QT_CONFIG(tooltip)
        self.label_in_S_dn.setToolTip(QCoreApplication.translate("MainWindow", u"Width of the stair to lower (basement) levels.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_in_S_dn.setStatusTip(QCoreApplication.translate("MainWindow", u"Width of the stair to lower (basement) levels.", None))
#endif // QT_CONFIG(statustip)
        self.label_in_S_dn.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>S<span style=\" vertical-align:sub;\">dn</span>, stair width to lower levels</p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.label_in_S_up_label.setToolTip(QCoreApplication.translate("MainWindow", u"Width of the stair to upper levels.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_in_S_up_label.setStatusTip(QCoreApplication.translate("MainWindow", u"Width of the stair to upper levels.", None))
#endif // QT_CONFIG(statustip)
        self.label_in_S_up_label.setText(QCoreApplication.translate("MainWindow", u"S<sub>up</sub>, stair width to upper level(s)", None))
#if QT_CONFIG(tooltip)
        self.label_in_B.setToolTip(QCoreApplication.translate("MainWindow", u"Number of persons from lower (basement) level(s).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_in_B.setStatusTip(QCoreApplication.translate("MainWindow", u"Number of persons from lower (basement) level(s).", None))
#endif // QT_CONFIG(statustip)
        self.label_in_B.setText(QCoreApplication.translate("MainWindow", u"B, no. persons from basement lev.", None))
#if QT_CONFIG(tooltip)
        self.label_in_W_SE.setToolTip(QCoreApplication.translate("MainWindow", u"Width of the door from final exit level.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_in_W_SE.setStatusTip(QCoreApplication.translate("MainWindow", u"Width of the door from final exit level.", None))
#endif // QT_CONFIG(statustip)
        self.label_in_W_SE.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>W<span style=\" vertical-align:sub;\">SE</span>, door width from final exit level</p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_in_B.setToolTip(QCoreApplication.translate("MainWindow", u"Positive integer. Number of persons from lower (basement) level.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lineEdit_in_B.setStatusTip(QCoreApplication.translate("MainWindow", u"Positive integer. Number of persons from lower (basement) level.", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(tooltip)
        self.lineEdit_in_W_SE.setToolTip(QCoreApplication.translate("MainWindow", u"Positive float. Width of the door from final exit level.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lineEdit_in_W_SE.setStatusTip(QCoreApplication.translate("MainWindow", u"Positive float. Width of the door from final exit level.", None))
#endif // QT_CONFIG(statustip)
        self.lineEdit_in_W_SE.setText("")
        self.label_in_B_unit.setText(QCoreApplication.translate("MainWindow", u"person", None))
        self.label_in_W_SE_unit.setText(QCoreApplication.translate("MainWindow", u"mm", None))
#if QT_CONFIG(tooltip)
        self.label_27.setToolTip(QCoreApplication.translate("MainWindow", u"Distance between building final exit to door of ground level or lower stair.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_27.setStatusTip(QCoreApplication.translate("MainWindow", u"Distance between building final exit to door of ground level or lower stair.", None))
#endif // QT_CONFIG(statustip)
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"D, distance indicated points", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_in_X.setToolTip(QCoreApplication.translate("MainWindow", u"Positive float. Minimum door width per person.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lineEdit_in_X.setStatusTip(QCoreApplication.translate("MainWindow", u"Positive float. Minimum door width per person.", None))
#endif // QT_CONFIG(statustip)
        self.lineEdit_in_X.setText("")
        self.label_in_X_unit.setText(QCoreApplication.translate("MainWindow", u"mm/pers.", None))
#if QT_CONFIG(tooltip)
        self.label_28.setToolTip(QCoreApplication.translate("MainWindow", u"Minimum door width per person.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_28.setStatusTip(QCoreApplication.translate("MainWindow", u"Minimum door width per person.", None))
#endif // QT_CONFIG(statustip)
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"X, exit factor", None))
        self.groupBox_options.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
#if QT_CONFIG(tooltip)
        self.radioButton_opt_scenario_1.setToolTip(QCoreApplication.translate("MainWindow", u"Scenario 1. Building final exit serves flow from upper levels and ground level.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.radioButton_opt_scenario_1.setStatusTip(QCoreApplication.translate("MainWindow", u"Scenario 1. Building final exit serves flow from upper levels and ground level.", None))
#endif // QT_CONFIG(statustip)
        self.radioButton_opt_scenario_1.setText(QCoreApplication.translate("MainWindow", u"Scenario 1. Flow from upper and final exit levels.", None))
#if QT_CONFIG(tooltip)
        self.radioButton_opt_scenario_2.setToolTip(QCoreApplication.translate("MainWindow", u"Scenario 2. Building final exit serves flow from upper levels and lower (basement) levels.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.radioButton_opt_scenario_2.setStatusTip(QCoreApplication.translate("MainWindow", u"Scenario 2. Building final exit serves flow from upper levels and lower (basement) levels.", None))
#endif // QT_CONFIG(statustip)
        self.radioButton_opt_scenario_2.setText(QCoreApplication.translate("MainWindow", u"Scenario 2. Flow from upper and basement levels.", None))
#if QT_CONFIG(tooltip)
        self.radioButton_opt_scenario_3.setToolTip(QCoreApplication.translate("MainWindow", u"Scenario 3. Building final exit serves flow from upper levels, lower (basement) levels and ground level.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.radioButton_opt_scenario_3.setStatusTip(QCoreApplication.translate("MainWindow", u"Scenario 3. Building final exit serves flow from upper levels, lower (basement) levels and ground level.", None))
#endif // QT_CONFIG(statustip)
        self.radioButton_opt_scenario_3.setText(QCoreApplication.translate("MainWindow", u"Scenario 3. Flow from upper, lower and final exit levels.", None))
        self.label_image_figure.setText("")
    # retranslateUi

