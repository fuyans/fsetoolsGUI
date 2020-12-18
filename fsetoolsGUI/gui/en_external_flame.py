import shutil
import tempfile
import threading
from os.path import join

from PySide2.QtWidgets import QVBoxLayout, QGridLayout, QLabel, QCheckBox, QSpacerItem, QSizePolicy
from fsetools.lib.fse_bs_en_1991_1_2_external_flame import ExternalFlame
from fsetools.lib.fse_bs_en_1991_1_2_external_flame_forced_draught import ExternalFlameForcedDraught

from fsetoolsGUI import __root_dir__, logger
from fsetoolsGUI.gui.bases.c9901_app_template import AppBaseClass
from fsetoolsGUI.gui.bases.custom_utilities import Counter


class App(AppBaseClass):
    app_id = '0411'
    app_name_short = 'BS EN 1991\nExternal\nflame'
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
            'Calculation follows Annex B in BS EN 1991-1-2:2002 '
            '"Eurocode 1: Actions on structures – Part 1-2: General actions – Actions on structures exposed to fire"\n'
        )
        self.ui.p1_description.setFixedWidth(440)
        self.ui.p1_description.setWordWrap(True)
        self.ui.p1_layout.addWidget(self.ui.p1_description)
        self.ui.p1_figure = QLabel()
        self.ui.p1_figure.setPixmap(join(__root_dir__, 'gui', 'images', f'{self.app_id}-1.png'))
        self.ui.p1_layout.addWidget(self.ui.p1_figure)

        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_q_fd', '<i>q<sub>fd</sub></i>, design fuel load', 'MJ/m<sup>2</sup>', min_width=60)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_Q', 'Q, HRR (override)', 'MW', label_obj='QCheckBox')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_W_1', '<i>W<sub>1</sub></i>, enclosure dim. 1', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_W_2', '<i>W<sub>2</sub></i>, enclosure dim. 2', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_A_f', '<i>A<sub>f</sub></i>, floor area', 'm<sup>2</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_A_t', '<i>A<sub>t</sub></i>, total surface area', 'm<sup>2</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_h_eq', '<i>h<sub>eq</sub></i>, weighted win. height', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_w_t', '<i>w<sub>t</sub></i>, total win. width', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_T_0', '<i>T<sub>0</sub></i>, Ambient temp.', 'K')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_tau_F', '<i>τ<sub>F</sub></i>, free burning duration', 's')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_L_x', '<i>L<sub>x</sub></i>, length along flame axis', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_u', '<i>u</i>, wind speed', 'm/s')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_L_c', '<i>L<sub>c</sub></i>, core length', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_W_c', '<i>W<sub>c</sub></i>, core depth', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_A_v1', '<i>A<sub>v1</sub></i>, win. area on wall 1', 'm<sup>2</sup>')

        self.ui.p2_layout.addItem(QSpacerItem(10, 1, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 3, 1, 1)

        c.reset()
        self.ui.p2_layout.addWidget(QLabel('<b>Options</b>'), c.count, 4, 1, 4)
        self.ui.p2_in_is_forced_draught = QCheckBox('Is forced draught?')
        self.ui.p2_in_is_wall_above_opening = QCheckBox('Is wall above opening?')
        self.ui.p2_in_is_windows_on_more_than_one_wall = QCheckBox('Win. on more than 1 wall?')
        self.ui.p2_in_is_central_core = QCheckBox('Is central core present?')
        self.ui.p2_in_make_pdf = QCheckBox('Make PDF report?')
        self.ui.p2_layout.addWidget(self.ui.p2_in_is_forced_draught, c.count, 4, 1, 4)
        self.ui.p2_layout.addWidget(self.ui.p2_in_is_wall_above_opening, c.count, 4, 1, 4)
        self.ui.p2_layout.addWidget(self.ui.p2_in_is_windows_on_more_than_one_wall, c.count, 4, 1, 4)
        self.ui.p2_layout.addWidget(self.ui.p2_in_is_central_core, c.count, 4, 1, 4)
        self.ui.p2_layout.addWidget(self.ui.p2_in_make_pdf, c.count, 4, 1, 4)

        c.reset(8)
        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), c.count, 4, 1, 4)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_out_Q', 'HRR', 'MW', col=4, min_width=60)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_out_L_L', '<i>L<sub>L</sub></i>', 'm', col=4)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_out_L_H', '<i>L<sub>H</sub></i>', 'm', col=4)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_out_L_f', '<i>L<sub>f</sub></i>', 'm', col=4)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_out_T_f', '<i>T<sub>f</sub></i>', 'K', col=4)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_out_T_w', '<i>T<sub>w</sub></i>', 'K', col=4)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_out_T_z', '<i>T<sub>z</sub></i>', 'K', col=4)
        self.ui.p2_out_T_f_check = QCheckBox(self.ui.page_2)
        self.ui.p2_out_T_w_check = QCheckBox(self.ui.page_2)
        self.ui.p2_out_T_z_check = QCheckBox(self.ui.page_2)
        c.reset(13)
        self.ui.p2_layout.addWidget(self.ui.p2_out_T_f_check, c.count, 7, 1, 1)
        self.ui.p2_layout.addWidget(self.ui.p2_out_T_w_check, c.count, 7, 1, 1)
        self.ui.p2_layout.addWidget(self.ui.p2_out_T_z_check, c.count, 7, 1, 1)

        # default values
        self.ui.p2_in_is_forced_draught.setChecked(True)
        self.ui.p2_in_tau_F.setText('1200')
        self.ui.p2_in_T_0.setText('293.15')
        self.ui.p2_in_Q_label.setChecked(True)
        self.ui.p2_out_T_f_check.setChecked(True)
        self.ui.p2_out_T_w_check.setChecked(True)
        self.ui.p2_out_T_z_check.setChecked(True)

        # signals
        def is_forced_draught():
            self.ui.p2_in_A_t.setEnabled(self.ui.p2_out_T_f_check.isChecked() or not self.ui.p2_in_Q_label.isChecked() or self.ui.p2_in_is_forced_draught.isChecked())
            self.ui.p2_in_u.setEnabled(self.ui.p2_in_is_forced_draught.isChecked())
            if self.ui.p2_in_is_forced_draught.isChecked():
                self.ui.p1_figure.setPixmap(join(__root_dir__, 'gui', 'images', f'{self.app_id}-2.png'))
            else:
                self.ui.p1_figure.setPixmap(join(__root_dir__, 'gui', 'images', f'{self.app_id}-1.png'))

        def is_central_core():
            self.ui.p2_in_L_c.setEnabled(self.ui.p2_in_is_central_core.isChecked() and not self.ui.p2_in_Q_label.isChecked())
            self.ui.p2_in_W_c.setEnabled(self.ui.p2_in_is_central_core.isChecked() and not self.ui.p2_in_Q_label.isChecked())
            self.ui.p2_in_A_v1.setEnabled(
                (self.ui.p2_in_is_windows_on_more_than_one_wall.isChecked() or self.ui.p2_in_is_central_core.isChecked()) and not self.ui.p2_in_Q_label.isChecked()
            )

        def is_windows_on_more_than_one_wall():
            self.ui.p2_in_A_v1.setEnabled(
                (self.ui.p2_in_is_windows_on_more_than_one_wall.isChecked() or self.ui.p2_in_is_central_core.isChecked()) and not self.ui.p2_in_Q_label.isChecked()
            )

        def override_Q():
            self.ui.p2_in_Q.setEnabled(self.ui.p2_in_Q_label.isChecked())
            self.ui.p2_in_is_windows_on_more_than_one_wall.setEnabled(not self.ui.p2_in_Q_label.isChecked())
            self.ui.p2_in_is_central_core.setEnabled(not self.ui.p2_in_Q_label.isChecked())
            self.ui.p2_in_q_fd.setEnabled(not self.ui.p2_in_Q_label.isChecked())
            self.ui.p2_in_W_1.setEnabled(not self.ui.p2_in_Q_label.isChecked())
            self.ui.p2_in_W_2.setEnabled(not self.ui.p2_in_Q_label.isChecked())
            self.ui.p2_in_A_f.setEnabled(not self.ui.p2_in_Q_label.isChecked())
            self.ui.p2_in_A_t.setEnabled(self.ui.p2_out_T_f_check.isChecked() or not self.ui.p2_in_Q_label.isChecked() or self.ui.p2_in_is_forced_draught.isChecked())
            self.ui.p2_in_tau_F.setEnabled(not self.ui.p2_in_Q_label.isChecked())
            self.ui.p2_in_L_c.setEnabled(self.ui.p2_in_is_central_core.isChecked() and not self.ui.p2_in_Q_label.isChecked())
            self.ui.p2_in_W_c.setEnabled(self.ui.p2_in_is_central_core.isChecked() and not self.ui.p2_in_Q_label.isChecked())
            self.ui.p2_in_A_v1.setEnabled(
                (self.ui.p2_in_is_windows_on_more_than_one_wall.isChecked() or self.ui.p2_in_is_central_core.isChecked()) and not self.ui.p2_in_Q_label.isChecked()
            )
            self.ui.p2_out_Q.setEnabled(not self.ui.p2_in_Q_label.isChecked())

        def T_f_check():
            self.ui.p2_out_T_f.setEnabled(self.ui.p2_out_T_f_check.isChecked())
            self.ui.p2_in_A_t.setEnabled(self.ui.p2_out_T_f_check.isChecked() or not self.ui.p2_in_Q_label.isChecked() or self.ui.p2_in_is_forced_draught.isChecked())

        def T_z_check():
            self.ui.p2_in_L_x.setEnabled(self.ui.p2_out_T_z_check.isChecked())
            self.ui.p2_out_T_w_check.setChecked(self.ui.p2_out_T_z_check.isChecked() or self.ui.p2_out_T_w_check.isChecked())
            self.ui.p2_out_T_z.setEnabled(self.ui.p2_out_T_z_check.isChecked())

        self.ui.p2_in_Q_label.stateChanged.connect(override_Q)
        self.ui.p2_in_is_forced_draught.stateChanged.connect(is_forced_draught)
        self.ui.p2_in_is_central_core.stateChanged.connect(is_central_core)
        self.ui.p2_in_is_windows_on_more_than_one_wall.stateChanged.connect(is_windows_on_more_than_one_wall)
        self.ui.p2_out_T_f_check.stateChanged.connect(T_f_check)
        self.ui.p2_out_T_w_check.stateChanged.connect(lambda: self.ui.p2_out_T_w.setEnabled(self.ui.p2_out_T_w_check.isChecked()))
        self.ui.p2_out_T_z_check.stateChanged.connect(T_z_check)

        # set UI default with signals/slots affects
        self.ui.p2_in_is_forced_draught.setChecked(False)
        self.ui.p2_out_T_z_check.setChecked(False)
        self.ui.p2_out_T_w_check.setChecked(False)
        self.ui.p2_out_T_f_check.setChecked(False)
        self.ui.p2_in_Q_label.setChecked(False)

    def example(self):
        input_kwargs = dict(
            q_fd=870,
            Q=None,
            W_1=1.82,
            W_2=5.46,
            A_f=14.88,
            A_t=70.3,
            h_eq=1.1,
            w_t=1.82,
            L_x=0.1,
            tau_F=1200,
            rho_g=0.45,
            g=9.81,
            T_0=293.15,
            u=6,
            L_c=None,
            W_c=None,
            A_v1=None,
            is_wall_above_opening=True,
            is_windows_on_more_than_one_wall=False,
            is_central_core=False,
            is_forced_draught=False,
            make_pdf=False,
            T_f=None,
            T_z=None,
            T_w=None,
        )
        self.input_parameters = input_kwargs

    @staticmethod
    def calculate(input_kwargs):
        if input_kwargs['is_forced_draught']:
            cls = ExternalFlameForcedDraught(alpha_c_beam=None, alpha_c_column=None, T_z_1=None, T_z_2=None, **input_kwargs)
        else:
            cls = ExternalFlame(alpha_c_beam=None, alpha_c_column=None, **input_kwargs)
        return cls

    def submit(self):

        self.ui.p2_out_Q.setText('')
        self.ui.p2_out_T_f.setText('')
        self.ui.p2_out_L_L.setText('')
        self.ui.p2_out_L_H.setText('')
        self.ui.p2_out_L_f.setText('')
        self.ui.p2_out_T_w.setText('')
        self.ui.p2_out_T_z.setText('')

        try:
            logger.info('Calculation started ...')
            cls = self.calculate(self.input_parameters)
            self.output_parameters = cls.output_kwargs
            logger.info('Successfully completed calculation')
            self.statusBar().showMessage('Calculation complete', timeout=10 * 1e3)
        except Exception as e:
            logger.error(f'Failed to complete calculation, {e}')
            self.statusBar().showMessage(f'{e}', timeout=10 * 1e3)
            raise e

        if self.ui.p2_in_make_pdf.isChecked():
            logger.info('Making local PDF ...')
            self.statusBar().showMessage('Making local PDF ...', timeout=10 * 1e3)
            try:
                if shutil.which('latexmk'):
                    temp = tempfile.NamedTemporaryFile(suffix='.pdf')
                    temp.close()
                    fp_pdf = temp.name
                    logger.info(f'Making local PDF ... {fp_pdf}')
                    threading.Thread(target=lambda: cls.make_pdf(fp_pdf=fp_pdf)).start()
                else:
                    temp = tempfile.NamedTemporaryFile(suffix='.tex', )
                    temp.close()
                    fp_tex = temp.name
                    logger.info(f'Making online PDF ... {fp_tex}')
                    threading.Thread(target=lambda: cls.make_pdf_web(fp_tex=fp_tex)).start()
            except Exception as e:
                logger.error(f'Failed to make PDF, {e}')

    @property
    def input_parameters(self):
        def str2float(v: str):
            try:
                return float(v)
            except ValueError:
                return None

        is_forced_draught = self.ui.p2_in_is_forced_draught.isChecked()
        is_wall_above_opening = self.ui.p2_in_is_wall_above_opening.isChecked()
        is_windows_on_more_than_one_wall = self.ui.p2_in_is_windows_on_more_than_one_wall.isChecked()
        is_central_core = self.ui.p2_in_is_central_core.isChecked()
        make_pdf = self.ui.p2_in_make_pdf.isChecked()

        q_fd = str2float(self.ui.p2_in_q_fd.text())
        Q = str2float(self.ui.p2_in_Q.text())
        W_1 = str2float(self.ui.p2_in_W_1.text())
        W_2 = str2float(self.ui.p2_in_W_2.text())
        A_f = str2float(self.ui.p2_in_A_f.text())
        A_t = str2float(self.ui.p2_in_A_t.text())
        h_eq = str2float(self.ui.p2_in_h_eq.text())
        w_t = str2float(self.ui.p2_in_w_t.text())
        T_0 = str2float(self.ui.p2_in_T_0.text())
        L_x = str2float(self.ui.p2_in_L_x.text())
        tau_F = str2float(self.ui.p2_in_tau_F.text())
        u = str2float(self.ui.p2_in_u.text())
        L_c = str2float(self.ui.p2_in_L_c.text())
        W_c = str2float(self.ui.p2_in_W_c.text())
        A_v1 = str2float(self.ui.p2_in_A_v1.text())

        input_kwargs = locals()
        input_kwargs.pop('self')
        input_kwargs.pop('str2float')

        for k in list(input_kwargs.keys()):
            if input_kwargs[k] is None:
                input_kwargs.pop(k)

        if not self.ui.p2_in_Q_label.isChecked() and 'Q' in input_kwargs:
            input_kwargs.pop('Q')

        # assign None to unchecked outputs so the calculation ignores them
        if not self.ui.p2_out_T_f_check.isChecked():
            input_kwargs['T_f'] = None
        if not self.ui.p2_out_T_w_check.isChecked():
            input_kwargs['T_w'] = None
        if not self.ui.p2_out_T_z_check.isChecked():
            input_kwargs['T_z'] = None

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
        self.ui.p2_in_Q_label.setChecked(v['Q'] is not None)
        self.ui.p2_in_make_pdf.setChecked(v['make_pdf'])

        self.ui.p2_in_q_fd.setText(float2str(v['q_fd']))
        self.ui.p2_in_Q.setText(float2str(v['Q']))
        self.ui.p2_in_W_1.setText(float2str(v['W_1']))
        self.ui.p2_in_W_2.setText(float2str(v['W_2']))
        self.ui.p2_in_A_f.setText(float2str(v['A_f']))
        self.ui.p2_in_A_t.setText(float2str(v['A_t']))
        self.ui.p2_in_h_eq.setText(float2str(v['h_eq']))
        self.ui.p2_in_w_t.setText(float2str(v['w_t']))
        # self.ui.p2_in_A_v.setText(float2str(v['A_v']))
        self.ui.p2_in_T_0.setText(float2str(v['T_0']))
        self.ui.p2_in_L_x.setText(float2str(v['L_x']))
        self.ui.p2_in_tau_F.setText(float2str(v['tau_F']))
        self.ui.p2_in_u.setText(float2str(v['u']))
        self.ui.p2_in_L_c.setText(float2str(v['L_c']))
        self.ui.p2_in_W_c.setText(float2str(v['W_c']))
        self.ui.p2_in_A_v1.setText(float2str(v['A_v1']))

        if 'T_f' in v:
            self.ui.p2_out_T_f_check.setChecked(False)
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

        # a helper function to set float to QLineEdit
        def try_set_text(cls, v_):
            try:
                if v_ > 1e2:
                    v_ = f'{v_:.0f}'
                else:
                    v_ = f'{v_:.3g}'
            except (ValueError, TypeError):
                v_ = ''
            getattr(cls, 'setText')(v_)

        try_set_text(self.ui.p2_out_Q, v['Q'])
        try_set_text(self.ui.p2_out_T_f, v['T_f'])
        try_set_text(self.ui.p2_out_L_L, v['L_L'])
        try_set_text(self.ui.p2_out_L_H, v['L_H'])
        try_set_text(self.ui.p2_out_L_f, v['L_f'])
        try_set_text(self.ui.p2_out_T_w, v['T_w'])
        try_set_text(self.ui.p2_out_T_z, v['T_z'])

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
    from PySide2 import QtWidgets
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
