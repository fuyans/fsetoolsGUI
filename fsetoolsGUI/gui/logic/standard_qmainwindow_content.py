from PySide2 import QtWidgets

from fsetoolsGUI.gui.layout.standard_qmainwindow_content import Ui_MainWindow
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow


class App(QMainWindow):

    # quality assurance log data with following format [[], []]
    qa_data: list = [
        [
            '00000000',  # date
            'Ian Fu',  # latest author
            'XXX XXX'  # QA & Technical Review
        ]
    ]

    def __init__(self, parent=None):

        # instantiate ui
        super().__init__(
            parent=parent,
            title='Standard Layout MainWindow Content',
            shortcut_Return=self.calculate,
            quality_assurance_content=self.qa_data,
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()

        self.ui.pushButton_control_ok.clicked.connect(self.show_quality_assurance_info)

    def example(self):
        pass

    def calculate(self):
        pass


if __name__ == "__main__":
    import sys
    qapp = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    qapp.exec_()
