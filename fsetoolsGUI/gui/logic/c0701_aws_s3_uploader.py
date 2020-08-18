from os import path

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QGridLayout

from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.custom_table import TableWindow

try:
    import boto3
except ModuleNotFoundError:
    boto3 = None


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
    """
    Required Environmental Variables: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
    """
    app_id = '0701'
    app_name_short = 'AWS\nS3\nUploader'
    app_name_long = 'AWS S3 Uploader'

    def __init__(self, parent=None, post_stats: bool = True):

        self.__s3_client = boto3.client('s3')
        self.signals = Signals()
        self.__fp_list = None
        self.__url_list = None
        self.__Table = None

        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)

        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5)
        self.ui.p2_layout.setHorizontalSpacing(5)
        self.add_widget_to_grid(self.ui.p2_layout, 0, 'p2_in_bucket', 'Bucket name', None)
        self.add_widget_to_grid(self.ui.p2_layout, 1, 'p2_in_prefix', 'Prefix', None, min_width=180)
        self.ui.p3_submit.setText('Select files and upload')

        self.ui.p3_about.setHidden(True)
        self.ui.p3_example.setHidden(True)

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
            self.__upload_to_s3(self.__fp_list, dir_name=self.ui.p2_in_prefix.text(), bucket=self.ui.p2_in_bucket.text())
        except Exception as e:
            self.statusBar().showMessage(f'Upload failed {e}')

        self.show_results_in_table()

    def ok(self):
        self.select_image_and_upload()

    def select_file_paths(self) -> list:
        """
        select input file and copy its path to ui object
        """

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
            window_title='Uploaded files and corresponding URL',
        )

        self.__Table.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        self.__Table.TableView.resizeColumnsToContents()
        self.__Table.show()

        return True

    def __upload_to_s3(self, file_paths: list, dir_name: str, bucket: str = 'ofr'):
        self.__url_list = list()
        for i, fp in enumerate(file_paths):
            self.statusBar().showMessage(f'Uploading image {i + 1}/{len(file_paths)}...')
            self.repaint()

            try:
                self.__s3_client.upload_file(fp, bucket, f'{dir_name}{path.basename(fp)}')
                self.__url_list.append(f'https://{bucket}.s3.eu-west-2.amazonaws.com/{dir_name}{path.basename(fp)}')
            except Exception as e:
                self.__url_list.append(f'{e}')

    def example(self):
        pass  # placeholder attribute, not used.


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
