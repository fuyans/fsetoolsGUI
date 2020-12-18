# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'i0630_safir_postprocessor.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(352, 685)
        MainWindow.setMinimumSize(QSize(90, 25))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(10)
        self.gridLayout_2.setVerticalSpacing(5)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.label_batch_run_description = QLabel(self.groupBox_2)
        self.label_batch_run_description.setObjectName(u"label_batch_run_description")
        self.label_batch_run_description.setWordWrap(True)

        self.gridLayout_2.addWidget(self.label_batch_run_description, 1, 0, 1, 3)

        self.lineEdit_batch_run_in_safir_input_folder = QLineEdit(self.groupBox_2)
        self.lineEdit_batch_run_in_safir_input_folder.setObjectName(u"lineEdit_batch_run_in_safir_input_folder")
        self.lineEdit_batch_run_in_safir_input_folder.setMinimumSize(QSize(100, 25))
        self.lineEdit_batch_run_in_safir_input_folder.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_2.addWidget(self.lineEdit_batch_run_in_safir_input_folder, 5, 1, 1, 1)

        self.label_batch_run_in_timeout_unit = QLabel(self.groupBox_2)
        self.label_batch_run_in_timeout_unit.setObjectName(u"label_batch_run_in_timeout_unit")

        self.gridLayout_2.addWidget(self.label_batch_run_in_timeout_unit, 4, 2, 1, 1)

        self.label_batch_run_in_timeout = QLabel(self.groupBox_2)
        self.label_batch_run_in_timeout.setObjectName(u"label_batch_run_in_timeout")
        self.label_batch_run_in_timeout.setMinimumSize(QSize(0, 25))
        self.label_batch_run_in_timeout.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_2.addWidget(self.label_batch_run_in_timeout, 4, 0, 1, 1)

        self.pushButton_batch_run_in_safir_exe_path = QPushButton(self.groupBox_2)
        self.pushButton_batch_run_in_safir_exe_path.setObjectName(u"pushButton_batch_run_in_safir_exe_path")
        self.pushButton_batch_run_in_safir_exe_path.setMinimumSize(QSize(0, 25))
        self.pushButton_batch_run_in_safir_exe_path.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_2.addWidget(self.pushButton_batch_run_in_safir_exe_path, 2, 2, 1, 1)

        self.label_batch_run_title = QLabel(self.groupBox_2)
        self.label_batch_run_title.setObjectName(u"label_batch_run_title")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(25)
        sizePolicy.setHeightForWidth(self.label_batch_run_title.sizePolicy().hasHeightForWidth())
        self.label_batch_run_title.setSizePolicy(sizePolicy)
        self.label_batch_run_title.setMinimumSize(QSize(0, 25))
        self.label_batch_run_title.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_2.addWidget(self.label_batch_run_title, 0, 0, 1, 3)

        self.lineEdit_batch_run_in_timeout = QLineEdit(self.groupBox_2)
        self.lineEdit_batch_run_in_timeout.setObjectName(u"lineEdit_batch_run_in_timeout")
        self.lineEdit_batch_run_in_timeout.setMinimumSize(QSize(0, 25))
        self.lineEdit_batch_run_in_timeout.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_2.addWidget(self.lineEdit_batch_run_in_timeout, 4, 1, 1, 1)

        self.label_batch_run_in_safir_exe_path = QLabel(self.groupBox_2)
        self.label_batch_run_in_safir_exe_path.setObjectName(u"label_batch_run_in_safir_exe_path")

        self.gridLayout_2.addWidget(self.label_batch_run_in_safir_exe_path, 2, 0, 1, 1)

        self.label_batch_run_in_safir_input_folder = QLabel(self.groupBox_2)
        self.label_batch_run_in_safir_input_folder.setObjectName(u"label_batch_run_in_safir_input_folder")

        self.gridLayout_2.addWidget(self.label_batch_run_in_safir_input_folder, 5, 0, 1, 1)

        self.lineEdit_batch_run_in_processes = QLineEdit(self.groupBox_2)
        self.lineEdit_batch_run_in_processes.setObjectName(u"lineEdit_batch_run_in_processes")
        self.lineEdit_batch_run_in_processes.setMinimumSize(QSize(0, 25))
        self.lineEdit_batch_run_in_processes.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_2.addWidget(self.lineEdit_batch_run_in_processes, 3, 1, 1, 1)

        self.lineEdit_batch_run_in_safir_exe_path = QLineEdit(self.groupBox_2)
        self.lineEdit_batch_run_in_safir_exe_path.setObjectName(u"lineEdit_batch_run_in_safir_exe_path")
        self.lineEdit_batch_run_in_safir_exe_path.setMinimumSize(QSize(100, 25))
        self.lineEdit_batch_run_in_safir_exe_path.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_2.addWidget(self.lineEdit_batch_run_in_safir_exe_path, 2, 1, 1, 1)

        self.pushButton_batch_run_in_safir_input_folder = QPushButton(self.groupBox_2)
        self.pushButton_batch_run_in_safir_input_folder.setObjectName(u"pushButton_batch_run_in_safir_input_folder")
        self.pushButton_batch_run_in_safir_input_folder.setMinimumSize(QSize(0, 25))
        self.pushButton_batch_run_in_safir_input_folder.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_2.addWidget(self.pushButton_batch_run_in_safir_input_folder, 5, 2, 1, 1)

        self.pushButton_batch_run_submit = QPushButton(self.groupBox_2)
        self.pushButton_batch_run_submit.setObjectName(u"pushButton_batch_run_submit")
        self.pushButton_batch_run_submit.setMinimumSize(QSize(60, 25))
        self.pushButton_batch_run_submit.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_2.addWidget(self.pushButton_batch_run_submit, 6, 2, 1, 1)

        self.label_batch_run_in_processes = QLabel(self.groupBox_2)
        self.label_batch_run_in_processes.setObjectName(u"label_batch_run_in_processes")
        self.label_batch_run_in_processes.setMinimumSize(QSize(0, 25))
        self.label_batch_run_in_processes.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_2.addWidget(self.label_batch_run_in_processes, 3, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.gridGroupBox = QGroupBox(self.centralwidget)
        self.gridGroupBox.setObjectName(u"gridGroupBox")
        self.gridLayout_3 = QGridLayout(self.gridGroupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(10)
        self.gridLayout_3.setVerticalSpacing(5)
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        self.pushButton_batchbc_root_dir = QPushButton(self.gridGroupBox)
        self.pushButton_batchbc_root_dir.setObjectName(u"pushButton_batchbc_root_dir")
        self.pushButton_batchbc_root_dir.setMinimumSize(QSize(60, 25))
        self.pushButton_batchbc_root_dir.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_3.addWidget(self.pushButton_batchbc_root_dir, 2, 2, 1, 1)

        self.checkBox_batchbc_reduction_factor = QCheckBox(self.gridGroupBox)
        self.checkBox_batchbc_reduction_factor.setObjectName(u"checkBox_batchbc_reduction_factor")
        self.checkBox_batchbc_reduction_factor.setMinimumSize(QSize(0, 25))
        self.checkBox_batchbc_reduction_factor.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_3.addWidget(self.checkBox_batchbc_reduction_factor, 6, 0, 1, 3)

        self.lineEdit_batchbc_root_dir = QLineEdit(self.gridGroupBox)
        self.lineEdit_batchbc_root_dir.setObjectName(u"lineEdit_batchbc_root_dir")
        self.lineEdit_batchbc_root_dir.setMinimumSize(QSize(0, 25))
        self.lineEdit_batchbc_root_dir.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_3.addWidget(self.lineEdit_batchbc_root_dir, 2, 1, 1, 1)

        self.label_batchbc_bc_file = QLabel(self.gridGroupBox)
        self.label_batchbc_bc_file.setObjectName(u"label_batchbc_bc_file")
        self.label_batchbc_bc_file.setMinimumSize(QSize(0, 25))
        self.label_batchbc_bc_file.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_3.addWidget(self.label_batchbc_bc_file, 3, 0, 1, 1)

        self.label_batchbc_root_dir = QLabel(self.gridGroupBox)
        self.label_batchbc_root_dir.setObjectName(u"label_batchbc_root_dir")
        self.label_batchbc_root_dir.setMinimumSize(QSize(0, 25))
        self.label_batchbc_root_dir.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_3.addWidget(self.label_batchbc_root_dir, 2, 0, 1, 1)

        self.label_3 = QLabel(self.gridGroupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setWordWrap(True)

        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 3)

        self.label_2 = QLabel(self.gridGroupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 25))
        self.label_2.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 3)

        self.lineEdit_batchbc_bc_file = QLineEdit(self.gridGroupBox)
        self.lineEdit_batchbc_bc_file.setObjectName(u"lineEdit_batchbc_bc_file")
        self.lineEdit_batchbc_bc_file.setMinimumSize(QSize(0, 25))
        self.lineEdit_batchbc_bc_file.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_3.addWidget(self.lineEdit_batchbc_bc_file, 3, 1, 1, 1)

        self.label_6 = QLabel(self.gridGroupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setWordWrap(True)

        self.gridLayout_3.addWidget(self.label_6, 7, 0, 1, 3)

        self.pushButton_batchbc_bc_file = QPushButton(self.gridGroupBox)
        self.pushButton_batchbc_bc_file.setObjectName(u"pushButton_batchbc_bc_file")
        self.pushButton_batchbc_bc_file.setMinimumSize(QSize(60, 25))
        self.pushButton_batchbc_bc_file.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_3.addWidget(self.pushButton_batchbc_bc_file, 3, 2, 1, 1)

        self.pushButton_batchbc_ok = QPushButton(self.gridGroupBox)
        self.pushButton_batchbc_ok.setObjectName(u"pushButton_batchbc_ok")
        self.pushButton_batchbc_ok.setMinimumSize(QSize(60, 25))
        self.pushButton_batchbc_ok.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_3.addWidget(self.pushButton_batchbc_ok, 8, 2, 1, 1)


        self.verticalLayout.addWidget(self.gridGroupBox)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(5)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.lineEdit_in_shell = QLineEdit(self.groupBox)
        self.lineEdit_in_shell.setObjectName(u"lineEdit_in_shell")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit_in_shell.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_shell.setSizePolicy(sizePolicy1)
        self.lineEdit_in_shell.setMinimumSize(QSize(100, 25))
        self.lineEdit_in_shell.setMaximumSize(QSize(16777215, 25))

        self.gridLayout.addWidget(self.lineEdit_in_shell, 2, 1, 1, 1)

        self.label_in_shell = QLabel(self.groupBox)
        self.label_in_shell.setObjectName(u"label_in_shell")

        self.gridLayout.addWidget(self.label_in_shell, 2, 0, 1, 1)

        self.comboBox_in_shell = QComboBox(self.groupBox)
        self.comboBox_in_shell.setObjectName(u"comboBox_in_shell")
        self.comboBox_in_shell.setMinimumSize(QSize(0, 25))
        self.comboBox_in_shell.setMaximumSize(QSize(16777215, 25))

        self.gridLayout.addWidget(self.comboBox_in_shell, 2, 2, 1, 1)

        self.pushButton_fp_out = QPushButton(self.groupBox)
        self.pushButton_fp_out.setObjectName(u"pushButton_fp_out")
        self.pushButton_fp_out.setMinimumSize(QSize(0, 25))
        self.pushButton_fp_out.setMaximumSize(QSize(16777215, 25))

        self.gridLayout.addWidget(self.pushButton_fp_out, 1, 2, 1, 1)

        self.pushButton_ok = QPushButton(self.groupBox)
        self.pushButton_ok.setObjectName(u"pushButton_ok")
        self.pushButton_ok.setMinimumSize(QSize(60, 25))
        self.pushButton_ok.setMaximumSize(QSize(16777215, 25))

        self.gridLayout.addWidget(self.pushButton_ok, 3, 2, 1, 1)

        self.lineEdit_in_fp_out = QLineEdit(self.groupBox)
        self.lineEdit_in_fp_out.setObjectName(u"lineEdit_in_fp_out")
        sizePolicy1.setHeightForWidth(self.lineEdit_in_fp_out.sizePolicy().hasHeightForWidth())
        self.lineEdit_in_fp_out.setSizePolicy(sizePolicy1)
        self.lineEdit_in_fp_out.setMinimumSize(QSize(100, 25))
        self.lineEdit_in_fp_out.setMaximumSize(QSize(16777215, 25))

        self.gridLayout.addWidget(self.lineEdit_in_fp_out, 1, 1, 1, 1)

        self.label_in_fp_out = QLabel(self.groupBox)
        self.label_in_fp_out.setObjectName(u"label_in_fp_out")

        self.gridLayout.addWidget(self.label_in_fp_out, 1, 0, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 25))
        self.label.setMaximumSize(QSize(16777215, 25))

        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)


        self.verticalLayout.addWidget(self.groupBox)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 352, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_batch_run_description.setText(QCoreApplication.translate("MainWindow", u"Run all *.in files within the selected root folder and sub-folders and sub-sub-folders.", None))
        self.label_batch_run_in_timeout_unit.setText(QCoreApplication.translate("MainWindow", u"s", None))
        self.label_batch_run_in_timeout.setText(QCoreApplication.translate("MainWindow", u"Timeout", None))
        self.pushButton_batch_run_in_safir_exe_path.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.label_batch_run_title.setText(QCoreApplication.translate("MainWindow", u"<b>Batch run *.in files<b>", None))
        self.lineEdit_batch_run_in_timeout.setText(QCoreApplication.translate("MainWindow", u"18000", None))
        self.lineEdit_batch_run_in_timeout.setPlaceholderText(QCoreApplication.translate("MainWindow", u"seconds", None))
        self.label_batch_run_in_safir_exe_path.setText(QCoreApplication.translate("MainWindow", u"Safir *.exe path", None))
        self.label_batch_run_in_safir_input_folder.setText(QCoreApplication.translate("MainWindow", u"*.in files root dirctory", None))
        self.lineEdit_batch_run_in_processes.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.lineEdit_batch_run_in_safir_exe_path.setText(QCoreApplication.translate("MainWindow", u"C:/work/fem/SAFIR/safir.exe", None))
        self.pushButton_batch_run_in_safir_input_folder.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.pushButton_batch_run_submit.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.label_batch_run_in_processes.setText(QCoreApplication.translate("MainWindow", u"No. of processes", None))
        self.pushButton_batchbc_root_dir.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.checkBox_batchbc_reduction_factor.setText(QCoreApplication.translate("MainWindow", u"Apply reduction factor", None))
        self.label_batchbc_bc_file.setText(QCoreApplication.translate("MainWindow", u"BC file to be populated", None))
        self.label_batchbc_root_dir.setText(QCoreApplication.translate("MainWindow", u"*.in files root directory", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Copy a selected BC file to all folders containing *.in file. The BC file must be comprised of two columns, time and temperature, respectively.", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Batch add boundary condition (BC) file</span></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"If selected, a file named `bc_reduction.csv` must be present in the selected root directory containing desired reduction factors. A template will be saved in the root directory upon root directory selection.", None))
        self.pushButton_batchbc_bc_file.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.pushButton_batchbc_ok.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.groupBox.setTitle("")
        self.label_in_shell.setText(QCoreApplication.translate("MainWindow", u"Shell index", None))
        self.pushButton_fp_out.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.pushButton_ok.setText(QCoreApplication.translate("MainWindow", u"OK", None))
        self.label_in_fp_out.setText(QCoreApplication.translate("MainWindow", u"*.out file path", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<b>Post process strain<b>", None))
    # retranslateUi

