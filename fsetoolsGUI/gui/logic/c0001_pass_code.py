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
            f'Version {fsetoolsGUI.__version__} released on {fsetoolsGUI.__date_released__.strftime("%Y %B %d")} is expired.\n'
            f'Download the latest version (follow link below) or enter a pass code in the input box below.'
        )

        self.edit = QtWidgets.QLineEdit()

        try:
            target = ''.join([chr(ord(v) + i % 10) for i, v in enumerate(fsetoolsGUI.__remote_version_url__)])
            version_dict = requests.get(target).json()
            self.edit.setText(version_dict['executable_download_url'])
        except Exception as e:
            if isinstance(e, requests.exceptions.ConnectionError):
                self.edit.setText(f'Connection error, failed to reach {fsetoolsGUI.__remote_version_url__}.')
            else:
                self.edit.setText(str(e))

        self.button = QtWidgets.QPushButton('OK')

        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # window properties
        ba = QtCore.QByteArray.fromBase64(OFR_LOGO_1_PNG)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.setWindowIcon(pix_map)
        self.setWindowTitle('Warning')

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
