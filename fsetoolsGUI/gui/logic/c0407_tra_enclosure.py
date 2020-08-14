import sys
from os import path

import numpy as np
from PySide2 import QtWidgets
from PySide2.QtWidgets import QLabel, QGridLayout, QVBoxLayout
from fsetools.lib.fse_thermal_radiation_2d_ortho import CuboidRoomModel
from matplotlib import cm

import fsetoolsGUI
from fsetoolsGUI.gui.logic.custom_app_template_1 import AppBaseClass
from fsetoolsGUI.gui.logic.custom_plot import App as PlotApp
from fsetoolsGUI.gui.logic.custom_table import TableWindow


class App(AppBaseClass):
    app_id = '0407'
    app_name_short = 'TRA\ncuboid\nenclosure\nmodel'
    app_name_long = 'TRA cuboid enclosure model'

    def __init__(self, parent=None):

        # instantiate super
        super().__init__(parent=parent)

        # ==============
        # instantiate ui
        # ==============
        # self.ui.label_figure.setPixmap(path.join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0407-1.png'))
        # self.ui.in_mesh_resolution.setToolTip('Equivalent to mesh resolution, proportionate to results accuracy')
        self.init_ui()

        # =======================
        # create local parameters
        # =======================
        self.__Figure = None
        self.__Figure_ax = None
        self.__Table = None
        self.__input_parameters: dict = None
        self.__output_parameters: dict = None

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
        self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.setVerticalSpacing(2)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), 0, 0, 1, 3)
        self.add_widget_to_grid(self.ui.p2_layout, 1, 'in_width', '  Width', 'm')
        self.add_widget_to_grid(self.ui.p2_layout, 2, 'in_depth', '  Depth', 'm')
        self.add_widget_to_grid(self.ui.p2_layout, 3, 'in_height', '  Height', 'm')
        self.add_widget_to_grid(self.ui.p2_layout, 4, 'in_mesh_resolution', ' Mesh resolution', 'm')
        self.ui.in_mesh_resolution.setToolTip('Equivalent to mesh resolution, proportionate to results accuracy')
        self.add_widget_to_grid(self.ui.p2_layout, 5, 'in_wall_1_heat_flux', '  Wall 1 heat flux', 'kW/m²')
        self.add_widget_to_grid(self.ui.p2_layout, 6, 'in_wall_2_heat_flux', '  Wall 2 heat flux', 'kW/m²')
        self.add_widget_to_grid(self.ui.p2_layout, 7, 'in_wall_3_heat_flux', '  Wall 3 heat flux', 'kW/m²')
        self.add_widget_to_grid(self.ui.p2_layout, 8, 'in_wall_4_heat_flux', '  Wall 4 heat flux', 'kW/m²')
        self.add_widget_to_grid(self.ui.p2_layout, 9, 'in_floor_heat_flux', '  Floor heat flux', 'kW/m²')
        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), 10, 0, 1, 3)
        self.add_widget_to_grid(self.ui.p2_layout, 11, 'out_max_heat_flux', '  Maximum heat flux', 'kW/m²')

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
            self.__Table.show()
            self.__Figure.show()
        except Exception as e:
            self.statusBar().showMessage(f'Unable to show results in table or figure. Error {str(e)}')
            return

        self.statusBar().showMessage('Calculation complete', 5)

    def show_results_in_table(self):

        output_parameters = self.output_parameters
        list_content = output_parameters['resultant_heat_flux'].tolist()
        xx = [f'{i:.3f}' for i in output_parameters['xx'][0, :].astype(float)]
        yy = [f'{i:.3f}' for i in output_parameters['yy'][:, 0].astype(float)]

        try:
            win_geo = self.__Table.geometry()
            self.__Table.destroy(destroyWindow=True, destroySubWindows=True)
            del self.__Table
        except AttributeError as e:
            win_geo = None

        self.__Table = TableWindow(
            parent=self,
            window_geometry=win_geo,
            data_list=list_content,
            header_col=xx,
            header_row=yy,
            window_title='Heat flux numerical results',
            enable_sorting=False,
        )
        # self.__Table.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        self.__Table.TableView.resizeColumnsToContents()
        self.__Table.show()

        return True

    def show_results_in_figure(self):
        """Show contour plot of the calculated heat flux at the ceiling surface as in a separate dialog.
        """

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

        # =========================
        # instantiate figure object
        # =========================
        if self.__Figure is None:
            self.__Figure = PlotApp(self, title='Heat flux contour plot')
            self.__Figure_ax = self.__Figure.add_subplots()
        else:
            self.__Figure_ax.clear()

        # ==========
        # make plots
        # ==========
        figure_levels = np.linspace(np.amin(resultant_heat_flux), np.amax(resultant_heat_flux), 15)
        figure_colors_contour = ['k'] * len(figure_levels)
        figure_colors_contourf = [cm.get_cmap('YlOrRd')(i / (len(figure_levels) - 1)) for i in
                                  range(len(figure_levels))]
        figure_colors_contourf = [(r_, g_, b_, 1) for r_, g_, b_, a_ in figure_colors_contourf]

        # plot line contour
        cs = self.__Figure_ax.contour(xx, yy, resultant_heat_flux, levels=figure_levels, colors=figure_colors_contour,
                                      linewidths=0.25)
        # plot filled contour
        cs_f = self.__Figure_ax.contourf(xx, yy, resultant_heat_flux, levels=figure_levels,
                                         colors=figure_colors_contourf)

        self.__Figure_ax.clabel(cs, inline=1, fontsize='small', fmt='%1.3f kW')
        self.__Figure_ax.grid(b=True, which='major', axis='both', color='k', alpha=0.1)

        # ============
        # format plots
        # ============
        # axis labels
        self.__Figure_ax.set_xlabel('Width [m]', fontsize='small')
        self.__Figure_ax.set_ylabel('Depth [m]', fontsize='small')
        # axis ticks
        self.__Figure_ax.set_xticks(np.arange(0, width + .5, 1))
        self.__Figure_ax.set_xticklabels([f'{i:.0f}' for i in np.arange(0, width + .5, 1)], fontsize='small')
        self.__Figure_ax.set_yticks(np.arange(0, depth + .5, 1))
        self.__Figure_ax.set_yticklabels([f'{i:.0f}' for i in np.arange(0, depth + .5, 1)], fontsize='small')
        self.__Figure_ax.tick_params(axis=u'both', which=u'both', direction='in')

        # axis limits
        self.__Figure_ax.set_xlim(0, width)
        self.__Figure_ax.set_ylim(0, depth)

        self.__Figure_ax.set_aspect(1)

        # ======================
        # refresh and show plots
        # ======================
        self.__Figure.figure.tight_layout()
        self.__Figure.figure_canvas.draw()

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
    app = App()
    app.show()
    qapp.exec_()
