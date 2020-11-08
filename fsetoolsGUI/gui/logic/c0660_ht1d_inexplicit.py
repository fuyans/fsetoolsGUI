from os.path import basename

import numpy as np
from PySide2.QtWidgets import QGridLayout, QLabel
from fsetools.ht1d.ht1d_inexplicit import main as ht1d_main
from scipy.interpolate import interp1d

from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.custom_plot import App as PlotApp
from fsetoolsGUI.gui.logic.custom_table import TableWindow
from matplotlib import cm
from fsetoolsGUI import logger


class App(AppBaseClass):
    app_id = basename(__file__)[1:5]
    app_name_short = 'HT1D\nInexplicit'
    app_name_long = 'HT1D 1-dimensional heat transfer (inexplicit)'

    def __init__(self, parent=None, post_stats: bool = True):

        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)

        self.FigureApp = PlotApp(parent=self, title='Parametric fire plot')
        self.TableApp = TableWindow(parent=self, window_title='Parametric fire results')
        self.__figure_ax = self.FigureApp.add_subplot()
        self.__figure_cb = None
        self.__output_parameters = None

        # ================
        # instantiation ui
        # ================
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5), self.ui.p2_layout.setVerticalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), 0, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 1, 'p2_in_n_nodes', 'No. of nodes', None)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 2, 'p2_in_dx', 'dx', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 3, 'p2_in_t_end', 't<sub>end</sub>', 's')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 4, 'p2_in_dt', 'dt', 's')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 5, 'p2_in_T_init', 'T<sub>init</sub>', '°C')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 6, 'p2_in_T_boundary_0', 'T<sub>bound,0</sub>', 's, °C;')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 7, 'p2_in_k', 'k', 'W/m/K')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 8, 'p2_in_rho', 'rho', 'kg/m<sup>3</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 9, 'p2_in_c', 'c', 'J/K/kg')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 10, 'p2_in_tol', 'tol', None)

        # =================
        # lineEdit tip text
        # =================

    def example(self):

        self.input_parameters = dict(
            n_nodes=21,
            T_init=20,
            tol=1e-3,
            t_end=7200,
            dt=5,
            dx=0.005,
            T_boundary_0='0, 20; 3600, 1200; 7200, 20',
            k=0.12,
            rho=600,
            c=1500,
        )

        self.repaint()

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

        n_nodes = int(self.ui.p2_in_n_nodes.text())
        dx = str2float(self.ui.p2_in_dx.text())
        t_end = str2float(self.ui.p2_in_t_end.text())
        dt = str2float(self.ui.p2_in_dt.text())
        T_init = str2float(self.ui.p2_in_T_init.text())
        T_boundary_0_raw = self.ui.p2_in_T_boundary_0.text()
        k = str2float(self.ui.p2_in_k.text())
        rho = str2float(self.ui.p2_in_rho.text())
        c = str2float(self.ui.p2_in_c.text())
        tol = str2float(self.ui.p2_in_tol.text())

        _ = T_boundary_0_raw.replace(';', ',').split(',')
        t = _[0::2]
        T = _[1::2]

        t = [str2float(i.strip()) for i in t]
        T = [str2float(i.strip()) for i in T]
        T_boundary_0 = interp1d(t, T, bounds_error=False)

        return dict(
            n_nodes=n_nodes, dx=dx, t_end=t_end, dt=dt, T_init=T_init, T_boundary_0=T_boundary_0, k=k, rho=rho, c=c, tol=tol,
        )

    @input_parameters.setter
    def input_parameters(self, v):

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

        self.ui.p2_in_n_nodes.setText(num2str(v['n_nodes']))
        self.ui.p2_in_dx.setText(num2str(v['dx']))
        self.ui.p2_in_t_end.setText(num2str(v['t_end']))
        self.ui.p2_in_dt.setText(num2str(v['dt']))
        self.ui.p2_in_T_init.setText(num2str(v['T_init']))
        self.ui.p2_in_T_boundary_0.setText(v['T_boundary_0'])
        self.ui.p2_in_k.setText(num2str(v['k']))
        self.ui.p2_in_rho.setText(num2str(v['rho']))
        self.ui.p2_in_c.setText(num2str(v['c']))
        self.ui.p2_in_tol.setText(num2str(v['tol']))

    @property
    def output_parameters(self) -> dict:
        return self.__output_parameters

    @output_parameters.setter
    def output_parameters(self, v: dict):
        self.__output_parameters = v

    @staticmethod
    def __calculate(
            n_nodes,
            dx,
            t_end,
            dt,
            T_init,
            T_boundary_0,
            k,
            rho,
            c,
            tol,
    ):
        T = ht1d_main(
            n_nodes=n_nodes,
            dx=dx,
            t_end=t_end,
            dt=dt,
            T_init=T_init,
            T_boundary_0=T_boundary_0,
            k=k,
            rho=rho,
            c=c,
            tol=tol,
        )

        return dict(T=T)

    def ok(self):
        # parse inputs from ui
        try:
            self.statusBar().showMessage('Parsing inputs from UI')
            self.repaint()
            input_parameters = self.input_parameters
        except Exception as e:
            logger.error(f'Unable to parse input. {str(e)}')
            self.statusBar().showMessage(f'Unable to parse input. {str(e)}')
            return

        # calculate
        try:
            self.statusBar().showMessage('Calculation started')
            self.repaint()
            self.output_parameters = self.__calculate(**input_parameters)
            self.statusBar().showMessage('Calculation completed')
        except Exception as e:
            logger.error(f'Calculation failed. Error {str(e)}')
            self.statusBar().showMessage(f'Calculation incomplete, {type(e).__name__} {e.args}')
            return
        # self.show_results_in_table()
        self.show_results_in_figure()

    def show_results_in_table(self):

        output_parameters = self.output_parameters

        # print results (for console enabled version only)
        list_content = [
            [float(i), float(j)] for i, j in zip(output_parameters['time'], output_parameters['temperature'] - 273.15)
        ]

        self.TableApp.update_table_content(
            content_data=list_content,
            col_headers=['time [s]', 'temperature [°C]'],
        )
        self.TableApp.show()

    def show_results_in_figure(self):

        output_parameters = self.output_parameters
        input_parameters = self.input_parameters

        self.__figure_ax.clear()
        # if self.__figure_cb is not None:
        #     self.__figure_cb.remove()
        #     self.FigureApp.figure_canvas.draw()

        l = np.linspace(0, (input_parameters['n_nodes'] - 1) * input_parameters['dx'], input_parameters['n_nodes'])
        t = np.arange(0, input_parameters['t_end'] + input_parameters['dt'] / 2, input_parameters['dt'])

        xx, yy = np.meshgrid(t / 60., l)
        zz = output_parameters['T'].T

        csf = self.__figure_ax.contourf(xx, yy, zz, cmap=cm.get_cmap('viridis'))
        if self.__figure_cb is not None:
            self.__figure_cb.update_normal(csf)
        else:
            self.__figure_cb = self.FigureApp.figure.colorbar(csf, ax=self.__figure_ax, shrink=0.9)
        self.__figure_cb.set_ticks(np.linspace(np.amin(zz), np.amax(zz), 10, endpoint=True))
        self.__figure_cb.set_clim(vmin=np.amin(zz), vmax=np.amax(zz))

        self.__figure_ax.set_xlabel('Time [minute]', fontsize='small')
        self.__figure_ax.set_ylabel('Depth [m]', fontsize='small')
        self.__figure_ax.tick_params(axis='both', labelsize='small')
        self.__figure_ax.grid(which='major', linestyle=':', linewidth='0.5', color='black')

        self.FigureApp.figure.tight_layout()

        self.FigureApp.show()
        self.FigureApp.refresh_figure()


if __name__ == '__main__':
    from PySide2 import QtWidgets
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
