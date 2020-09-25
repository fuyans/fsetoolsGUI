import sys
from os import path

import numpy as np
from PySide2 import QtWidgets
from PySide2.QtWidgets import QLabel, QGridLayout, QVBoxLayout
from fsetools.lib.fse_thermal_radiation_2d_ortho import CuboidRoomModel
from matplotlib import cm

import fsetoolsGUI
from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass
from fsetoolsGUI.gui.logic.custom_plot import App as PlotApp
from fsetoolsGUI.gui.logic.custom_table import TableWindow


class App(AppBaseClass):
    app_id = '0407'
    app_name_short = 'TRA\ncuboid\nenclosure\nmodel'
    app_name_long = 'TRA cuboid enclosure model'

    def __init__(self, parent=None, post_stats: bool = True):

        # instantiate super
        super().__init__(parent=parent, post_stats=post_stats)

        # =======================
        # create local parameters
        # =======================
        self.FigureApp = PlotApp(parent=self, title='Heat flux contour plot')
        self.TableApp = TableWindow(parent=self, window_title='Results')
        self.activated_dialogs.extend([self.FigureApp, self.TableApp])
        self.__figure_ax = self.FigureApp.add_subplot()
        self.__input_parameters: dict = None
        self.__output_parameters: dict = None

        # ==============
        # instantiate ui
        # ==============
        self.init_ui()

        # =============
        # setup signals
        # =============
        self.ui.p3_submit.clicked.connect(self.calculate)
        self.ui.p3_example.clicked.connect(self.example)

    def init_ui(self):

        self.ui.p1_description = QLabel(
            'This app calculates the imposed thermal radiation heat flux at the ceiling surface due to the wall and '
            'floor within the same enclosure as per figure below.'
        )
        self.ui.p1_description.setFixedWidth(350)
        self.ui.p1_description.setWordWrap(True)
        self.ui.p1_figure = QLabel()
        self.ui.p1_figure.setPixmap(path.join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0407-1.png'))
        self.ui.p1_layout = QVBoxLayout(self.ui.page_1)
        self.ui.p1_layout.addWidget(self.ui.p1_description)
        self.ui.p1_layout.addWidget(self.ui.p1_figure)

        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5), self.ui.p2_layout.setVerticalSpacing(5)

        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), 0, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 1, 'in_width', '  Width', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 2, 'in_depth', '  Depth', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 3, 'in_height', '  Height', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 4, 'in_mesh_resolution', ' Mesh resolution', 'm')
        self.ui.in_mesh_resolution.setToolTip('Equivalent to mesh resolution, proportionate to results accuracy')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 5, 'in_wall_1_heat_flux', '  Wall 1 heat flux', 'kW/m²')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 6, 'in_wall_2_heat_flux', '  Wall 2 heat flux', 'kW/m²')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 7, 'in_wall_3_heat_flux', '  Wall 3 heat flux', 'kW/m²')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 8, 'in_wall_4_heat_flux', '  Wall 4 heat flux', 'kW/m²')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 9, 'in_floor_heat_flux', '  Floor heat flux', 'kW/m²')

        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), 10, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 11, 'out_max_heat_flux', '  Maximum heat flux', 'kW/m²')

    @property
    def input_parameters(self):

        def str2num(v: str):
            try:
                return float(v)
            except ValueError:
                return None

        width = str2num(self.ui.in_width.text())
        depth = str2num(self.ui.in_depth.text())
        height = str2num(self.ui.in_height.text())
        deltas = str2num(self.ui.in_mesh_resolution.text())
        wall_1_heat_flux = str2num(self.ui.in_wall_1_heat_flux.text())
        wall_2_heat_flux = str2num(self.ui.in_wall_2_heat_flux.text())
        wall_3_heat_flux = str2num(self.ui.in_wall_3_heat_flux.text())
        wall_4_heat_flux = str2num(self.ui.in_wall_4_heat_flux.text())
        floor_heat_flux = str2num(self.ui.in_floor_heat_flux.text())

        self.__input_parameters = dict(
            width=width, depth=depth, height=height, deltas=deltas, wall_1_heat_flux=wall_1_heat_flux,
            wall_2_heat_flux=wall_2_heat_flux, wall_3_heat_flux=wall_3_heat_flux, wall_4_heat_flux=wall_4_heat_flux,
            floor_heat_flux=floor_heat_flux)

        return self.__input_parameters

    @input_parameters.setter
    def input_parameters(self, v: dict):

        for k in v.keys():
            v[k] = str(v[k])

        width = v['width']
        depth = v['depth']
        height = v['height']
        deltas = v['deltas']
        wall_1_heat_flux = v['wall_1_heat_flux']
        wall_2_heat_flux = v['wall_2_heat_flux']
        wall_3_heat_flux = v['wall_3_heat_flux']
        wall_4_heat_flux = v['wall_4_heat_flux']
        floor_heat_flux = v['floor_heat_flux']

        self.ui.in_width.setText(width)
        self.ui.in_depth.setText(depth)
        self.ui.in_height.setText(height)
        self.ui.in_mesh_resolution.setText(deltas)
        self.ui.in_wall_1_heat_flux.setText(wall_1_heat_flux)
        self.ui.in_wall_2_heat_flux.setText(wall_2_heat_flux)
        self.ui.in_wall_3_heat_flux.setText(wall_3_heat_flux)
        self.ui.in_wall_4_heat_flux.setText(wall_4_heat_flux)
        self.ui.in_floor_heat_flux.setText(floor_heat_flux)

    @property
    def output_parameters(self):
        return self.__output_parameters

    @output_parameters.setter
    def output_parameters(self, output_parameters: dict):
        self.__output_parameters = output_parameters

        self.ui.out_max_heat_flux.setText(f'{np.amax(output_parameters["resultant_heat_flux"]):.2f}')

    def example(self):
        input_parameters = dict(
            width=8,
            depth=5,
            height=2,
            deltas=0.05,
            wall_1_heat_flux=1,
            wall_2_heat_flux=1,
            wall_3_heat_flux=1,
            wall_4_heat_flux=1,
            floor_heat_flux=0,
        )
        self.input_parameters = input_parameters
        self.repaint()

    def ok(self):
        self.calculate()

    def calculate(self):
        try:
            self.statusBar().showMessage('Parsing inputs from UI')
            self.repaint()
            input_parameters = self.input_parameters
        except Exception as e:
            self.statusBar().showMessage(f'Unable to parse inputs. Error {str(e)}')
            return

        try:
            self.statusBar().showMessage('Calculation started', 5)
            self.repaint()
            output_parameters = self.__calculate_worker(**input_parameters)
        except Exception as e:
            self.statusBar().showMessage(f'Calculation failed. Error {str(e)}')
            return

        try:
            self.statusBar().showMessage('Preparing results', 5)
            self.repaint()
            self.output_parameters = output_parameters
            assert self.show_results_in_table()
            self.show_results_in_figure()
            self.TableApp.show()
            self.FigureApp.show()
        except Exception as e:
            self.statusBar().showMessage(f'Unable to show results in table or figure. Error {str(e)}')
            return

        self.statusBar().showMessage('Calculation complete', 5)

    def show_results_in_table(self):

        output_parameters = self.output_parameters
        list_content = output_parameters['resultant_heat_flux'].tolist()
        xx = [f'{i:.3f}' for i in output_parameters['xx'][0, :].astype(float)]
        yy = [f'{i:.3f}' for i in output_parameters['yy'][:, 0].astype(float)]

        self.TableApp.update_table_content(
            content_data=list_content,
            row_headers=yy,
            col_headers=xx
        )

        self.TableApp.refresh_content_size()
        self.TableApp.show()

        return True

    def show_results_in_figure(self):
        """Show contour plot of the calculated heat flux at the ceiling surface as in a separate dialog.
        """

        self.__figure_ax.clear()

        # =========================================
        # prepare parameters necessary for the plot
        # =========================================
        input_parameters = self.__input_parameters
        output_parameters = self.output_parameters
        xx = output_parameters['xx']
        yy = output_parameters['yy']
        resultant_heat_flux = output_parameters['resultant_heat_flux']
        width = input_parameters['width']
        depth = input_parameters['depth']

        # ==========
        # make plots
        # ==========
        figure_levels = np.linspace(np.amin(resultant_heat_flux), np.amax(resultant_heat_flux), 15)
        figure_colors_contour = ['k'] * len(figure_levels)
        figure_colors_contourf = [cm.get_cmap('YlOrRd')(i / (len(figure_levels) - 1)) for i in range(len(figure_levels))]
        figure_colors_contourf = [(r_, g_, b_, 1) for r_, g_, b_, a_ in figure_colors_contourf]

        # plot line contour
        cs = self.__figure_ax.contour(xx, yy, resultant_heat_flux, levels=figure_levels, colors=figure_colors_contour, linewidths=0.25)
        # plot filled contour
        cs_f = self.__figure_ax.contourf(xx, yy, resultant_heat_flux, levels=figure_levels, colors=figure_colors_contourf)

        self.__figure_ax.clabel(cs, inline=1, fontsize='small', fmt='%1.3f kW')
        self.__figure_ax.grid(b=True, which='major', axis='both', color='k', alpha=0.1)

        # ============
        # format plots
        # ============
        # axis labels
        self.__figure_ax.set_xlabel('Width [m]', fontsize='small')
        self.__figure_ax.set_ylabel('Depth [m]', fontsize='small')
        # axis ticks
        self.__figure_ax.set_xticks(np.arange(0, width + .5, 1))
        self.__figure_ax.set_xticklabels([f'{i:.0f}' for i in np.arange(0, width + .5, 1)], fontsize='small')
        self.__figure_ax.set_yticks(np.arange(0, depth + .5, 1))
        self.__figure_ax.set_yticklabels([f'{i:.0f}' for i in np.arange(0, depth + .5, 1)], fontsize='small')
        self.__figure_ax.tick_params(axis=u'both', which=u'both', direction='in')

        # axis limits
        self.__figure_ax.set_xlim(0, width)
        self.__figure_ax.set_ylim(0, depth)

        self.__figure_ax.set_aspect(1)

        self.FigureApp.show()
        self.FigureApp.refresh_figure()

    @staticmethod
    def __calculate_worker(
            width, depth, height, deltas,
            wall_1_heat_flux, wall_2_heat_flux, wall_3_heat_flux, wall_4_heat_flux, floor_heat_flux,
            *_, **__
    ):

        model = CuboidRoomModel(width=width, depth=depth, height=height, delta=deltas)
        resultant_heat_flux = model.resultant_heat_flux(
            (wall_1_heat_flux, wall_2_heat_flux, wall_3_heat_flux, wall_4_heat_flux, floor_heat_flux)
        )[:, :, 0]
        xx, yy, zz = model.ceiling.mesh_grid_3d
        return dict(xx=xx[:, :, 0], yy=yy[:, :, 0], resultant_heat_flux=resultant_heat_flux)


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
