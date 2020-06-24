from PySide2 import QtWidgets
from fsetoolsGUI.gui.layout.std_qmainwindow_content import Ui_MainWindow

from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow


class App(QMainWindow):

    def __init__(self, parent=None):

        # instantiate ui
        super().__init__(
            parent=parent,
            module_id='0001',
            mode=-1
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init(self)


if __name__ == "__main__":
    import sys
    qapp = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    qapp.exec_()
