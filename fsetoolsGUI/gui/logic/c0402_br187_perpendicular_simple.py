from fsetoolsGUI.gui.layout.i0401_br187_simple import Ui_MainWindow as Ui_0403
from fsetoolsGUI.gui.logic.c0404_br187_perpendicular_complex import App as App0404
from fsetoolsGUI.gui.logic.c0401_br187_base_class import BR187BaseClass


class App(BR187BaseClass):
    """0402, thermal radiation calculation between a rectangular shaped emitter and a perpendicular oriented receiver.

    Error handling scenarios:
        1.  Input parsing failure due to inappropriate data type, i.e. height = 12.e4 will be not successfully parsed.
        2.  Calculation failure, when to solve separation distance for given unprotected area, reached upper limit of
            the predefined S.
        3.  Calculation failure, when to solve separation distance for given unprotected area, reached lower limit of
            the predefined S.
        4.  Calculation failure, no convergence found.
    """
    app_id = '0402'
    app_name_short = 'BR 187\nperp.'
    app_name_long = 'BR 187 perpendicular oriented rectangle emitter and receiver'

    def __init__(self, parent=None):
        super().__init__(ui=Ui_0403, parent=parent)
        self.ui.label_description.setText(
            'This sheet calculates the thermal radiation intensity at a receiver that is perpendicular to '
            'an rectangular emitter. Calculation coded in this sheet follows "BR 187 External fire spread" 2nd edition.'
        )
        self.init()

    @staticmethod
    def phi_solver(W: float, H: float, w: float, h: float, Q: float, Q_a: float, S=None, UA=None) -> tuple:
        """A wrapper to `phi_parallel_any_br187` with error handling and customised IO"""

        return App0404.phi_solver(W=W, H=H, w=0, h=0, Q=Q, Q_a=Q_a, S=S, UA=UA)


if __name__ == "__main__":
    import sys
    from PySide2 import QtWidgets

    qapp = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    qapp.exec_()
