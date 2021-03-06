import os.path as path

import fsetoolsGUI
from fsetoolsGUI.gui.logic.custom_scrollable import AppBaseClassScrollableContent


class App(AppBaseClassScrollableContent):
    app_id = '0102'
    app_name_short = 'BS 9999\ndata sheet\n1'
    app_name_long = 'BS 9999 data sheet no. 1 - means of escape'

    def __init__(self, parent=None, post_stats: bool = True):
        super().__init__(
            fp_image=path.join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0102-0.png'),
            parent=parent,
            post_stats=post_stats
        )
        self.resize(1000, 600)


if __name__ == '__main__':
    from PySide2 import QtWidgets
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
