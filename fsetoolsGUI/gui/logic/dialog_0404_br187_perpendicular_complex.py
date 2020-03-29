from fsetoolsGUI.gui.logic.dialog_0403_br187_parallel_complex import Dialog04


class Dialog0404(Dialog04):
    def __init__(self, parent=None):
        super().__init__(
            module_id='0404',
            parent=parent,
        )


if __name__ == "__main__":
    from PySide2 import QtWidgets
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = Dialog0404()
    app.show()
    qapp.exec_()
