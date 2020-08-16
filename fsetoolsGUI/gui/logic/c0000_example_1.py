from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QLabel, QGridLayout, QVBoxLayout

from fsetoolsGUI.gui.logic.custom_app_template_1 import AppBaseClass


class App(AppBaseClass):
    app_id = '0000'
    app_name_short = 'example name short'
    app_name_long = 'example name long'

    def __init__(self, parent=None):
        # instantiate ui
        super().__init__(
            parent=parent,
        )

        self.ui.p1_grid = QVBoxLayout(self.ui.page_1)
        self.ui.p1_intro = QLabel(
            'This is a brief description. \n'
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et '
            'dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip '
            'ex ea commodo consequat.'
        )
        self.ui.p1_intro.setFixedWidth(350)
        self.ui.p1_intro.setWordWrap(True)
        self.ui.p1_grid.addWidget(self.ui.p1_intro)
        self.ui.p1_image = QLabel('placeholder image')
        self.ui.p1_image.setFixedSize(350, 200)
        self.ui.p1_image.setAlignment(QtCore.Qt.AlignCenter)
        # self.ui.p1_image.setPixmap(join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0401-1.png'))
        self.ui.p1_grid.addWidget(self.ui.p1_image)

        self.ui.p2_grid = QGridLayout(self.ui.page_2)
        self.ui.p2_grid.addWidget(QLabel('<b>Input parameter list</b>'), 0, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_grid, 1, 'p2_entry_1', 'test description 1', 'unit 1')
        self.add_lineedit_set_to_grid(self.ui.p2_grid, 2, 'p2_entry_2', 'test description 2', 'unit 2')
        self.add_lineedit_set_to_grid(self.ui.p2_grid, 3, 'p2_entry_3', 'test description 3', 'unit 3')
        self.add_lineedit_set_to_grid(self.ui.p2_grid, 4, 'p2_entry_4', 'test description 4', 'unit 4')
        self.add_lineedit_set_to_grid(self.ui.p2_grid, 5, 'p2_entry_5', 'test description 5', 'unit 5')
        self.add_lineedit_set_to_grid(self.ui.p2_grid, 6, 'p2_entry_6', 'test description 6', 'unit 6')
        self.add_lineedit_set_to_grid(self.ui.p2_grid, 7, 'p2_entry_7', 'test description 7', 'unit 7')
        self.add_lineedit_set_to_grid(self.ui.p2_grid, 8, 'p2_entry_8', 'test description 8', 'unit 8')
        self.ui.p2_grid.addWidget(QLabel('<b>Output parameter list</b>'), 9, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_grid, 10, 'p2_entry_10', 'test description 10', 'unit 10')
        self.add_lineedit_set_to_grid(self.ui.p2_grid, 11, 'p2_entry_11', 'test description 11', 'unit 11')

    def ok(self):
        pass

    def example(self):
        pass


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    qapp.exec_()
