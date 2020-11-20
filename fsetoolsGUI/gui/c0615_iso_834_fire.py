import numpy as np
from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout, QLabel

from fsetoolsGUI import logger
from fsetoolsGUI.gui.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.c0000_utilities import Counter
from fsetoolsGUI.gui.custom_plot import App as PlotApp
from fsetoolsGUI.gui.custom_table import TableWindow


def calculate_worker(
        t_end: float,
        t_step: float,
        *_, **__,
):
    """
    ISO 834 standard fire curve
    Signature to match the keys of `App.symbols_inputs`
    Return dict keys to match the keys of `App.symbols.outputs`

    :param t_end: [min]
    :param t_step: [s]
    :return temperature: [K]
    """

    # Unit conversion
    t_end = t_end * 60.  # min -> s

    t = np.arange(0, t_end + t_step / 2., t_step)

    temperature_ = (345.0 * np.log10((t / 60.0) * 8.0 + 1.0) + 20.0) + 273.15

    return dict(
        time=t,
        temperature=temperature_,
    )


class App(AppBaseClass):
    app_id = '0613'
    app_name_short = 'ISO 834\nstandard\nfire'
    app_name_long = 'ISO 834 standard fire'

    # Keys to match signature of `heat_flux_wrapper`
    symbols_inputs = dict(
        t_end=dict(description='<i>t<sub>end</sub></i>, fire time duration', unit='min', default=180.),
        t_step=dict(description='<i>t<sub>step</sub></i>, fire time step', unit='s', default=1.),
    )
    # Keys to match output keys of `heat_flux_wrapper`
    symbols_outputs = dict()

    def __init__(self, parent=None, post_stats: bool = True):

        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)

        self.FigureApp = PlotApp(parent=self, title='ISO 834 fire plot')
        self.TableApp = TableWindow(parent=self, window_title='ISO 834 fire results')
        self.__figure_ax = self.FigureApp.add_subplot()
        self.__output_parameters = dict(time=None, temperature=None)
        self.__input_parameters: dict = dict()
        self.__output_parameters: dict = dict()

        # ================
        # instantiation ui
        # ================
        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5), self.ui.p2_layout.setVerticalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        for k, v in self.symbols_inputs.items():
            self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_' + k, v['description'], v['unit'], min_width=70)

        if self.symbols_outputs:
            self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), c.count, 0, 1, 3)
            for k, v in self.symbols_outputs.items():
                self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_out_' + k, v['description'], v['unit'])
                getattr(self.ui, 'p2_out_' + k).setReadOnly(True)

    def example(self):
        self.input_parameters = {k: v['default'] for k, v in self.symbols_inputs.items()}

    @property
    def input_parameters(self):

        def str2float(v):
            try:
                return float(v)
            except:
                return None

        # ====================
        # parse values from ui
        # ====================
        input_parameters = dict()
        for k, v in self.symbols_inputs.items():
            input_parameters[k] = str2float(getattr(self.ui, 'p2_in_' + k).text())

        try:
            self.__input_parameters.update(input_parameters)
        except TypeError:
            self.__input_parameters = input_parameters

        return self.__input_parameters

    @input_parameters.setter
    def input_parameters(self, v):
        for k, v_ in self.symbols_inputs.items():
            getattr(self.ui, 'p2_in_' + k).setText(self.num2str(v[k]))

    @property
    def output_parameters(self) -> dict:
        return self.__output_parameters

    @output_parameters.setter
    def output_parameters(self, v: dict):
        self.__output_parameters = v

        for k, v_ in self.symbols_outputs.items():
            getattr(self.ui, 'p2_out_' + k).setText(self.num2str(v[k]))

    def ok(self):
        # parse inputs from ui
        try:
            self.statusBar().showMessage('Parsing inputs from UI')
            self.repaint()
            input_parameters = self.input_parameters
        except Exception as e:
            self.statusBar().showMessage(f'Unable to parse input. {str(e)}')
            return

        # calculate
        try:
            self.statusBar().showMessage('Calculation started')
            self.repaint()
            output_parameters = calculate_worker(**input_parameters)
        except Exception as e:
            self.statusBar().showMessage(f'Calculation failed. Error {str(e)}')
            raise e

        # cast outputs to ui
        try:
            self.statusBar().showMessage('Preparing results')
            self.repaint()
            self.output_parameters = output_parameters
            self.show_results_in_table()
            self.show_results_in_figure()
        except Exception as e:
            self.statusBar().showMessage(f'Unable to show results, {str(e)}')
            logger.error(f'Unable to show results, {str(e)}')

        self.statusBar().showMessage('Calculation complete')

    def show_results_in_table(self):

        output_parameters = self.output_parameters

        # print results (for console enabled version only)
        list_content = [
            [float(i), float(j)] for i, j in zip(output_parameters['time'], output_parameters['temperature'] - 273.15)
        ]

        self.TableApp.update_table_content(
            content_data=list_content,
            col_headers=['Time [s]', 'Temperature [°C]'],
        )
        self.TableApp.show()

        return True

    def show_results_in_figure(self):

        output_parameters = self.output_parameters

        self.__figure_ax.clear()
        self.__figure_ax.plot(output_parameters['time'] / 60., output_parameters['temperature'] - 273.15, c='k')
        self.__figure_ax.set_xlabel('Time [minute]', fontsize='small')
        self.__figure_ax.set_ylabel('Temperature [°C]', fontsize='small')
        self.__figure_ax.tick_params(axis='both', labelsize='small')
        self.__figure_ax.grid(which='major', linestyle=':', linewidth='0.5', color='black')

        self.FigureApp.show()
        self.FigureApp.refresh_figure()

        return True

    @staticmethod
    def num2str(num):
        if isinstance(num, int):
            return f'{num:g}'
        elif isinstance(num, float):
            return f'{num:.3f}'.rstrip('0').rstrip('.')
        elif isinstance(num, str):
            return num
        elif num is None:
            return ''
        else:
            return str(num)


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
