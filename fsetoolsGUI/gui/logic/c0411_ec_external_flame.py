import tempfile
import threading
from os.path import join

from PySide2 import QtWidgets
from PySide2.QtWidgets import QVBoxLayout, QGridLayout, QLabel, QCheckBox, QSpacerItem, QSizePolicy
from fsetools.lib.fse_bs_en_1991_1_2_external_flame import ExternalFlame
from fsetools.lib.fse_bs_en_1991_1_2_external_flame_forced_draught import ExternalFlameForcedDraught

from fsetoolsGUI import __root_dir__, logger
from fsetoolsGUI.gui.logic.c0000_app_template_1 import AppBaseClass


class App(AppBaseClass):
    app_id = '0411'
    app_name_short = 'EC\nExternal\nflame'
    app_name_long = 'BS EN 1991-1-2:2002 External flame'

    def __init__(self, parent=None, post_stats: bool = True):

        # instantiation
        super().__init__(parent, post_stats)

        self.ui.p1_layout = QVBoxLayout(self.ui.page_1)
        self.ui.p1_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.p1_description = QLabel(
            'This app calculates: '
            '(a) the maximum temperatures of a compartment fire; '
            '(b) the size and temperatures of the flame from openings; and '
            '(c) the thermal radiation and convection parameters.\n\n'
            'Calculation methodology follows Annex B in BS EN 1991-1-2:2002 '
            '"Eurocode 1: Actions on structures – Part 1-2: General actions – Actions on structures exposed to fire"'
        )
        self.ui.p1_description.setFixedWidth(440)
        self.ui.p1_description.setWordWrap(True)
        self.ui.p1_layout.addWidget(self.ui.p1_description)
        self.ui.p1_figure = QLabel()
        self.ui.p1_figure.setPixmap(join(__root_dir__, 'gui', 'images', f'{self.app_id}-1.png'))
        self.ui.p1_layout.addWidget(self.ui.p1_figure)

        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), 0, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 1, 'p2_in_q_fd', 'q<sub>fd</sub>, design fuel load',
                                      'MJ/m<sup>2</sup>', min_width=60)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 2, 'p2_in_Q', 'Override HRR', 'MW', descrip_cls='QCheckBox')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 3, 'p2_in_W_1', 'W<sub>1</sub>, enclosure dim. 1', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 4, 'p2_in_W_2', 'W<sub>2</sub>, enclosure dim. 2', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 5, 'p2_in_A_f', 'A<sub>f</sub>, floor area', 'm<sup>2</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 6, 'p2_in_A_t', 'A<sub>t</sub>, total surface area',
                                      'm<sup>2</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 7, 'p2_in_h_eq', 'h<sub>eq</sub>, weighted win. height', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 8, 'p2_in_w_t', 'w<sub>t</sub>, total win. width', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 9, 'p2_in_A_v', 'A<sub>v</sub>, win. area', 'm<sup>2</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 10, 'p2_in_T_0', 'T<sub>0</sub>, Ambient temp.', 'K')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 11, 'p2_in_L_x', 'L<sub>x</sub>, length along flame axis', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 12, 'p2_in_tau_F', 'tau<sub>F</sub>, free burning duration',
                                      's')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 13, 'p2_in_u', 'u, wind speed', 'm/s')

        self.ui.p2_layout.addItem(QSpacerItem(10, 1, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 3, 1, 1)

        self.ui.p2_layout.addWidget(QLabel('<b>Options</b>'), 0, 4, 1, 4)
        self.ui.p2_in_is_forced_draught = QCheckBox('Is forced draught?')
        self.ui.p2_in_is_wall_above_opening = QCheckBox('Is wall above opening?')
        self.ui.p2_in_is_windows_on_more_than_one_wall = QCheckBox('Win. on more than 1 wall?')
        self.ui.p2_in_is_central_core = QCheckBox('Is central core present?')
        self.ui.p2_in_make_pdf_web = QCheckBox('Make PDF report?')
        self.ui.p2_layout.addWidget(self.ui.p2_in_is_forced_draught, 1, 4, 1, 4)
        self.ui.p2_layout.addWidget(self.ui.p2_in_is_wall_above_opening, 2, 4, 1, 4)
        self.ui.p2_layout.addWidget(self.ui.p2_in_is_windows_on_more_than_one_wall, 3, 4, 1, 4)
        self.ui.p2_layout.addWidget(self.ui.p2_in_is_central_core, 4, 4, 1, 4)
        self.ui.p2_layout.addWidget(self.ui.p2_in_make_pdf_web, 5, 4, 1, 4)

        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), 6, 4, 1, 4)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 7, 'p2_out_Q', 'HRR', 'MW', col=4, min_width=60)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 8, 'p2_out_T_f', 'T<sub>f</sub>', 'K', col=4)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 9, 'p2_out_L_L', 'L<sub>L</sub>', 'm', col=4)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 10, 'p2_out_L_H', 'L<sub>H</sub>', 'm', col=4)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 11, 'p2_out_L_f', 'L<sub>f</sub>', 'm', col=4)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 12, 'p2_out_T_w', 'T<sub>w</sub>', 'K', col=4)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 13, 'p2_out_T_z', 'T<sub>z</sub>', 'K', col=4)
        # is_windows_on_more_than_one_wall = self.ui.p2_in_is_windows_on_more_than_one_wall.isChecked()
        # is_central_core = self.ui.p2_in_is_central_core.isChecked()
        self.ui.p2_out_T_w_check = QCheckBox(self.ui.page_2)
        self.ui.p2_out_T_z_check = QCheckBox(self.ui.page_2)
        self.ui.p2_layout.addWidget(self.ui.p2_out_T_w_check, 12, 7, 1, 1)
        self.ui.p2_layout.addWidget(self.ui.p2_out_T_z_check, 13, 7, 1, 1)

        # default values
        # self.__override_Q()
        self.ui.p2_in_is_windows_on_more_than_one_wall.setEnabled(False)  # todo, not yet implemented
        self.ui.p2_in_is_central_core.setEnabled(False)  # todo, not yet implemented
        self.ui.p2_in_Q.setEnabled(False)
        self.__change_forced_draught()
        self.ui.p2_out_T_w_check.setChecked(True)
        self.ui.p2_out_T_z_check.setChecked(True)

        # signals
        def override_Q():
            self.ui.p2_in_Q.setEnabled(self.ui.p2_in_Q_label.isChecked())
            self.ui.p2_in_q_fd.setEnabled(not self.ui.p2_in_Q_label.isChecked())
            self.ui.p2_out_Q.setEnabled(not self.ui.p2_in_Q_label.isChecked())

        self.ui.p2_in_Q_label.stateChanged.connect(override_Q)
        self.ui.p2_out_T_w_check.stateChanged.connect(lambda: self.ui.p2_out_T_w.setEnabled(self.ui.p2_out_T_w_check.isChecked()))
        self.ui.p2_out_T_z_check.stateChanged.connect(lambda: self.ui.p2_out_T_z.setEnabled(self.ui.p2_out_T_z_check.isChecked()))
        self.ui.p2_in_is_forced_draught.toggled.connect(self.__change_forced_draught)

    def example(self):
        input_kwargs = dict(
            q_fd=870,
            Q=80,
            W_1=1.82,
            W_2=5.46,
            A_f=14.88,
            A_t=70.3,
            h_eq=1.1,
            w_t=1.82,
            A_v=2.002,
            L_x=0.1,
            tau_F=1200,
            rho_g=0.45,
            g=9.81,
            T_0=293.15,
            u=6,
            is_wall_above_opening=True,
            is_windows_on_more_than_one_wall=False,
            is_central_core=False,
            is_forced_draught=False,
            make_pdf_web=False,
            T_z=None,
            T_w=None,
        )

        self.input_parameters = input_kwargs

    @staticmethod
    def calculate(input_kwargs):
        if input_kwargs['is_forced_draught']:
            cls = ExternalFlameForcedDraught(
                alpha_c_beam=None, alpha_c_column=None, T_z_1=None, T_z_2=None, **input_kwargs
            )
        else:
            cls = ExternalFlame(
                alpha_c_beam=None, alpha_c_column=None, **input_kwargs
            )

        try:
            if input_kwargs['make_pdf_web']:
                temp = tempfile.NamedTemporaryFile(suffix='.tex')
                fp_tex = temp.name
                temp.close()
                threading.Thread(target=lambda: cls.make_pdf_web(fp_tex=fp_tex)).start()
        except Exception as e:
            logger.debug(f'{e}')

        return cls.output_kwargs

    def ok(self):

        self.ui.p2_out_Q.setText('')
        self.ui.p2_out_T_f.setText('')
        self.ui.p2_out_L_L.setText('')
        self.ui.p2_out_L_H.setText('')
        self.ui.p2_out_L_f.setText('')
        self.ui.p2_out_T_w.setText('')
        self.ui.p2_out_T_z.setText('')

        try:
            self.output_parameters = self.calculate(self.input_parameters)
            self.statusBar().showMessage('Calculation complete')
        except Exception as e:
            self.statusBar().showMessage(f'{e}', timeout=10 * 1e3)

    @property
    def input_parameters(self):
        def str2float(v: str):
            try:
                return float(v)
            except ValueError:
                return None

        is_forced_draught = self.ui.p2_in_is_forced_draught.isChecked()
        is_wall_above_opening = self.ui.p2_in_is_wall_above_opening.isChecked()
        # is_windows_on_more_than_one_wall = self.ui.p2_in_is_windows_on_more_than_one_wall.isChecked()
        # is_central_core = self.ui.p2_in_is_central_core.isChecked()
        make_pdf_web = self.ui.p2_in_make_pdf_web.isChecked()

        q_fd = str2float(self.ui.p2_in_q_fd.text())
        Q = str2float(self.ui.p2_in_Q.text())
        W_1 = str2float(self.ui.p2_in_W_1.text())
        W_2 = str2float(self.ui.p2_in_W_2.text())
        A_f = str2float(self.ui.p2_in_A_f.text())
        A_t = str2float(self.ui.p2_in_A_t.text())
        h_eq = str2float(self.ui.p2_in_h_eq.text())
        w_t = str2float(self.ui.p2_in_w_t.text())
        A_v = str2float(self.ui.p2_in_A_v.text())
        T_0 = str2float(self.ui.p2_in_T_0.text())
        L_x = str2float(self.ui.p2_in_L_x.text())
        tau_F = str2float(self.ui.p2_in_tau_F.text())
        u = str2float(self.ui.p2_in_u.text())

        if not self.ui.p2_out_T_w_check.isChecked():
            T_w = None
        if not self.ui.p2_out_T_z_check.isChecked():
            T_z = None

        input_kwargs = locals()
        input_kwargs.pop('self')
        input_kwargs.pop('str2float')
        if not self.ui.p2_in_Q_label.isChecked():
            input_kwargs.pop('Q')

        return input_kwargs

    @input_parameters.setter
    def input_parameters(self, v: dict):
        def float2str(v: float):
            if v is None:
                return ''
            else:
                return f'{v:g}'

        self.ui.p2_in_is_forced_draught.setChecked(v['is_forced_draught'])
        self.ui.p2_in_is_wall_above_opening.setChecked(v['is_wall_above_opening'])
        self.ui.p2_in_is_central_core.setChecked(v['is_central_core'])
        self.ui.p2_in_is_windows_on_more_than_one_wall.setChecked(v['is_windows_on_more_than_one_wall'])
        self.ui.p2_in_make_pdf_web.setChecked(v['make_pdf_web'])

        self.ui.p2_in_q_fd.setText(float2str(v['q_fd']))
        self.ui.p2_in_Q.setText(float2str(v['Q']))
        self.ui.p2_in_W_1.setText(float2str(v['W_1']))
        self.ui.p2_in_W_2.setText(float2str(v['W_2']))
        self.ui.p2_in_A_f.setText(float2str(v['A_f']))
        self.ui.p2_in_A_t.setText(float2str(v['A_t']))
        self.ui.p2_in_h_eq.setText(float2str(v['h_eq']))
        self.ui.p2_in_w_t.setText(float2str(v['w_t']))
        self.ui.p2_in_A_v.setText(float2str(v['A_v']))
        self.ui.p2_in_T_0.setText(float2str(v['T_0']))
        self.ui.p2_in_L_x.setText(float2str(v['L_x']))
        self.ui.p2_in_tau_F.setText(float2str(v['tau_F']))
        self.ui.p2_in_u.setText(float2str(v['u']))

        if 'T_w' in v:
            self.ui.p2_out_T_w_check.setChecked(False)
        if 'T_z' in v:
            self.ui.p2_out_T_z_check.setChecked(False)

    @property
    def output_parameters(self):
        def str2float(v: str):
            try:
                return float(v)
            except ValueError:
                return None

        return dict(
            Q=str2float(self.ui.p2_out_Q.text()),
            T_f=str2float(self.ui.p2_out_T_f.text()),
            L_L=str2float(self.ui.p2_out_L_L.text()),
            L_H=str2float(self.ui.p2_out_L_H.text()),
            L_f=str2float(self.ui.p2_out_L_f.text()),
            T_w=str2float(self.ui.p2_out_T_w.text()),
            T_z=str2float(self.ui.p2_out_T_z.text()),
        )

    @output_parameters.setter
    def output_parameters(self, v: dict):

        def float2str(v_: float):
            if v_ is None:
                return ''
            try:
                if v_ > 1e2:
                    return f'{v_:.0f}'
                else:
                    return f'{v_:.3g}'
            except ValueError:
                return ''

        def try_set_text(cls, d: dict, k: str):
            try:
                getattr(cls, 'setText')(float2str(d[k]))
            except KeyError:
                logger.info(f'Key {k} not found in {d.keys()}')

        try_set_text(self.ui.p2_out_Q, v, 'Q')
        try_set_text(self.ui.p2_out_T_f, v, 'T_f')
        try_set_text(self.ui.p2_out_L_L, v, 'L_L')
        try_set_text(self.ui.p2_out_L_H, v, 'L_H')
        try_set_text(self.ui.p2_out_L_f, v, 'L_f')
        try_set_text(self.ui.p2_out_T_w, v, 'T_w')
        try_set_text(self.ui.p2_out_T_z, v, 'T_z')

    def __change_forced_draught(self):
        if self.ui.p2_in_is_forced_draught.isChecked():
            self.__set_enabled_label_input_and_unit(self.ui, 'p2_in_u', True)
            self.ui.p1_figure.setPixmap(join(__root_dir__, 'gui', 'images', f'{self.app_id}-2.png'))

        else:
            self.__set_enabled_label_input_and_unit(self.ui, 'p2_in_u', False)
            self.ui.p1_figure.setPixmap(join(__root_dir__, 'gui', 'images', f'{self.app_id}-1.png'))

    @staticmethod
    def __set_hidden_label_input_and_unit(cls, attr_name: str, is_hidden: bool = True):
        getattr(cls, attr_name).setHidden(is_hidden)
        getattr(cls, f'{attr_name}_label').setHidden(is_hidden)
        getattr(cls, f'{attr_name}_unit').setHidden(is_hidden)

    @staticmethod
    def __set_enabled_label_input_and_unit(cls, attr_name: str, is_enabled: bool = True):
        getattr(cls, attr_name).setEnabled(is_enabled)
        getattr(cls, f'{attr_name}_label').setEnabled(is_enabled)
        getattr(cls, f'{attr_name}_unit').setEnabled(is_enabled)


if __name__ == '__main__':
    from PySide2 import QtWidgets, QtCore
    import PySide2
    import sys

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        PySide2.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        PySide2.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
