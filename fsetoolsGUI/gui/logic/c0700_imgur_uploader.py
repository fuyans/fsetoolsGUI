from PySide2 import QtWidgets, QtCore
from imgurpython import ImgurClient
from imgurpython.client import AuthWrapper

from fsetoolsGUI.gui.layout.i0700_imgur_uploader import Ui_MainWindow
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow
from fsetoolsGUI.gui.logic.custom_table import TableWindow
from os import path
import threading


class Signals(QtCore.QObject):
    __upload_progress_bar_signal = QtCore.Signal(int)
    __upload_complete = QtCore.Signal(bool)

    @property
    def upload_progress_bar_signal(self):
        return self.__upload_progress_bar_signal

    @property
    def upload_complete(self):
        return self.__upload_complete


class App0700(QMainWindow):

    def __init__(self, parent=None, mode=None):
        module_id = '0700'

        self.__client_id = '2a5830013bb0f84'
        self.__client_secret = '02e494ed1134c8bfc89502fc22b243c14b92a0af'
        self.__access_token = 'e777696ed606854567533da71300ac153df2f5e1'
        self.__refresh_token = 'a638e7e8b5c1aad9caa5b50dad505b8e64cc5c95'

        self.__imgur_client = ImgurClient(self.__client_id, self.__client_secret)
        self.__imgur_auth = None
        self.__image_files = None
        self.__image_urls = None

        self.signals = Signals()

        self.__Table = None

        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(
            module_id=module_id,
            parent=parent,
            freeze_window_size=False,
            mode=mode
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init(self)

        # =======================
        # lineEdit default values
        # =======================

        # =================
        # Slots and Signals
        # =================
        self.ui.pushButton_select_img.clicked.connect(self.select_image_and_upload)
        self.signals.upload_progress_bar_signal.connect(self.ui.progressBar.setValue)

    @property
    def input_parameters(self):

        def str2int(v):
            try:
                return int(v)
            except:
                return None

        # ====================
        # parse values from ui
        # ====================

        # ======================================================
        # check if necessary inputs are provided for calculation
        # ======================================================

        # ==============================
        # validate individual parameters
        # ==============================

        # ================
        # units conversion
        # ================

        return None

    def select_image_and_upload(self):
        self.__image_files = self.select_file_paths()

        try:
            self.__upload_fp_to_imgur(self.__image_files)
        except Exception as e:
            self.statusBar().showMessage(f'Upload failed {e}')

        self.show_results_in_table()

    def ok(self):
        pass

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

        list_content = [[i, path.basename(i), str(j)] for i, j in list(zip(self.__image_files, self.__image_urls))]

        for i in list_content:
            print(i)

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


    def __upload_fp_to_imgur(self, file_paths: list):

        # file_paths = self.__image_files

        if self.__imgur_auth is None:
            auth_wrapper = AuthWrapper(
                access_token=self.__access_token,
                refresh_token=self.__refresh_token,
                client_id=self.__client_id,
                client_secret=self.__client_secret,
            )
            auth_wrapper.refresh()
            self.__imgur_auth = auth_wrapper



        self.__imgur_client.set_user_auth(
            access_token=self.__imgur_auth.current_access_token,
            refresh_token=self.__imgur_auth.refresh_token
        )

        self.__image_urls = list()
        for i, fp in enumerate(file_paths):
            self.statusBar().showMessage(f'Uploading image {i+1}/{len(file_paths)}...')
            self.repaint()
            try:
                uploaded_img_url = self.__imgur_client.upload_from_path(fp)
                print(uploaded_img_url)
                self.__image_urls.append(uploaded_img_url['link'])
            except Exception as e:
                self.__image_urls.append(f'{e}')


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App0700(mode=-1)
    app.show()
    qapp.exec_()
