from os import path

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QHBoxLayout, QSplitter

import fsetoolsGUI

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

qt_css = open(path.join(fsetoolsGUI.__root_dir__, 'gui', '../styles/fancy.css'), "r").read()


class App(QtWidgets.QDialog):
    def __init__(self, parent=None, title: str = None):
        super().__init__(parent=parent)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)

        self.resize(380, 380)

        # ======================
        # instantiate UI objects
        # ======================
        self.setStyleSheet(qt_css)

        if title:
            self.setWindowTitle(title)

        self.p0_layout = QSplitter()

        pw1 = gl.GLViewWidget()
        pw1.setCameraPosition(distance=40)
        g = gl.GLGridItem(size=QtGui.QVector3D(100,100,1))
        # g.scale(10, 10, 1)
        pw1.addItem(g)

        verts = np.array([
            [0, 0, 0],
            [10, 0, 0],
            [10, 10, 0],
            [0, 10, 1],
        ])
        faces = np.array([
            [0, 1, 2],
            [0, 1, 3],
            [0, 2, 3],
            [1, 2, 3]
        ])
        colors = np.array([0.1, 0.2, 0.3, 0.9])

        ## Mesh item will automatically compute face normals.
        m1 = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False)
        # m1.translate(5, 5, 0)
        m1.setGLOptions('additive')
        pw1.addItem(m1)

        self.p0_layout.addWidget(pw1)

        layout = QHBoxLayout()
        layout.addWidget(self.p0_layout)
        self.setLayout(layout)


def _test_1():
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(title='Example')
    app.show()

    qapp.exec_()


if __name__ == '__main__':
    _test_1()
