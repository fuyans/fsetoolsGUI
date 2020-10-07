from typing import List

import numpy as np
from PySide2 import QtCore
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QGridLayout, QLabel
from fsetools.lib.fse_thermal_radiation_2d_ortho import Emitter, Receiver
from matplotlib import cm

from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.c0000_utilities import Counter
from fsetoolsGUI.gui.logic.custom_plot import App as FigureApp
from fsetoolsGUI.gui.logic.custom_table import TableApp2


class Signals(QtCore.QObject):
    __update_progress_bar_signal = QtCore.Signal(int)
    __calculation_complete = QtCore.Signal(bool)

    @property
    def update_progress_bar_signal(self):
        return self.__update_progress_bar_signal

    @property
    def calculation_complete(self):
        return self.__calculation_complete


class App(AppBaseClass):
    app_id = '0406'
    app_name_short = 'TRA\n2D\nparallel'
    app_name_long = 'TRA 2D parallel orientated emitters contour plot'

    def __init__(self, parent=None, post_stats: bool = True):
        super().__init__(parent=parent, post_stats=post_stats, ui=AppBaseClassUISimplified01)
        self.__input_parameters = dict()
        self.__output_parameters = dict()
        self.TableAppReceiver = TableApp2(parent=self, window_title='Receivers')
        self.TableAppEmitter = TableApp2(parent=self, window_title='Emitters')
        self.FigureApp = FigureApp(parent=self, title='Visualisation', show_toolbar=True)
        self.__figure_ax = self.FigureApp.add_subplot()

        # Instantiate UI objects
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5), self.ui.p2_layout.setVerticalSpacing(5)
        c = Counter()
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_emitters', 'Emitters', '...', unit_obj='QPushButton')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_receivers', 'Receivers', '...', unit_obj='QPushButton')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_X', 'X, analysis range', 'm, m', min_width=100)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_Y', 'Y, analysis range', 'm, m')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_Z', 'Z, analysis range', 'm, m')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_figure_font_size', 'Figure font size', 'pt')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_figure_object_line_thickness', 'Figure object line thickness', 'pt')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_Q_crit', 'Q<sub>crit</sub>', 'kW/m<sup>2</sup>')

        # Assign default values
        self.activated_dialogs.extend([self.TableAppReceiver, self.TableAppEmitter])
        self.ui.p2_in_Q_crit.setText('12.6')
        self.TableAppEmitter.update_table_content(content_data=[[''] * 8], col_headers=['Name', 'x1', 'x2', 'y1', 'y2', 'z1', 'z2', 'Q'])
        self.TableAppReceiver.update_table_content(content_data=[[''] * 7], col_headers=['Name', 'x1', 'x2', 'y1', 'y2', 'z1', 'z2'])

        self.ui.p2_in_emitters_unit.clicked.connect(lambda: self.TableAppEmitter.show())
        self.ui.p2_in_receivers_unit.clicked.connect(lambda: self.TableAppReceiver.show())

    def example(self):
        receiver = Receiver(
            x1=0, x2=10,
            y1=5, y2=5,
            z=0.5,
            delta=0.2
        )

        example_inputs = dict(
            emitters=[
                Emitter(
                    x1=1, x2=2,
                    y1=1, y2=2,
                    z1=0, z2=1,
                    is_parallel=True,
                    receiver=receiver
                ),
                Emitter(
                    x1=3, x2=4,
                    y1=1, y2=1,
                    z1=0, z2=1,
                    is_parallel=True,
                    receiver=receiver
                ),
            ],
            receivers=receiver,
            X=(0, 10),
            Y=(0, 10),
            Z=(0, 5),
            figure_font_size=9,
            figure_object_line_thickness=2,
            Q_crit=12.6,
        )
        self.input_parameters = example_inputs

    def ok(self):
        solver_heat_map_solved = self.calculate(**self.input_parameters)
        self.show_results_in_figure(**solver_heat_map_solved)

    @staticmethod
    def calculate(emitters: List[Emitter], *_, **__):
        return dict(phi=np.sum([emitter.phi for emitter in emitters], axis=0))

    def graphics_max_heat_flux_check(self):
        if self.ui.checkBox_max_heat_flux.isChecked():
            self.ui.doubleSpinBox_graphic_z.setEnabled(False)
            if len(self.solver_results) == 0:
                return 0  # skip if calculation not yet carried out.
            heat_flux = np.max(np.array([i for i in self.solver_results['heat_flux_dict'].values()]), axis=0)
            heat_flux[heat_flux == 0] = -1
            self.solver_results['heat_flux'] = heat_flux
            self.update_plot()
        else:
            self.ui.doubleSpinBox_graphic_z.setEnabled(True)
            self.update_graphic_z_plane()

    @property
    def input_parameters(self):
        return self.__input_parameters

    @input_parameters.setter
    def input_parameters(self, v: dict):
        self.__input_parameters.update(v)

        # receivers_list = list()
        # for i in v['receivers']:
        #     name, is_receiver, x1, x2, y1, y2, z1, z2, T, Q = i.to_list()
        #     receivers_list.append([name, x1, x2, y1, y2, z1, z2])
        # self.TableAppReceiver.update_table_content(
        #     content_data=receivers_list,
        #     col_headers=['name', 'x1', 'x2', 'y1', 'y2', 'z1', 'z2']
        # )

        emitters_list = list()
        for i in v['emitters']:
            name, is_receiver, x1, x2, y1, y2, z1, z2, T, Q = i.to_list()
            emitters_list.append([name, x1, x2, y1, y2, z1, z2, Q])
        self.TableAppEmitter.update_table_content(
            content_data=emitters_list,
            col_headers=['name', 'x1', 'x2', 'y1', 'y2', 'z1', 'z2', 'Q']
        )

        self.ui.p2_in_emitters.setText(f"{len(v['emitters']):d}")
        self.ui.p2_in_receivers.setText(f"{len(v['receivers']):d}")
        self.ui.p2_in_X.setText('{}, {}'.format(*v['X']))
        self.ui.p2_in_Y.setText('{}, {}'.format(*v['Y']))
        self.ui.p2_in_Z.setText('{}, {}'.format(*v['Z']))
        self.ui.p2_in_figure_font_size.setText(f"{v['figure_font_size']:.1f}")
        self.ui.p2_in_figure_object_line_thickness.setText(f"{v['figure_object_line_thickness']:.1f}")
        self.ui.p2_in_Q_crit.setText(f"{v['Q_crit']:.3f}")

    def show_results_in_figure(self, xx, yy, zz):
        contour_line_font_size = 8

        critical_heat_flux = 12.6
        figure_levels = (0, 12.6, 20, 40, 60, 80, 200)
        figure_levels = list(figure_levels) + [critical_heat_flux]
        figure_levels = tuple(sorted(set(figure_levels)))

        figure_levels_contour = figure_levels
        figure_colors_contour = ['r' if i == critical_heat_flux else 'k' for i in figure_levels_contour]
        figure_levels_contourf = figure_levels_contour
        figure_colors_contourf = [cm.get_cmap('YlOrRd')(i / (len(figure_levels_contour) - 1)) for i, _ in
                                  enumerate(figure_levels_contour)]
        figure_colors_contourf = [(r_, g_, b_, 0.65) for r_, g_, b_, a_ in figure_colors_contourf]
        figure_colors_contourf[0] = (195 / 255, 255 / 255, 143 / 255, 0.65)

        ax = self.__figure_ax
        ax.clear()
        # create axes
        cs = ax.contour(xx, yy, zz, levels=figure_levels_contour, colors=figure_colors_contour)
        cs_f = ax.contourf(xx, yy, zz, levels=figure_levels_contourf, colors=figure_colors_contourf)

        if contour_line_font_size > 0:
            ax.clabel(cs, inline=1, fontsize=contour_line_font_size, fmt='%1.1f kW')

        ax.grid(b=True, which='major', axis='both', color='k', alpha=0.1)

        # axis ticks
        ax.set_xticks(np.arange(np.amin(xx), np.amax(xx) + .5, 1))
        ax.set_xticklabels([f'{i:.0f}' for i in np.arange(np.amin(xx), np.amax(xx) + .5, 1)], fontsize=9)
        ax.set_yticks(np.arange(np.amin(yy), np.amax(yy) + .5, 1))
        ax.set_yticklabels([f'{i:.0f}' for i in np.arange(np.amin(yy), np.amax(yy) + .5, 1)], fontsize=9)
        ax.tick_params(axis=u'both', which=u'both', direction='in')

        # axis limits
        ax.set_xlim((np.amin(xx), np.amax(xx)))
        ax.set_ylim((np.amin(yy), np.amax(yy)))

        ax.set_aspect(1)

        self.FigureApp.show()

    def update_emitters_table2obj(self):
        print(self.TableAppEmitter.TableModel.content)


if __name__ == "__main__":
    import sys
    from PySide2 import QtWidgets
    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
    pass
