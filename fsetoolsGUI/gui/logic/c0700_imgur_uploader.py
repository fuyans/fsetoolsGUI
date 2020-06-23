from PySide2 import QtWidgets, QtCore
from imgurpython import ImgurClient
from imgurpython.client import AuthWrapper

from fsetoolsGUI.gui.layout.i0700_imgur_uploader import Ui_MainWindow
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow
from fsetoolsGUI.gui.logic.custom_table import TableWindow
from os import path


class App0700(QMainWindow):

    def __init__(self, parent=None, mode=None):
        module_id = '0700'

        self.__client_id = '2a5830013bb0f84'
        self.__client_secret = '02e494ed1134c8bfc89502fc22b243c14b92a0af'
        self.__access_token = '570a314ab63c83adc5f95fa4273b55f6e5681f85'
        self.__refresh_token = '9ad4c3f8c3c841f270fbcf40b60a91a9402a6bbf'

        self.__imgur_client = ImgurClient(self.__client_id, self.__client_secret)
        self.__imgur_auth = None

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
        self.ui.pushButton_upload.clicked.connect(self.upload_image)

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

    @input_parameters.setter
    def input_parameters(self, v):

        def num2str(num):
            if isinstance(num, int):
                return f'{num:g}'
            elif isinstance(num, float):
                return f'{num:.3f}'.rstrip('0').rstrip('.')
            elif isinstance(num, str):
                return v
            elif num is None:
                return ''
            else:
                return str(v)

        pass

    @property
    def output_parameters(self):
        return self.__output_fire_curve

    @output_parameters.setter
    def output_parameters(self, v):
        img_url = v['img_url']
        self.ui.lineEdit_img_url.setText(img_url)

    def select_image_and_upload(self):
        fp = self.select_file_path()

        if len(fp) == 0:
            return 0

        self.ui.lineEdit_fp.setText(fp)

        self.upload_image()

    def upload_image(self):
        fp = self.ui.lineEdit_fp.text()

        try:
            self.statusBar().showMessage('Uploading image...')
            self.repaint()
            img_url = self.__upload_fp_to_imgur(fp=fp)
        except Exception as e:
            self.statusBar().showMessage(f'Upload failed {e}')
            return e

        try:
            self.ui.lineEdit_img_url.setText(img_url)
            self.ui.lineEdit_img_url.selectAll()
            self.copy_str(img_url)
            self.statusBar().showMessage('url copied to clipboard')
        except Exception as e:
            self.statusBar().showMessage(f'Copy url failed {e}')
            return e

    def ok_silent(self):

        # --------------------
        # Parse inputs from UI
        # --------------------

        # -------------------------------------------------------
        # Make strain evaluation data for selected `unique_shell`
        # -------------------------------------------------------

        # ------------------
        # Cast outputs to UI
        # ------------------

        return 0

    def ok(self):

        fp = self.select_file_path()

        try:
            self.statusBar().showMessage('Uploading image...')
            self.repaint()
            img_url = self.__upload_fp_to_imgur(fp=fp)
        except Exception as e:
            self.statusBar().showMessage(f'Upload failed {e}')
            return e

        self.output_parameters = dict(img_url=img_url)

        self.copy_str(img_url)
        self.ui.lineEdit_img_url.selectAll()

        self.statusBar().showMessage('url copied to clipboard')

        return 0


    def select_file_path(self):
        """select input file and copy its path to ui object"""

        # dialog to select file
        path_to_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select File",
            "~/",
            "Image (*.png *.jpg)")

        # paste the select file path to the ui object
        return path_to_file

    def show_results_in_table(self):

        # output_parameters = self.output_parameters

        list_x = [list(i['x']) for i in self.__strain_lines]
        list_y = [i['y'] for i in self.__strain_lines]
        list_label = [i['label'] for i in self.__strain_lines]

        # make a full x values
        x_all = []
        for i in self.__strain_lines:
            x_all += list(i['x'])
        x_all = list(set(x_all))
        x_all.sort()

        # fill y values to match len(x_all)
        for i in range(len(list_x)):
            x = list_x[i]
            y = list_y[i]
            y_ = [0] * len(x_all)
            for j, v in enumerate(x_all):
                try:
                    y_[j] = y[x.index(v)]
                except ValueError:
                    pass
            list_y[i] = y_
            print(len(y_))

        list_content = [x_all]
        [list_content.append(i) for i in list_y]
        list_content = [[float(j) for j in i] for i in zip(*list_content)]

        # print results (for console enabled version only)

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
            header_col=['time'] + list_label,
            window_title='Table',
        )

        self.__Table.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        self.__Table.TableView.resizeColumnsToContents()
        self.__Table.show()

        return True

    def __upload_fp_to_imgur(self, fp: str):

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

        uploaded_img_url = self.__imgur_client.upload_from_path(fp)

        return uploaded_img_url['link']


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App0700(mode=-1)
    app.show()
    qapp.exec_()
