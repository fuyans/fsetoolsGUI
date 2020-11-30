import shutil
import tempfile
import threading
from collections import OrderedDict
from os.path import join

from PySide2.QtWidgets import QVBoxLayout, QGridLayout, QLabel, QSpacerItem, QSizePolicy, QCheckBox
from fsetools.lib.fse_bs_en_1993_1_2_external_column import ExternalSteelTemperatureFullyEngulfedColumn

from fsetoolsGUI import __root_dir__, logger
from fsetoolsGUI.gui.c9901_app_template import AppBaseClass
from fsetoolsGUI.gui.custom_utilities import Counter


class App(AppBaseClass):
    app_id = '0311'
    app_name_short = 'BS EN 1993\nExternal\ncolumn temp.'
    app_name_long = 'BS EN 1993-1-2:2005 External column temperatures'

    def __init__(self, parent=None, post_stats: bool = True):

        # instantiation
        super().__init__(parent, post_stats)

        self.input_symbols: OrderedDict = OrderedDict(
            C_1=['<i>C<sub>1</sub></i>, face 1 protection coef.', '-'],
            C_2=['<i>C<sub>2</sub></i>, face 2 protection coef.', '-'],
            C_3=['<i>C<sub>3</sub></i>, face 3 protection coef.', '-'],
            C_4=['<i>C<sub>4</sub></i>, face 4 protection coef.', '-'],
            lambda_1=['<i>λ<sub>1</sub></i>, flame thickness to face 1', 'm'],
            lambda_3=['<i>λ<sub>1</sub></i>, flame thickness to face 3', 'm'],
            d_1=['<i>d<sub>1</sub></i>, steel sec. dim. 1', 'm'],
            d_2=['<i>d<sub>2</sub></i>, steel sec. dim. 2', 'm'],
            Q=['<i>Q</i>, HRR', 'MW'],
            w_t=['<i>w<sub>t</sub></i>, opening width', 'm'],
            L_H=['<i>L<sub>H</sub></i>, flame h. projection', 'm'],
            L_L=['<i>L<sub>L</sub></i>, flame v. projection', 'm'],
            h_eq=['<i>h<sub>eq</sub></i>, opening height', 'm'],
            T_f=['<i>T<sub>f</sub></i>, temp. in the enclosure', 'K'],
            T_z=['<i>T<sub>z</sub></i>, temp. at L<sub>x</sub>', 'K'],
            T_o=['<i>T<sub>o</sub></i>, temp. at opening', 'K'],
        )
        self.output_symbols: OrderedDict = OrderedDict(
            # I_z=['Radiative h. t. from flames', 'kW/m<sup>2</sup>'],
            # I_f=['Radiative h. t. from openings', 'kW/m<sup>2</sup>'],
            T_m_1=['<i>T<sub>m,1</sub></i>, temp. at face 1', 'K'],
            T_m_2=['<i>T<sub>m,2</sub></i>, temp. at face 2', 'K'],
            T_m_3=['<i>T<sub>m,3</sub></i>, temp. at face 3', 'K'],
            T_m_4=['<i>T<sub>m,4</sub></i>, temp. at face 4', 'K'],
            T_m=['<i>T<sub>m</sub></i>, average temp.', 'K'],
        )

        # instantiate UI
        self.ui.p1_layout = QVBoxLayout(self.ui.page_1)
        self.ui.p1_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.p1_description = QLabel(
            'This app calculates the temperatures of an external steel column.\n\n'
            'Calculation follows Annex B in '
            '"Eurocode 3: Design of steel structures — Part 1-2: General rules — Structural fire design" '
            '(BS EN 1991-1-3).\n\n'
            'This app considers only an external steel column opposite to an window.\n'
        )
        self.ui.p1_description.setFixedWidth(400)
        self.ui.p1_description.setWordWrap(True)
        self.ui.p1_layout.addWidget(self.ui.p1_description)
        self.ui.p1_figure = QLabel()
        self.ui.p1_figure.setPixmap(join(__root_dir__, 'gui', 'images', f'{self.app_id}-1.png'))
        self.ui.p1_layout.addWidget(self.ui.p1_figure)

        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        for k, v in self.input_symbols.items():
            self.add_lineedit_set_to_grid(self.ui.p2_layout, c, f'p2_in_{k}', v[0], v[1])

        self.ui.p2_layout.addItem(QSpacerItem(10, 1, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 3, 1, 1)

        c.reset()
        self.ui.p2_layout.addWidget(QLabel('<b>Options</b>'), c.count, 4, 1, 4)
        self.ui.p2_in_is_forced_draught = QCheckBox('Is forced draught?')
        self.ui.p2_in_make_pdf = QCheckBox('Make PDF report?')
        self.ui.p2_layout.addWidget(self.ui.p2_in_is_forced_draught, c.count, 4, 1, 4)
        self.ui.p2_layout.addWidget(self.ui.p2_in_make_pdf, c.count, 4, 1, 4)

        c.reset(c.count + 8)
        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), c.count, 4, 1, 3)
        for k, v in self.output_symbols.items():
            self.add_lineedit_set_to_grid(self.ui.p2_layout, c, f'p2_out_{k}', v[0], v[1], col=4)

        self.ui.p2_in_is_forced_draught.stateChanged.connect(
            lambda: self.ui.p1_figure.setPixmap(
                join(__root_dir__, 'gui', 'images', f'{self.app_id}-2.png' if self.ui.p2_in_is_forced_draught.isChecked() else f'{self.app_id}-1.png')))

    def example(self):
        input_kwargs = dict(
            C_1=1,
            C_2=1,
            C_3=1,
            C_4=1,
            lambda_1=10.1,
            lambda_3=0.59,
            Q=200,
            T_f=1330,
            T_z=975,
            T_o=984,
            # T_0=293.15,
            d_1=0.4,
            d_2=1.,
            w_t=20.9,
            L_H=6.68,
            L_L=3.39,
            h_eq=3.3,
            # alpha=0.0065,
            # w_f=20.9,
        )
        self.input_parameters = input_kwargs

    @staticmethod
    def calculate(input_kwargs):
        input_kwargs['is_fully_engulfed'] = True  # todo
        # input_kwargs['is_forced_draught'] = False  # todo
        if input_kwargs['is_fully_engulfed']:
            cls = ExternalSteelTemperatureFullyEngulfedColumn(sigma=5.67e-11, **input_kwargs)
        else:
            raise NotImplementedError('Column not or partially engulfed within flames is currently not implemented')
        return cls

    def ok(self):
        try:
            cls = self.calculate(self.input_parameters)
            self.output_parameters = cls.output_kwargs
            self.statusBar().showMessage('Calculation complete', timeout=10 * 1e3)
        except Exception as e:
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

        input_parameters = {k: str2float(getattr(self.ui, f'p2_in_{k}').text()) for k in list(self.input_symbols.keys())}
        input_parameters['is_forced_draught'] = self.ui.p2_in_is_forced_draught.isChecked()
        logger.info(f'Inputs: {input_parameters}')
        return input_parameters

    @input_parameters.setter
    def input_parameters(self, v: dict):
        def float2str(num: float):
            if num is None:
                return ''
            else:
                return f'{num:g}'

        for k, v_ in v.items():
            getattr(self.ui, f'p2_in_{k}').setText(float2str(v_))

    @property
    def output_parameters(self):
        raise NotImplementedError

    @output_parameters.setter
    def output_parameters(self, v: dict):
        def float2str(num: float):
            if num is None:
                return ''
            else:
                return f'{num:g}'

        for k in self.output_symbols.keys():
            getattr(self.ui, f'p2_out_{k}').setText(float2str(v[k]))


if __name__ == '__main__':
    from PySide2 import QtWidgets
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
