# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_0406_tra_2d_xy_contour.ui'
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
        MainWindow.resize(1076, 744)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_plot = QVBoxLayout()
        self.verticalLayout_plot.setObjectName(u"verticalLayout_plot")
        self.verticalLayout_plot.setSizeConstraint(QLayout.SetMinimumSize)

        self.gridLayout.addLayout(self.verticalLayout_plot, 0, 0, 1, 1)

        self.verticalLayout_control = QVBoxLayout()
        self.verticalLayout_control.setObjectName(u"verticalLayout_control")
        self.verticalLayout_control.setSizeConstraint(QLayout.SetMinimumSize)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(396, 160))
        self.groupBox.setMaximumSize(QSize(396, 160))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(25, 40, 181, 26))
        self.label.setMinimumSize(QSize(150, 0))
        self.label.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_graphic_critical_heat_flux = QLineEdit(self.groupBox)
        self.lineEdit_graphic_critical_heat_flux.setObjectName(u"lineEdit_graphic_critical_heat_flux")
        self.lineEdit_graphic_critical_heat_flux.setGeometry(QRect(215, 40, 91, 26))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(25, 75, 181, 26))
        self.label_2.setMinimumSize(QSize(0, 0))
        self.label_2.setMaximumSize(QSize(16777215, 16777215))
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(25, 110, 181, 26))
        self.horizontalSlider_graphic_line_thickness = QSlider(self.groupBox)
        self.horizontalSlider_graphic_line_thickness.setObjectName(u"horizontalSlider_graphic_line_thickness")
        self.horizontalSlider_graphic_line_thickness.setGeometry(QRect(215, 110, 91, 26))
        self.horizontalSlider_graphic_line_thickness.setMinimum(0)
        self.horizontalSlider_graphic_line_thickness.setMaximum(10)
        self.horizontalSlider_graphic_line_thickness.setValue(5)
        self.horizontalSlider_graphic_line_thickness.setOrientation(Qt.Horizontal)
        self.horizontalSlider_graphic_line_thickness.setInvertedAppearance(False)
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(315, 40, 51, 26))
        self.label_7.setMinimumSize(QSize(0, 0))
        self.label_7.setMaximumSize(QSize(16777215, 16777215))
        self.label_graphic_contour_label_font_size = QLabel(self.groupBox)
        self.label_graphic_contour_label_font_size.setObjectName(u"label_graphic_contour_label_font_size")
        self.label_graphic_contour_label_font_size.setGeometry(QRect(315, 75, 51, 26))
        self.label_graphic_contour_label_font_size.setMinimumSize(QSize(0, 0))
        self.label_graphic_contour_label_font_size.setMaximumSize(QSize(16777215, 16777215))
        self.label_graphic_line_thickness = QLabel(self.groupBox)
        self.label_graphic_line_thickness.setObjectName(u"label_graphic_line_thickness")
        self.label_graphic_line_thickness.setGeometry(QRect(315, 110, 51, 26))
        self.label_graphic_line_thickness.setMinimumSize(QSize(0, 0))
        self.label_graphic_line_thickness.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalSlider_graphic_contour_font_size = QSlider(self.groupBox)
        self.horizontalSlider_graphic_contour_font_size.setObjectName(u"horizontalSlider_graphic_contour_font_size")
        self.horizontalSlider_graphic_contour_font_size.setGeometry(QRect(215, 75, 91, 26))
        self.horizontalSlider_graphic_contour_font_size.setMinimum(0)
        self.horizontalSlider_graphic_contour_font_size.setMaximum(20)
        self.horizontalSlider_graphic_contour_font_size.setValue(12)
        self.horizontalSlider_graphic_contour_font_size.setOrientation(Qt.Horizontal)
        self.horizontalSlider_graphic_contour_font_size.setInvertedAppearance(False)

        self.verticalLayout_control.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(396, 441))
        self.groupBox_2.setMaximumSize(QSize(396, 441))
        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(25, 40, 86, 26))
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(25, 75, 86, 26))
        self.lineEdit_solver_x = QLineEdit(self.groupBox_2)
        self.lineEdit_solver_x.setObjectName(u"lineEdit_solver_x")
        self.lineEdit_solver_x.setGeometry(QRect(110, 40, 61, 26))
        self.lineEdit_solver_z = QLineEdit(self.groupBox_2)
        self.lineEdit_solver_z.setObjectName(u"lineEdit_solver_z")
        self.lineEdit_solver_z.setGeometry(QRect(310, 75, 61, 26))
        self.lineEdit_solver_y = QLineEdit(self.groupBox_2)
        self.lineEdit_solver_y.setObjectName(u"lineEdit_solver_y")
        self.lineEdit_solver_y.setGeometry(QRect(310, 40, 61, 26))
        self.lineEdit_solver_delta = QLineEdit(self.groupBox_2)
        self.lineEdit_solver_delta.setObjectName(u"lineEdit_solver_delta")
        self.lineEdit_solver_delta.setGeometry(QRect(110, 75, 61, 26))
        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(225, 75, 86, 26))
        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(225, 40, 86, 26))
        self.tableView_emitters = QTableView(self.groupBox_2)
        self.tableView_emitters.setObjectName(u"tableView_emitters")
        self.tableView_emitters.setGeometry(QRect(25, 140, 346, 116))
        self.tableView_emitters.setMaximumSize(QSize(396, 16777215))
        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(25, 110, 86, 26))
        self.pushButton_emitter_list_append = QPushButton(self.groupBox_2)
        self.pushButton_emitter_list_append.setObjectName(u"pushButton_emitter_list_append")
        self.pushButton_emitter_list_append.setGeometry(QRect(105, 110, 36, 26))
        self.pushButton_emitter_list_remove = QPushButton(self.groupBox_2)
        self.pushButton_emitter_list_remove.setObjectName(u"pushButton_emitter_list_remove")
        self.pushButton_emitter_list_remove.setGeometry(QRect(140, 110, 36, 26))
        self.tableView_receivers = QTableView(self.groupBox_2)
        self.tableView_receivers.setObjectName(u"tableView_receivers")
        self.tableView_receivers.setGeometry(QRect(25, 295, 221, 116))
        self.tableView_receivers.setMaximumSize(QSize(396, 16777215))
        self.pushButton_receiver_list_remove = QPushButton(self.groupBox_2)
        self.pushButton_receiver_list_remove.setObjectName(u"pushButton_receiver_list_remove")
        self.pushButton_receiver_list_remove.setGeometry(QRect(140, 265, 36, 26))
        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(25, 265, 86, 26))
        self.pushButton_receiver_list_append = QPushButton(self.groupBox_2)
        self.pushButton_receiver_list_append.setObjectName(u"pushButton_receiver_list_append")
        self.pushButton_receiver_list_append.setGeometry(QRect(105, 265, 36, 26))

        self.verticalLayout_control.addWidget(self.groupBox_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 1)
        self.pushButton_example = QPushButton(self.centralwidget)
        self.pushButton_example.setObjectName(u"pushButton_example")
        self.pushButton_example.setMinimumSize(QSize(96, 26))
        self.pushButton_example.setMaximumSize(QSize(96, 26))

        self.horizontalLayout_2.addWidget(self.pushButton_example)

        self.pushButton_refresh = QPushButton(self.centralwidget)
        self.pushButton_refresh.setObjectName(u"pushButton_refresh")
        self.pushButton_refresh.setMinimumSize(QSize(96, 26))
        self.pushButton_refresh.setMaximumSize(QSize(96, 26))

        self.horizontalLayout_2.addWidget(self.pushButton_refresh)

        self.pushButton_save_figure = QPushButton(self.centralwidget)
        self.pushButton_save_figure.setObjectName(u"pushButton_save_figure")
        self.pushButton_save_figure.setMinimumSize(QSize(96, 26))
        self.pushButton_save_figure.setMaximumSize(QSize(96, 26))

        self.horizontalLayout_2.addWidget(self.pushButton_save_figure)

        self.pushButton_submit = QPushButton(self.centralwidget)
        self.pushButton_submit.setObjectName(u"pushButton_submit")
        self.pushButton_submit.setMinimumSize(QSize(96, 26))
        self.pushButton_submit.setMaximumSize(QSize(96, 26))

        self.horizontalLayout_2.addWidget(self.pushButton_submit)


        self.verticalLayout_control.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_control.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QSize(296, 26))
        self.progressBar.setMaximumSize(QSize(99999, 26))
        self.progressBar.setValue(0)

        self.horizontalLayout.addWidget(self.progressBar)


        self.verticalLayout_control.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout_control, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1076, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Graphic Options", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Critical heat flux", None))
        self.lineEdit_graphic_critical_heat_flux.setText(QCoreApplication.translate("MainWindow", u"12.6", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Contour Label Font Size", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"E. / R. Element Thickness", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"kW/m<sup>2<sup>", None))
        self.label_graphic_contour_label_font_size.setText(QCoreApplication.translate("MainWindow", u"12 pt", None))
        self.label_graphic_line_thickness.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Solver Inputs", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Domain X", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Resolution", None))
        self.lineEdit_solver_x.setText("")
        self.lineEdit_solver_z.setText("")
        self.lineEdit_solver_y.setText("")
        self.lineEdit_solver_delta.setText("")
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Domain Z", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Domain Y", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Emitters", None))
        self.pushButton_emitter_list_append.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.pushButton_emitter_list_remove.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.pushButton_receiver_list_remove.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Receivers", None))
        self.pushButton_receiver_list_append.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.pushButton_example.setText(QCoreApplication.translate("MainWindow", u"Example", None))
        self.pushButton_refresh.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.pushButton_save_figure.setText(QCoreApplication.translate("MainWindow", u"Save Figure", None))
        self.pushButton_submit.setText(QCoreApplication.translate("MainWindow", u"Submit", None))
    # retranslateUi

