from os import path

import boto3
from PySide2 import QtWidgets, QtCore

from fsetoolsGUI.gui.layout.i0701_s3_uploader import Ui_MainWindow
from fsetoolsGUI.gui.logic.custom_app_template import AppBaseClass
from fsetoolsGUI.gui.logic.custom_table import TableWindow


class Signals(QtCore.QObject):
    __upload_progress_bar_signal = QtCore.Signal(int)
    __upload_complete = QtCore.Signal(bool)

    @property
    def upload_progress_bar_signal(self):
        return self.__upload_progress_bar_signal

    @property
    def upload_complete(self):
        return self.__upload_complete


class App(AppBaseClass):
    app_id = '0701'
    app_name_short = 's3\nUploader'
    app_name_long = 's3 Uploader'

    def __init__(self, parent=None, mode=None):

        self.__s3_client = boto3.client('s3')


        self.signals = Signals()

        self.__fp_list = None
        self.__url_list = None

        self.__Table = None

        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()

        # =======================
        # lineEdit default values
        # =======================

        # =================
        # Slots and Signals
        # =================
        self.ui.pushButton_select_img.clicked.connect(self.select_image_and_upload)

    def select_image_and_upload(self):
        self.__fp_list, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            "Select File",
            "~/",
            "All ()")

        if len(self.__fp_list) == 0:
            self.statusBar().showMessage('Nothing to upload')
            return

        try:
            self.__upload_to_s3(self.__fp_list, dir=self.ui.lineEdit_in_key.text())
        except Exception as e:
            self.statusBar().showMessage(f'Upload failed {e}')

        self.show_results_in_table()

    def ok(self):
        self.select_image_and_upload()

    def select_file_paths(self) -> list:
        """select input file and copy its path to ui object"""

        # dialog to select file
        path_to_file, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            "Select File",
            "~/",
            "Image (*.png *.jpg)")

        # paste the select file path to the ui object
        return path_to_file

    def show_results_in_table(self):

        # output_parameters = self.output_parameters

        list_content = [[i, path.basename(i), str(j)] for i, j in list(zip(self.__fp_list, self.__url_list))]

        try:
            win_geo = self.__Table.geometry()
            self.__Table.destroy(destroyWindow=True, destroySubWindows=True)
            del self.__Table
        except AttributeError as e:
            win_geo = None

        self.__Table = TableWindow(
            parent=self,
            window_geometry=win_geo,
            data_list=list_content,
            header_col=['file path', 'file name', 'url'],
            window_title='Table',
        )

        self.__Table.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        self.__Table.TableView.resizeColumnsToContents()
        self.__Table.show()

        return True

    def __upload_to_s3(self, file_paths: list, dir: str, bucket: str = 'ofr'):

        self.__url_list = list()
        for i, fp in enumerate(file_paths):
            self.statusBar().showMessage(f'Uploading image {i + 1}/{len(file_paths)}...')
            self.repaint()

            try:
                self.__s3_client.upload_file(fp, bucket, f'{dir}{path.basename(fp)}')
                self.__url_list.append(f'https://{bucket}.s3.eu-west-2.amazonaws.com/{dir}{path.basename(fp)}')
            except Exception as e:
                self.__url_list.append(f'{e}')


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(mode=-1)
    app.show()
    qapp.exec_()
