import os.path as path
from PySide2 import QtCore
import fsetoolsGUI
from fsetoolsGUI.gui.logic.dialog_0101_adb_datasheet_1 import DialogPageDisplay


class Dialog0102(DialogPageDisplay):
    def __init__(self):
        super().__init__(
            module_id='0102',
            fp_image=path.join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0102-0.png')
        )
        self.resize(1000, 600)


if __name__ == '__main__':
    from PySide2 import QtWidgets
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = Dialog0102()
    app.show()
    qapp.exec_()
