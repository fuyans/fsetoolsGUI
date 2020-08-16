from os.path import join

from PySide2.QtWidgets import QLabel, QVBoxLayout

import fsetoolsGUI
from fsetoolsGUI.gui.logic.c0400_br187_base_class import BR187SimpleBaseClass
from fsetoolsGUI.gui.logic.c0403_br187_parallel_complex import App as App0403


class App(BR187SimpleBaseClass):
    """0401, for analysis thermal radiation between a rectangular shaped emitter and ...

    Error handling scenarios:
        1.  Input parsing failure due to inappropriate data type, i.e. height = 12.e4 will be not successfully parsed.
        2.  Calculation failure, when to solve separation distance for given unprotected area, reached upper limit of
            the predefined S.
        3.  Calculation failure, when to solve separation distance for given unprotected area, reached lower limit of
            the predefined S.
        4.  Calculation failure, no convergence found.
    """
    app_id = '0401'
    app_name_short = 'BR 187\nparallel'
    app_name_long = 'BR 187 parallel oriented rectangle emitter and receiver'

    def __init__(self, parent=None, post_stats: bool = True):
        super().__init__(parent, post_stats)

        self.ui.p1_description = QLabel(
            'This sheet calculates the thermal radiation intensity at a receiver that is '
            'parallel to a rectangular emitter. Calculation coded in this sheet follows "BR 187 External fire spread" '
            '2nd edition.'
        )
        self.ui.p1_description.setFixedWidth(350)
        self.ui.p1_description.setWordWrap(True)
        self.ui.p1_image = QLabel()
        self.ui.p1_image.setPixmap(join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0401-1.png'))
        self.ui.p1_layout = QVBoxLayout(self.ui.page_1)
        self.ui.p1_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.p1_layout.addWidget(self.ui.p1_description)
        self.ui.p1_layout.addWidget(self.ui.p1_image)

    @staticmethod
    def phi_solver(W: float, H: float, w: float, h: float, Q: float, Q_a: float, S=None, UA=None) -> tuple:
        """A wrapper to `phi_parallel_any_br187` with error handling and customised IO"""
        return App0403.phi_solver(W=W, H=H, w=0, h=0, Q=Q, Q_a=Q_a, S=S, UA=UA)


if __name__ == "__main__":
    import sys
    from PySide2 import QtWidgets

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
