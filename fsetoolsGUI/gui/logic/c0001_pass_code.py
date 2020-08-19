from os import getlogin

import requests
from PySide2 import QtWidgets, QtGui, QtCore

import fsetoolsGUI
from fsetoolsGUI.gui.images_base64 import OFR_LOGO_1_PNG


class App(QtWidgets.QDialog):
    _pass_code = None

    def __init__(self, parent=None):
        super().__init__(parent)

        # ui elements instantiation
        self.label = QtWidgets.QLabel(
            f'FSETOOLS {fsetoolsGUI.__version__} released on {fsetoolsGUI.__date_released__.strftime("%Y %B %d")} is expired.\n\n'
            f'Either to download the latest version (link provided in the box below) or enter a pass code.\n\n'
            f'Your login name is {getlogin()}\n'
        )
        self.label.setWordWrap(True)

        self.edit = QtWidgets.QLineEdit()

        try:
            target = ''.join([chr(ord(v) + i % 10) for i, v in enumerate(fsetoolsGUI.__remote_version_url__)])

            version_dict = requests.get(target).json()
            latest_version_url = version_dict['latest_executable_download_url']
            self.edit.setText(latest_version_url)
        except Exception as e:
            if isinstance(e, requests.exceptions.ConnectionError):
                self.edit.setText(f'Connection error, failed to reach {fsetoolsGUI.__remote_version_url__}.')
            else:
                self.edit.setText(str(e))

        self.button = QtWidgets.QPushButton('OK')
        self.button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.label, 0, 0, 1, 2)
        layout.addWidget(self.edit, 1, 0, 1, 1)
        layout.addWidget(self.button, 1, 1, 1, 1)
        self.setLayout(layout)

        # window properties
        ba = QtCore.QByteArray.fromBase64(OFR_LOGO_1_PNG)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.setWindowIcon(pix_map)
        self.setWindowTitle('Application Expired')

        # signals and slots
        self.button.clicked.connect(self.submit)

    def submit(self):
        self._pass_code = self.edit.text()
        QtWidgets.QApplication.exit()

    @property
    def pass_code(self) -> str:
        if self._pass_code is None:
            return '-1'
        else:
            return self._pass_code


if __name__ == '__main__':
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    qapp.exec_()
