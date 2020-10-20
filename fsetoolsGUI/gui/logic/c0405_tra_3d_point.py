from os.path import join

import numpy as np
from PySide2 import QtWidgets, QtGui, QtCore
from fsetools.lib.fse_thermal_radiation_3d import single_receiver, heat_flux_to_temperature

import fsetoolsGUI
from fsetoolsGUI.gui.images_base64 import dialog_0404_page as image_figure
from fsetoolsGUI.gui.layout.i0405_tra_3d_point import Ui_MainWindow
from fsetoolsGUI.gui.logic.c0000_app_template_old import AppBaseClass


class App(AppBaseClass):
    maximum_acceptable_thermal_radiation_heat_flux = 12.6
    fp_doc = join(fsetoolsGUI.__root_dir__, 'gui', 'docs', '0405.md')  # doc file path
    app_id = '0405'
    app_name_short = 'TRA\n3D single point'
    app_name_long = 'TRA 3D polygon emitter and a single point'

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()

        # for i in filter_objects_by_name(self.ui.groupBox_out, object_types=[QtWidgets.QLineEdit]):
        #     try:
        #         i.setReadOnly(True)
        #     except AttributeError:
        #         i.setEnabled(False)

        # set up radiation figure
        ba = QtCore.QByteArray.fromBase64(image_figure)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.ui.label.setPixmap(pix_map)

        # set default values
        self.ui.lineEdit_in_emitter_points.setText('1000')
        self.ui.lineEdit_in_receiver_initial_temperature.setText('293.15')

        # set signals
        self.ui.pushButton_test.clicked.connect(self.test)
        self.ui.pushButton_calculate.clicked.connect(self.calculate)

    def test(self):

        self.ui.plainTextEdit_in_emiter_xyz.setPlainText('0,0,5\n0,5,5\n5,5,5\n5,0,5')
        self.ui.lineEdit_in_emitter_normal.setText('0,0,-1')
        self.ui.lineEdit_in_receiver_location.setText('2.5,2.5,0')
        self.ui.lineEdit_in_receiver_normal.setText('0,0,1')
        self.ui.lineEdit_in_Q.setText('100')

        self.calculate()

        self.repaint()

    def calculate(self):

        # clear ui output fields
        self.ui.lineEdit_out_Phi.setText('')
        self.ui.lineEdit_out_q.setText('')
        self.ui.lineEdit_out_T.setText('')

        # parse inputs from ui
        emitter_points = int(self.ui.lineEdit_in_emitter_points.text())
        emitter_vertices = list()
        for i in [i.split(',') for i in
                  str.strip(self.ui.plainTextEdit_in_emiter_xyz.toPlainText()).replace(' ', '').split('\n')]:
            if len(i) == 0:
                continue
            i_ = list()
            for j in i:
                i_.append(float(j))
            emitter_vertices.append(i_)
        emitter_normal = [float(i) for i in self.ui.lineEdit_in_emitter_normal.text().split(',')]
        receiver_xyz = [float(i) for i in self.ui.lineEdit_in_receiver_location.text().split(',')]
        receiver_normal = [float(i) for i in self.ui.lineEdit_in_receiver_normal.text().split(',')]
        receiver_initial_temperature = float(self.ui.lineEdit_in_receiver_initial_temperature.text())
        Q = float(self.ui.lineEdit_in_Q.text())

        # calculate
        emitter_temperature = heat_flux_to_temperature(Q * 1000)
        receiver_heat_flux, phi = single_receiver(
            ep_vertices=np.array(emitter_vertices),
            ep_norm=np.array(emitter_normal),
            ep_temperature=emitter_temperature,
            n_points=emitter_points,  # number of hot spots
            rp_vertices=np.array(receiver_xyz),
            rp_norm=np.array(receiver_normal),
            rp_temperature=receiver_initial_temperature
        )

        # write results to ui
        self.ui.lineEdit_out_Phi.setText(f'{phi:.4f}')
        self.ui.lineEdit_out_q.setText(f'{receiver_heat_flux / 1000:.2f}')
        self.ui.lineEdit_out_T.setText(f'{emitter_temperature:.2f}')

        # refresh_content_size ui
        self.repaint()


if __name__ == '__main__':
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    qapp.exec_()
