from PySide2 import QtWidgets, QtCore

from fsetoolsGUI.gui.layout.standard_qmainwindow_module import Ui_MainWindow
from fsetoolsGUI.gui.logic.OFRCustom import QMainWindow
from fsetoolsGUI.gui.logic.dialog_0002_tableview import TableWindow as TableWindow_QMainWindow


class App(QMainWindow):

    qa_data: list = [
        [
            '00000000',  # date
            'Ian Fu',  # latest author
            'XXX XXX'  # QA & Technical Review
        ]
    ]

    dialog_list = []

    def __init__(self, parent=None):

        # instantiate ui
        super().__init__(
            parent=parent,
            title='Standard Layout QMainWindow Module',
            shortcut_Return=self.calculate,
            quality_assurance_content=self.qa_data,
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()

        self.ui.pushButton_control_qa.clicked.connect(self.show_quality_assurance_info)

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