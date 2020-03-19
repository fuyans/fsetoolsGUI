import sys

import matplotlib.pyplot as plt
import numpy as np
from PySide2 import QtWidgets, QtCore
from fsetools.lib.fse_thermal_radiation_2d_v2 import main as tra_main, main_plot as tra_main_plot

from fsetoolsGUI.gui.layout.dialog_0406_tra_2d_xy_contour import Ui_MainWindow
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow
from fsetoolsGUI.gui.logic.custom_tableview import TableModel

try:
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas,
        NavigationToolbar2QT as NavigationToolbar
    )
except ModuleNotFoundError:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas,
        NavigationToolbar2QT as NavigationToolbar
    )


class Dialog0406(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(
            id='0406',
            title='TRA 2D Parallel',
            parent=parent,
            shortcut_Return=self.calculate
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # instantiate objects
        self.figure = plt.figure()
        self.figure.patch.set_facecolor('None')

        self.ax = self.figure.subplots()
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.figure_canvas = FigureCanvas(self.figure)
        self.figure_canvas.setStyleSheet("background-color:transparent;")  # set the plt widget background from white to transparent.
        self.ui.verticalLayout_plot.addWidget(self.figure_canvas)
        # self.addToolBar(NavigationToolbar(self.figure_canvas, self))  # add plt default toolbar.

        # instantiate variables
        self.Solver = ThreadTRA(self)

        # instantiate tables
        self.init_table()

        # signals
        self.ui.pushButton_ok.clicked.connect(self.calculate)
        self.ui.pushButton_refresh.clicked.connect(self.update_plot)
        self.ui.pushButton_save_figure.clicked.connect(self.save_figure)
        self.ui.pushButton_example.clicked.connect(self.example)
        self.ui.pushButton_emitter_list_append.clicked.connect(lambda x=self.TableModel_emitters, y=self.ui.tableView_emitters: self.table_insert(x, y))
        self.ui.pushButton_emitter_list_remove.clicked.connect(lambda x=self.TableModel_emitters, y=self.ui.tableView_emitters: self.table_remove(x, y))
        self.ui.pushButton_receiver_list_append.clicked.connect(lambda x=self.TableModel_receivers, y=self.ui.tableView_receivers: self.table_insert(x, y))
        self.ui.pushButton_receiver_list_remove.clicked.connect(lambda x=self.TableModel_receivers, y=self.ui.tableView_receivers: self.table_remove(x, y))
        self.ui.horizontalSlider_graphic_line_thickness.valueChanged.connect(lambda: self.update_label(self.ui.label_graphic_line_thickness, f'{self.ui.horizontalSlider_graphic_line_thickness.value():d} pt'))
        self.ui.horizontalSlider_graphic_contour_font_size.valueChanged.connect(lambda: self.update_label(self.ui.label_graphic_contour_label_font_size, f'{self.ui.horizontalSlider_graphic_contour_font_size.value():d} pt'))
        self.ui.doubleSpinBox_graphic_z.valueChanged.connect(self.update_graphic_z_plane)
        self.ui.progressBar.valueChanged.connect(self.update_plot)
        self.Solver.updateProgress.connect(self.ui.progressBar.setValue)
        self.ui.checkBox_max_heat_flux.stateChanged.connect(self.graphics_max_heat_flux_check)

        # containers
        self.__is_first_submit: bool = True
        self.__solver_parameters: dict = dict()
        self.__solver_results: dict = dict()

        self.init()

    def graphics_max_heat_flux_check(self):
        if self.ui.checkBox_max_heat_flux.isChecked():
            self.ui.doubleSpinBox_graphic_z.setEnabled(False)
            if len(self.Solver.results) == 0:
                return 0  # skip if calculation not yet carried out.
            heat_flux = np.max(np.array([i for i in self.Solver.results['heat_flux_dict'].values()]), axis=0)
            heat_flux[heat_flux == 0] = -1
            self.Solver.results['heat_flux'] = heat_flux
            self.update_plot()
        else:
            self.ui.doubleSpinBox_graphic_z.setEnabled(True)
            self.update_graphic_z_plane()

    @staticmethod
    def update_label(QLabel: QtWidgets.QLabel, v: str):
        QLabel.setText(v)

    def update_graphic_z_plane(self):
        """when z-plane value changes, set heat_flux accordingly and perform plot"""
        if len(self.Solver.results) == 0:
            return 0  # skip if calculation not yet carried out.

        z = self.ui.doubleSpinBox_graphic_z.value()

        for i, v in self.Solver.results['heat_flux_dict'].items():
            if abs(float(i) - z) < 1e-5:
                self.Solver.results['heat_flux'] = v
                self.update_plot()
                break

    def table_insert(self, TableModel:TableModel, TableView:QtWidgets.QTableView):
        print('Inserting a row into table.')
        # get selected row index
        selected_indexes = TableView.selectionModel().selectedIndexes()
        selected_row_index = selected_indexes[-1].row()
        print(f'row index {selected_row_index}.')
        # insert
        TableModel.insertRow(selected_row_index)

        print(TableView == self.ui.tableView_emitters)
        TableView.model().layoutChanged.emit()
        TableView.resizeRowsToContents()
        self.repaint()

    def table_remove(self, TableModel:TableModel, TableView:QtWidgets.QTableView):
        if TableModel.rowCount(TableView) <= 1:
            raise ValueError('Not enough rows to delete.')

        # get selected row index
        selected_indexes = TableView.selectionModel().selectedIndexes()
        if len(selected_indexes) > 1:
            selected_row_index = selected_indexes[-1].row()
        else:
            selected_row_index = selected_indexes[0].row()
        # remove
        TableModel.removeRow(selected_row_index)
        TableView.model().layoutChanged.emit()
        TableView.resizeRowsToContents()
        self.repaint()

    def init_table(self):

        emitter_list_default = [
            [''] * 5,
        ]
        emitter_list_header = [
            'Name', 'Point 1', 'Point 2', 'Height', u'kW/m²'
        ]

        self.TableModel_emitters = TableModel(self, content=emitter_list_default, row_header=emitter_list_header)
        self.ui.tableView_emitters.setModel(self.TableModel_emitters)
        self.ui.tableView_emitters.resizeColumnsToContents()

        # width of each column in the table is set to a percentage of total width
        for i_column, width_in_px in enumerate([i * 326 for i in [0.2, 0.2, 0.2, 0.2, 0.2]]):
            self.ui.tableView_emitters.setColumnWidth(i_column, width_in_px)
        self.ui.tableView_emitters.horizontalScrollBar().setEnabled(False)
        self.ui.tableView_emitters.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.tableView_emitters.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ui.tableView_emitters.verticalHeader().setVisible(False)
        self.ui.tableView_emitters.resizeRowsToContents()

        receiver_list_default = [
            [''] * 3,
        ]
        receiver_list_header = [
            'Name', 'Point 1', 'Point 2'
        ]

        self.TableModel_receivers = TableModel(self, content=receiver_list_default, row_header=receiver_list_header)
        self.ui.tableView_receivers.setModel(self.TableModel_receivers)
        self.ui.tableView_receivers.resizeColumnsToContents()

        for i_column, width_in_px in enumerate([i * 331 for i in [0.2, 0.2, 0.2]]):
            self.ui.tableView_receivers.setColumnWidth(i_column, width_in_px)
        self.ui.tableView_receivers.horizontalScrollBar().setEnabled(False)
        self.ui.tableView_receivers.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.tableView_receivers.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ui.tableView_receivers.verticalHeader().setVisible(False)
        self.ui.tableView_receivers.resizeRowsToContents()

    def calculate(self):
        self.ui.checkBox_max_heat_flux.setChecked(True)
        self.ui.doubleSpinBox_graphic_z.setEnabled(False)

        self.Solver.inputs = self.solver_parameters
        self.Solver.start()

    def example(self):

        param_dict = dict(
            emitter_list=[
                dict(
                    name='facade 1',
                    x=[0, 5],
                    y=[0, 0],
                    z=[0, 3],
                    heat_flux=168
                ),
                dict(
                    name='facade 1',
                    x=[5, 10],
                    y=[0, 0],
                    z=[0, 3],
                    heat_flux=84
                ),
            ],
            receiver_list=[
                dict(
                    name='wall 1',
                    x=[0, 10],
                    y=[10, 10]
                )
            ],
            solver_domain=dict(
                x=(-5, 15),
                y=(0, 15),
                z=''
            ),
            solver_delta=.5
        )

        self.solver_parameters = param_dict
        self.repaint()

    def update_plot(self):
        if self.ui.progressBar.value() == 100:

            z_values = [float(i) for i in self.Solver.results['heat_flux_dict'].keys()]
            z_max, z_min = max(z_values), min(z_values)
            self.ui.doubleSpinBox_graphic_z.setRange(z_min, z_max)
            self.ui.doubleSpinBox_graphic_z.setSingleStep((z_max-z_min)/(len(z_values)-1))

            if self.is_first_plot:
                # tra_main_plot(self.Solver.results, ax=self.ax, fig=self.figure, **self.graphic_parameters)
                tra_main_plot(self.Solver.results, ax=self.ax, **self.graphic_parameters)
                self.is_first_plot = False
            else:
                self.ax.clear()
                tra_main_plot(self.Solver.results, ax=self.ax, **self.graphic_parameters)

            # self._update_label_contour_font_size()
            self.figure.tight_layout()
            self.figure_canvas.draw()
            self.repaint()

    def save_figure(self):
        path_to_file, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption='Save Figure',
            dir='image.png'
        )

        self.figure.savefig(path_to_file, dpi=96, transparent=True)

    @property
    def solver_parameters(self) -> dict:
        """parse inputs:dict from ui"""

        solver_parameter_dict = dict()

        # domain, parse domain parameters
        solver_domain_x = [float(i) for i in self.ui.lineEdit_solver_x.text().split(',')]
        solver_domain_y = [float(i) for i in self.ui.lineEdit_solver_y.text().split(',')]
        solver_delta = float(self.ui.lineEdit_solver_delta.text())
        if 'solver_domain' not in self.__solver_parameters:
            solver_parameter_dict['solver_domain'] = dict()

        solver_parameter_dict['solver_delta'] = solver_delta
        solver_parameter_dict['solver_domain']['x'] = solver_domain_x
        solver_parameter_dict['solver_domain']['y'] = solver_domain_y

        if len(self.ui.lineEdit_solver_z.text().strip()) == 0:
            solver_parameter_dict['solver_domain']['z'] = None
        else:
            solver_domain_z = [float(i) for i in self.ui.lineEdit_solver_z.text().split(',')]
            solver_parameter_dict['solver_domain']['z'] = solver_domain_z

        # emitters, parse emitter parameters
        solver_parameter_dict['emitter_list'] = self.solver_parameter_emitters

        # receivers, parse receiver parameters
        solver_parameter_dict['receiver_list'] = self.solver_parameter_receivers

        return solver_parameter_dict

    @solver_parameters.setter
    def solver_parameters(self, solver_parameter_dict: dict = None):
        """map solver_parameter_dict:dict to ui."""

        # domain, parse domain parameters
        solver_domain_x = ','.join(
            f'{i:.3f}'.rstrip('0').rstrip('.') for i in solver_parameter_dict['solver_domain']['x']
        )
        solver_domain_y = ','.join(
            f'{i:.3f}'.rstrip('0').rstrip('.') for i in solver_parameter_dict['solver_domain']['y'])
        if len(solver_parameter_dict["solver_domain"]["z"]) == 0:
            solver_domain_z = None
        else:
            solver_domain_z = f'{solver_parameter_dict["solver_domain"]["z"][0]:.3f}'.rstrip('0').rstrip('.')
        solver_delta = f'{solver_parameter_dict["solver_delta"]:.3f}'.rstrip('0').rstrip('.')

        self.ui.lineEdit_solver_x.setText(solver_domain_x)
        self.ui.lineEdit_solver_y.setText(solver_domain_y)
        self.ui.lineEdit_solver_z.setText(solver_domain_z)
        self.ui.lineEdit_solver_delta.setText(solver_delta)

        # emitters, parse emitter parameters
        self.solver_parameter_emitters = solver_parameter_dict['emitter_list']

        # receivers, parse receiver parameters
        self.solver_parameter_receivers = solver_parameter_dict['receiver_list']

        self.repaint()

    @property
    def solver_parameter_emitters(self) -> list:
        """parse `emitter_list` from ui."""

        emitter_list = list()
        for emitter in self.TableModel_emitters.content:
            name, xy1, xy2, z1z2, q = emitter
            x1, y1 = xy1.split(',')
            x2, y2 = xy2.split(',')
            z1, z2 = z1z2.split(',')

            emitter_list.append(
                dict(
                    name=name,
                    x=(float(x1), float(x2)),
                    y=(float(y1), float(y2)),
                    z=(float(z1), float(z2)),
                    heat_flux=float(q)
                )
            )
        return emitter_list

    @solver_parameter_emitters.setter
    def solver_parameter_emitters(self, emitter_list: list):
        """cast `emitter_list` onto ui."""

        emitter_list_prepared = list()

        for emitter in emitter_list:
            name = emitter['name']
            x1, x2 = emitter['x']
            y1, y2 = emitter['y']
            z1, z2 = emitter['z']
            q = emitter['heat_flux']

            xy1 = ','.join(f'{i:.3f}'.rstrip('0').rstrip('.') for i in [x1, y1])
            xy2 = ','.join(f'{i:.3f}'.rstrip('0').rstrip('.') for i in [x2, y2])
            z1z2 = ','.join(f'{i:.3f}'.rstrip('0').rstrip('.') for i in [z1, z2])
            q = f'{q:.3f}'.rstrip('0').rstrip('.')

            emitter_list_prepared.append([name, xy1, xy2, z1z2, q])

        self.TableModel_emitters.content = emitter_list_prepared
        self.ui.tableView_emitters.model().layoutChanged.emit()
        self.ui.tableView_emitters.resizeRowsToContents()
        self.repaint()

    @property
    def solver_parameter_receivers(self) -> list:
        """parse `receiver_list` from ui."""

        receiver_list = list()

        for receiver in self.TableModel_receivers.content:
            name, xy1, xy2 = receiver
            x1, y1 = xy1.split(',')
            x2, y2 = xy2.split(',')

            receiver_list.append(
                dict(
                    name=name,
                    x=(float(x1), float(x2)),
                    y=(float(y1), float(y2)),
                )
            )
        return receiver_list

    @solver_parameter_receivers.setter
    def solver_parameter_receivers(self, receiver_list: list):
        """cast `receiver_list` onto ui."""

        receiver_list_prepared = list()

        for receiver in receiver_list:
            name = receiver['name']
            x1, x2 = receiver['x']
            y1, y2 = receiver['y']

            xy1 = ','.join(f'{i:.3f}'.rstrip('0').rstrip('.') for i in [x1, y1])
            xy2 = ','.join(f'{i:.3f}'.rstrip('0').rstrip('.') for i in [x2, y2])

            receiver_list_prepared.append([name, xy1, xy2])

        self.TableModel_receivers.content = receiver_list_prepared
        self.ui.tableView_receivers.model().layoutChanged.emit()
        self.ui.tableView_receivers.resizeRowsToContents()
        self.repaint()

    @property
    def graphic_parameters(self):
        param_dict = dict(
            critical_heat_flux=float(self.ui.lineEdit_graphic_critical_heat_flux.text()),
            contour_line_font_size=float(self.ui.horizontalSlider_graphic_contour_font_size.value()),
            emitter_receiver_line_thickness=float(self.ui.horizontalSlider_graphic_line_thickness.value())
        )
        return param_dict

    @graphic_parameters.setter
    def graphic_parameters(self, param_dict: dict):
        pass  # todo

    @property
    def is_first_plot(self):
        return self.__is_first_submit

    @is_first_plot.setter
    def is_first_plot(self, v: bool):
        self.__is_first_submit = v


#Inherit from QThread
class ThreadTRA(QtCore.QThread):

    #This is the signal that will be emitted during the processing.
    #By including int as an argument, it lets the signal know to expect
    #an integer argument when emitting.
    updateProgress = QtCore.Signal(int)

    #You can do any extra things in this init you need, but for this example
    #nothing else needs to be done expect call the super's init
    def __init__(
            self,
            # MasterWidget: Dialog0406,
            parent=None,
    ):
        super().__init__(parent=parent)
        self.__solver_results: dict = dict()
        self.__solver_parameters: dict = dict()

    @property
    def inputs(self):
        return self.__solver_parameters

    @inputs.setter
    def inputs(self, v):
        self.__solver_parameters = v

    @property
    def results(self):
        return self.__solver_results

    @results.setter
    def results(self, v):
        self.__solver_results = v

    #A QThread is run by calling it's start() function, which calls this run()
    #function in it's own "thread".
    def run(self):
        #Notice this is the same thing you were doing in your progress() function

        if len(self.__solver_parameters) > 0:
            self.__solver_results = tra_main(self.__solver_parameters, QtCore_ProgressSignal=self.updateProgress)
            self.updateProgress.emit(100)


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = Dialog0406()
    app.show()
    qapp.exec_()
